# Mental Health Support Application

A comprehensive mental health support chatbot built with CrewAI, Streamlit, and Mem0, offering personalized therapy sessions, knowledge-based responses, and voice interaction capabilities.

## Overview

This application provides mental health support through a structured process:
1. User profile collection
2. AI-powered therapy session
3. Personalized support chat based on therapy outcomes

## Features

- **Multi-Agent System**: Three specialized AI agents work together:
  - **Therapist Agent**: Conducts empathetic therapy sessions
  - **Knowledge Specialist**: Searches mental health knowledge base
  - **Summarizer Agent**: Creates personalized, style-adapted responses
  
- **Memory Integration**: Uses Mem0 for maintaining conversation context
- **Voice Support**: Speech-to-text and text-to-speech capabilities
- **Knowledge Base**: PDF-based mental health resources
- **Personalization**: Adapts response style to user preferences
- **Session Management**: Complete session flow from intake to summary

## Project Structure

```
├── app.py                    # Main Streamlit application entry point
├── pages/
│   ├── 1_user_input.py      # User information collection
│   ├── 2_therapy_session.py  # AI therapy session interface
│   ├── 3_chatbot.py         # Main support chat interface
│   └── 4_session_summary.py  # Session summary and feedback
├── src/
│   └── crewai_knowledge_chatbot/
│       ├── crew.py          # CrewAI agent and task definitions
│       └── main.py          # CLI version of the chatbot
├── config/
│   ├── agents.yaml          # Agent role definitions
│   └── tasks.yaml           # Task configurations
└── [PDF files]              # Mental health knowledge base documents
```

## Technology Stack

- **Framework**: Streamlit for web interface
- **AI Framework**: CrewAI for multi-agent orchestration
- **Memory**: Mem0 for context management
- **Speech Processing**: 
  - Google Speech Recognition for transcription
  - gTTS (Google Text-to-Speech) for audio generation
  - audiorecorder for voice input
- **Knowledge Base**: PDF files processed through CrewAI's PDFKnowledgeSource

## Prerequisites

```bash
# Core dependencies
crewai
streamlit
mem0
python-dotenv
speech_recognition
gtts
audiorecorder
```

## Installation Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd mental-health-chatbot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3.A. Set up environment variables
```bash
# Create .env file with required keys
cp .env.example .env

OPENAI_API_KEY=sk-...        For CrewAI's LLM operations
MEM0_API_KEY=...             If using Mem0 cloud service (optional if using local)
MODEL=
```

3.B. Add their OpenAI API key, model and Mem0 key to .env file
```bash
OPENAI_API_KEY=sk-...        For CrewAI's LLM operations
MEM0_API_KEY=...             If using Mem0 cloud service (optional if using local)
MODEL=
```


4. Add your mental health resource PDFs to the project directory:
   - `first_resource.pdf`
   - `second_resource.pdf`
   - `third_resource.pdf`

5. Directory Structure Setup
   ```bash
   mkdir -p src/crewai_knowledge_chatbot
   mkdir config
   mkdir pages
   touch src/__init__.py
   touch src/crewai_knowledge_chatbot/__init__.py
   src/crewai_knowledge_chatbot/__init__.py
    ```


## Usage

### Web Application

Run the Streamlit application:
```bash
streamlit run app.py
```

Navigate through the application:
1. **User Input**: Provide basic information and preferences
2. **Therapy Session**: Answer 7 structured questions
3. **Support Chat**: Engage in personalized conversation
4. **Session Summary**: Review insights and get recommendations

### Command Line Interface

Run the CLI version:
```bash
python src/crewai_knowledge_chatbot/main.py
```

## Configuration

### Agent Roles (config/agents.yaml)

- **Therapist**: Empathetic questioner for understanding user needs
- **Knowledge Specialist**: Searches knowledge base for relevant information
- **Summarizer**: Creates concise, style-adapted responses

### Communication Styles

Users can choose from three response styles:
1. Supportive and empathetic
2. Direct and solution-focused
3. Educational and informative

## Key Components

### 1. User Profile Collection
- Name, age group, mood assessment
- Concern selection (stress, anxiety, depression, etc.)
- Communication style preference

### 2. Therapy Session
- 7-question structured interview
- Empathetic, progressive questioning
- Session transcript recording

### 3. Support Chat
- Context-aware responses
- Voice mode with audio input/output
- Knowledge base integration
- Personalized advice based on therapy session

### 4. Session Summary
- Profile review
- Session statistics
- Key takeaways and recommendations
- Feedback collection

## Voice Features

- **Speech Recognition**: Uses Google Speech Recognition API
- **Text-to-Speech**: Google Text-to-Speech (gTTS)
- **Audio Recording**: Built-in Streamlit audio recorder
- **Autoplay Support**: JavaScript-enhanced audio playback

## Memory Management

The application uses Mem0 for:
- Maintaining conversation context
- Storing user responses
- Enabling personalized interactions
- Cross-session information retention

## Security and Privacy

- All conversations are kept confidential
- User can choose what information to share
- Session data can be cleared at any time
- Crisis resources are prominently displayed

## Limitations

- Knowledge base limited to provided PDF documents
- Voice recognition requires internet connection
- Response quality depends on knowledge base content
- Not a replacement for professional mental health care

## Crisis Resources

The application prominently displays crisis resources:
- National Suicide Prevention Lifeline: 988
- Crisis Text Line: Text HOME to 741741
- Emergency Services: 911

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Specify your license here]

## Disclaimer

This application is designed to provide supportive conversations and is not a substitute for professional mental health care. Users experiencing mental health emergencies should contact appropriate crisis services or healthcare providers immediately.

## Support

For technical issues or questions about the application, please open an issue in the repository.

## Acknowledgments

- CrewAI team for the multi-agent framework
- Streamlit for the web interface
- Mem0 for memory management capabilities
- Contributors and mental health professionals who provided guidance
