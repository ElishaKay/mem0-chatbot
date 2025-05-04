import streamlit as st
import sys
import os
from dotenv import load_dotenv
import speech_recognition as sr
from gtts import gTTS
import tempfile
import io
from io import BytesIO
import base64
import streamlit.components.v1 as components
import time
from audiorecorder import audiorecorder

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import your CrewAI chatbot
from src.crewai_knowledge_chatbot.crew import CrewaiKnowledgeChatbot

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Mental Health Support Chat",
    page_icon="💬",
    layout="wide",
)

# Add JavaScript for better autoplay support
st.markdown("""
<script>
// Function to enable audio autoplay
function enableAudioAutoplay() {
    // Create an AudioContext
    if (typeof window.audioContext === 'undefined') {
        window.audioContext = new (window.AudioContext || window.webkitAudioContext)();
    }
    
    // Resume the audio context on user interaction
    document.addEventListener('click', function() {
        if (window.audioContext.state !== 'running') {
            window.audioContext.resume();
        }
    }, { once: true });
}

// Function to play audio
function playAudio(audioId) {
    const audio = document.getElementById(audioId);
    if (audio) {
        // Try to play with a promise
        const playPromise = audio.play();
        
        if (playPromise !== undefined) {
            playPromise.then(() => {
                console.log('Audio playback started successfully');
            }).catch((error) => {
                console.log('Audio playback failed:', error);
                // Fallback: show the audio controls
                audio.controls = true;
            });
        }
    }
}

// Enable autoplay when the page loads
window.addEventListener('load', enableAudioAutoplay);
</script>
""", unsafe_allow_html=True)

