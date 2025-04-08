# InterviewAlchemy 🧪

> Transform your interview preparation with AI-powered mock interviews

InterviewAlchemy is an innovative AI-powered interview simulator that uses autonomous agents to create realistic technical interview experiences. By leveraging the power of Microsoft's Autogen framework and GPT-4, it creates dynamic conversations between an AI interviewer and an AI candidate, helping you understand both sides of the interview process.

![InterviewAlchemy Demo](assets/demo.gif)

## ✨ Features

- 🤖 Dual AI Agents: Interviewer and Candidate roles
- 🎯 Role-specific interviews for various tech positions
- 📊 Real-time feedback and performance analysis
- 🔄 Natural conversation flow with turn-based interactions
- 🎨 Clean, intuitive Gradio web interface
- 📝 Comprehensive interview summaries
- 🎭 Experience level adaptation (Junior to Senior)
- 🛠️ Multiple technical focus areas

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- OpenAI API key
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/r123singh/interview-alchemy.git
cd interview-alchemy
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_api_key_here
```

### Running the Application

1. Start the application:
```bash
python interview_simulator.py
```

2. Open your browser and navigate to:
```
http://localhost:7860
```

## 🎮 Usage

1. **Select Job Role**: Choose from various technical positions
   - Frontend Developer
   - Backend Developer
   - Full Stack Developer
   - Data Scientist
   - DevOps Engineer
   - Machine Learning Engineer

2. **Configure Interview**:
   - Set experience level (Junior/Mid-level/Senior)
   - Choose technical focus areas
   - Select interview duration

3. **Start Interview**: Click "Start Interview" to begin the simulation

4. **Review Results**: Get instant feedback and a comprehensive summary

## 🛠️ Technical Architecture

```
interview-alchemy/
├── interview_simulator.py   # Main application file
├── requirements.txt        # Project dependencies
├── .env                   # Environment variables
└── assets/               # Images and resources
```

### Key Components

- **Autogen Agents**: Manages AI agent interactions
- **Gradio Interface**: Handles web UI and real-time updates
- **GroupChat System**: Coordinates agent communication
- **Message Processor**: Formats and streams responses

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- Microsoft Autogen team for the amazing framework
- OpenAI for GPT-4 API
- Gradio team for the wonderful UI framework

## 🔮 Future Plans

- [ ] Multi-agent panel interviews
- [ ] Custom question sets
- [ ] Interview recording and playback
- [ ] Performance analytics dashboard
- [ ] Integration with code execution environments
- [ ] Support for more specialized roles

---

Built with ❤️ using Microsoft Autogen and GPT-4