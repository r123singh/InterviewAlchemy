import os
import gradio as gr
import autogen
from dotenv import load_dotenv
from typing import List, Dict
import time

# Load environment variables
load_dotenv()

# Configure OpenAI
config_list = [
    {
        'model': 'gpt-4',
        'api_key': os.getenv('OPENAI_API_KEY')
    }
]

class InterviewSimulator:
    def __init__(self):
        # Initialize the agents
        self.interviewer = autogen.AssistantAgent(
            name="interviewer",
            system_message="""You are an experienced technical interviewer. Your role is to:
            1. Ask relevant technical and behavioral questions based on the job role
            2. Evaluate the candidate's responses
            3. Provide constructive feedback
            4. Maintain a professional and encouraging tone
            5. Focus on both technical skills and soft skills
            
            Format your responses using markdown for better readability.
            End the interview by saying 'INTERVIEW_COMPLETE' when you have gathered enough information.""",
            llm_config={"config_list": config_list}
        )

        self.candidate = autogen.AssistantAgent(
            name="candidate",
            system_message="""You are a job candidate interviewing for a technical position. You should:
            1. Respond based on your assigned experience level and role
            2. Use the STAR method when appropriate
            3. Be honest and professional
            4. Ask clarifying questions when needed
            5. Show enthusiasm and willingness to learn
            
            Format your responses using markdown for better readability.""",
            llm_config={"config_list": config_list}
        )

    def start_interview(
        self,
        job_role: str,
        experience_level: str,
        technical_focus: str,
        interview_duration: str,
        progress=gr.Progress()
    ) -> gr.components.Component:
        """Start the interview simulation with streaming"""
        
        interview_log = []
        feedback = []
        summary = "## Interview Summary\n\n"

        def update_chat_log(name, content):
            nonlocal interview_log, feedback
            if name == "interviewer":
                msg = f"👤 **Interviewer**: {content}\n\n"
                if "feedback" in content.lower():
                    feedback.append(content)
            else:
                msg = f"🎯 **Candidate**: {content}\n\n"
            interview_log.append(msg)
            return "".join(interview_log), "\n".join(feedback), summary

        # Construct the interview prompt
        interview_prompt = f"""
        Conduct a technical interview for a {job_role} position.
        - Candidate Experience Level: {experience_level}
        - Technical Focus Areas: {technical_focus}
        - Interview Duration: {interview_duration}
        
        Follow this structure:
        1. Start with a brief introduction
        2. Ask relevant technical questions
        3. Include behavioral questions
        4. Provide feedback after each response
        5. Conclude with a summary
        
        Keep responses concise and focused.
        """

        # Initial message from interviewer
        initial_msg = "Hello! I'll be conducting your technical interview today. Let's begin with a brief introduction."
        chat_output = update_chat_log("interviewer", initial_msg)
        yield chat_output

        # Create team for the interview with termination condition
        team = autogen.GroupChat(
            agents=[self.interviewer, self.candidate],
            messages=[],
            max_round=12,
            speaker_selection_method="round_robin",
            allow_repeat_speaker=False
        )
        
        manager = autogen.GroupChatManager(
            groupchat=team,
            llm_config={"config_list": config_list}
        )

        # Run the interview
        chat_messages = manager.initiate_chat(
            self.interviewer,
            message=interview_prompt
        )

        # Process messages
        for message in team.messages[1:]:  # Skip the first message as we already displayed it
            name = message.get("name", "")
            content = message.get("content", "")
            
            if content and name:  # Only process if we have both name and content
                chat_output = update_chat_log(name, content)
                yield chat_output
                time.sleep(1)  # Add delay for readability

        # Generate final summary
        summary += "### Key Points:\n"
        summary += "- Technical Knowledge\n"
        summary += "- Communication Skills\n"
        summary += "- Problem-solving Approach\n\n"
        
        summary += "### Feedback Summary:\n"
        if feedback:
            for f in feedback[-3:]:
                summary += f"- {f.split('feedback:')[-1].strip()}\n"
        else:
            summary += "- Interview completed\n"

        yield (
            "".join(interview_log),
            "\n".join(feedback),
            summary
        )

# Create the Gradio interface
def create_interface():
    with gr.Blocks(theme=gr.themes.Soft()) as interface:
        gr.Markdown("""
        # 🤖 AI Interview Simulator
        
        Practice technical interviews with AI-powered interviewer and candidate simulation.
        """)

        with gr.Row():
            with gr.Column():
                job_role = gr.Dropdown(
                    choices=[
                        "Frontend Developer",
                        "Backend Developer",
                        "Full Stack Developer",
                        "Data Scientist",
                        "DevOps Engineer",
                        "Machine Learning Engineer"
                    ],
                    label="Job Role",
                    value="Frontend Developer"
                )
                
                experience_level = gr.Radio(
                    choices=["Junior", "Mid-level", "Senior"],
                    label="Experience Level",
                    value="Junior"
                )
                
                technical_focus = gr.CheckboxGroup(
                    choices=[
                        "Algorithms & Data Structures",
                        "System Design",
                        "Programming Languages",
                        "Frameworks & Tools",
                        "Soft Skills"
                    ],
                    label="Technical Focus Areas",
                    value=["Programming Languages", "Frameworks & Tools"]
                )
                
                interview_duration = gr.Dropdown(
                    choices=["15 minutes", "30 minutes", "45 minutes"],
                    label="Interview Duration",
                    value="30 minutes"
                )
                
                start_btn = gr.Button("Start Interview", variant="primary")

        with gr.Row():
            with gr.Column():
                interview_output = gr.Markdown(label="Interview Progress")
            with gr.Column():
                feedback_output = gr.Markdown(label="Feedback")
                summary_output = gr.Markdown(label="Summary")

        # Initialize the simulator
        simulator = InterviewSimulator()

        # Handle the start button click with streaming
        start_btn.click(
            fn=simulator.start_interview,
            inputs=[
                job_role,
                experience_level,
                technical_focus,
                interview_duration
            ],
            outputs=[
                interview_output,
                feedback_output,
                summary_output
            ],
            show_progress=True
        )

    return interface

if __name__ == "__main__":
    demo = create_interface()
    demo.queue()  # Enable queuing for streaming
    demo.launch(share=True) 