# Add CSS
st.markdown("""
<style>
.chat-message {
    padding: 1rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
    flex-direction: row;
    align-items: flex-start;
}
.chat-message .avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    margin-right: 1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
}
.chat-message .user-avatar {
    background-color: #6c757d;
    color: white;
}
.chat-message .assistant-avatar {
    background-color: #6c757d;
    color: white;
}
.chat-message .content {
    flex-grow: 1;
    padding-left: 0.5rem;
}
.chat-message-text {
    margin-bottom: 0;
}
.audio-recorder {
    padding: 1rem;
    border-radius: 0.5rem;
    background-color: #f8f9fa;
    margin: 1rem 0;
}
.hidden-audio {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "voice_mode" not in st.session_state:
    st.session_state.voice_mode = False
if "last_audio_input" not in st.session_state:
    st.session_state.last_audio_input = None
if "processed_audio" not in st.session_state:
    st.session_state.processed_audio = True
if "user_has_interacted" not in st.session_state:
    st.session_state.user_has_interacted = False

# Audio helper functions
def transcribe_audio(audio_bytes):
    """Convert audio bytes to text using speech recognition"""
    try:
        recognizer = sr.Recognizer()
        
        # Create a temporary file with the audio data
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
            # If audio_bytes is already bytes, write directly
            if isinstance(audio_bytes, bytes):
                temp_audio.write(audio_bytes)
            # If it's a BytesIO object, get the value
            elif isinstance(audio_bytes, BytesIO):
                temp_audio.write(audio_bytes.getvalue())
            # If it's an AudioSegment, export to the temp file
            elif hasattr(audio_bytes, 'export'):
                audio_bytes.export(temp_audio.name, format='wav')
            else:
                temp_audio.write(audio_bytes)
            
            temp_audio_path = temp_audio.name
        
        # Convert audio file to text using Google Speech Recognition
        with sr.AudioFile(temp_audio_path) as source:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
        
        # Clean up temporary file
        os.unlink(temp_audio_path)
        
        return text
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand the audio."
    except sr.RequestError as e:
        return f"Sorry, there was an error with the speech recognition service: {str(e)}"
    except Exception as e:
        return f"Error transcribing audio: {str(e)}"

def text_to_speech(text):
    """Convert text to speech audio"""
    try:
        # Ensure text is a string
        if not isinstance(text, str):
            text = str(text)
        
        tts = gTTS(text=text, lang='en', slow=False)
        
        # Create a BytesIO object to store the audio
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        return audio_buffer.getvalue()
    except Exception as e:
        st.error(f"Error generating speech: {str(e)}")
        return None

def create_autoplay_audio(audio_bytes):
    """Create an HTML audio element with autoplay capabilities"""
    # Convert audio to base64
    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
    
    # Generate a unique ID for this audio element
    audio_id = f"audio_{int(time.time() * 1000)}"
    
    # Create the HTML with autoplay
    audio_html = f"""
    <audio id="{audio_id}" style="display: none;">
        <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
    </audio>
    <script>
        // Wait for the audio element to be ready
        setTimeout(function() {{
            playAudio('{audio_id}');
        }}, 100);
    </script>
    """
    
    return audio_html

def process_message(user_input):
    """Process user input through the chatbot"""
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.chat_history.append(f"User: {user_input}")
    
    # Prepare comprehensive context
    full_context = ""
    
    # Add user profile data
    if st.session_state.get('user_data'):
        user_data = st.session_state.user_data
        full_context += f"""User Profile:
        - Name: {user_data.get('name', 'Not provided')}
        - Age Group: {user_data.get('age_group', 'Not provided')}
        - Current Mood: {user_data.get('mood', 'Not provided')}
        - Concerns: {', '.join(user_data.get('concerns', [])) or 'None'}
        - Preferred Style: {user_data.get('preferred_style', 'Not provided')}
        - Additional Info: {user_data.get('additional_info', 'None')}
        
        """
    
    # Add therapy session context
    if st.session_state.get('therapy_session_data'):
        therapy_data = st.session_state.therapy_session_data
        full_context += f"""Therapy Session Summary:
        {chr(10).join(therapy_data.get('transcript', []))}
        
        """
    
    # Add conversation history
    full_context += f"""Current Conversation:
    {chr(10).join(st.session_state.chat_history)}"""
    
    # Process with CrewAI chatbot crew
    inputs = {
        "user_message": user_input,
        "full_context": full_context
    }
    
    try:
        # Get response from CrewAI
        crew_output = CrewaiKnowledgeChatbot().chatbot_crew().kickoff(inputs=inputs)
        
        # Extract the final response (from the last task output)
        if hasattr(crew_output, 'tasks_output') and crew_output.tasks_output:
            # Get the last task output (summary task)
            final_task_output = crew_output.tasks_output[-1]
            if hasattr(final_task_output, 'raw'):
                response = final_task_output.raw
            else:
                response = str(final_task_output)
        elif hasattr(crew_output, 'raw'):
            response = crew_output.raw
        else:
            response = str(crew_output)
        
        # Update history
        st.session_state.chat_history.append(f"Assistant: {response}")
        
        # Add assistant response to messages
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        return response
    except Exception as e:
        error_message = f"I apologize, but I encountered an error: {str(e)}. Please try again."
        st.session_state.messages.append({"role": "assistant", "content": error_message})
        return error_message

# Check if user has completed therapy session
if 'therapy_session_data' not in st.session_state:
    st.warning("Please complete the therapy session first.")
    if st.button("Go to Therapy Session"):
        st.switch_page("pages/2_therapy_session.py")
else:
    # Sidebar content
    with st.sidebar:
        # Add chat settings section at the top of sidebar
        st.title("Chat Settings")
        st.session_state.voice_mode = st.toggle("🎤 Voice Mode", value=st.session_state.voice_mode)
        
        if st.session_state.voice_mode:
            st.info("🔊 Voice Active")
        else:
            st.info("⌨️ Text Mode")
        
        # Add instructions on how to use the Voice mode
        with st.expander("**ℹ️ How to use Voice Mode:**"):
            st.markdown("""
                        1. Toggle **Voice Mode** on
                        2. Click the **microphone button** to start recording
                        3. Speak your message clearly
                        4. Click the **stop button** when finished
                        5. Your message will be transcribed and sent to the chatbot
                        6. The chatbot's response will be played as audio automatically
                        **Note:** Make sure your browser has permission to access your microphone.
                    """)
        
        with st.expander("**👤 User Profile**"):
            if st.session_state.get('user_data'):
                user_data = st.session_state.user_data
                st.markdown(f"**Name:** {user_data.get('name', 'Anonymous')}")
                st.markdown(f"**Age Group:** {user_data.get('age_group', 'Prefer not to say')}")
                st.markdown(f"**Mood:** {user_data.get('mood', 'Not specified')}")
                st.markdown(f"**Concerns:** {', '.join(user_data.get('concerns', [])) or 'None specified'}")
                st.markdown(f"**Additional Information:** {user_data.get('additional_info', '')}")
                st.markdown(f"**Chatbot Tone Preference:** {user_data.get('preferred_style', 'Supportive and empathetic')}")

        st.divider()
        
        st.markdown("### Session Actions")
        
        if st.button("🔄 Clear Current Chat", help="Clear this conversation but stay in session"):
            st.session_state.messages = []
            st.session_state.chat_history = []
            st.session_state.last_audio_input = None
            st.session_state.processed_audio = True
            st.rerun()
        
        if st.button("🏁 End Session", type="primary", help="End session and view summary"):
            st.switch_page("pages/4_session_summary.py")

    # Main chat interface
    st.title("Mental Health Support Chat")
    st.markdown("Based on our therapy session, I'm here to provide you with personalized support and resources.")

    # Display chat messages
    for message in st.session_state.messages:
        avatar = "💭" if message["role"] == "user" else "🤖"
        avatar_class = "user-avatar" if message["role"] == "user" else "assistant-avatar"
        message_class = "user" if message["role"] == "user" else "assistant"
        
        st.markdown(f"""
        <div class="chat-message {message_class}">
            <div class="avatar {avatar_class}">{avatar}</div>
            <div class="content">
                <p class="chat-message-text">{message["content"]}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Add audio playback for assistant messages if voice mode is enabled
        if st.session_state.voice_mode and message["role"] == "assistant":
            audio_bytes = text_to_speech(message["content"])
            if audio_bytes:
                st.audio(audio_bytes, format='audio/mp3')

    # Input area
    if st.session_state.voice_mode:
        # Add an interaction button to enable audio context
        if not st.session_state.user_has_interacted:
            if st.button("🎙️ Start Voice Conversation"):
                st.session_state.user_has_interacted = True
                st.rerun()
            st.info("Click the button above to enable voice interaction")
        else:
            # Voice input using audiorecorder
            # Audio recorder
            audio_segment = audiorecorder("Start sharing your thoughts", "Click to stop")
            
            if audio_segment:
                # Convert AudioSegment to bytes for Streamlit
                audio_buffer = io.BytesIO()
                audio_segment.export(audio_buffer, format="wav")
                audio_bytes = audio_buffer.getvalue()
                
                # Check if we have new audio
                if audio_bytes != st.session_state.last_audio_input:
                    st.session_state.last_audio_input = audio_bytes
                    st.session_state.processed_audio = False
                
                # Process unprocessed audio
                if not st.session_state.processed_audio:
                    # Show the audio player
                    st.audio(audio_bytes, format="audio/wav")
                    
                    # Transcribe audio
                    with st.spinner("Transcribing..."):
                        user_input = transcribe_audio(audio_bytes)
                    
                    if user_input and not user_input.startswith("Sorry"):
                        st.success(f"You said: {user_input}")
                        
                        # Mark audio as processed
                        st.session_state.processed_audio = True
                        
                        # Process the transcribed text
                        with st.spinner("Thinking..."):
                            response = process_message(user_input)
                        
                        # Generate and play response audio with autoplay
                        response_audio = text_to_speech(response)
                        if response_audio:
                            # Create autoplay audio element
                            audio_html = create_autoplay_audio(response_audio)
                            components.html(audio_html, height=0)
                            
                            # Also provide a visible audio player as fallback
                            st.markdown("**Assistant's Response:**")
                            st.audio(response_audio, format='audio/mp3')
                        
                        # Force a rerun to update the UI
                        time.sleep(0.5)  # Small delay to ensure audio starts playing
                        st.rerun()
                    else:
                        st.error(user_input)
                        st.session_state.processed_audio = True
    
    else:
        # Text input
        user_input = st.chat_input("How can I help you today?")
        
        if user_input:
            # Process message
            with st.spinner("Thinking..."):
                response = process_message(user_input)
            
            # Force a rerun to update the UI
            st.rerun()