import streamlit as st
import sys
import os
from mem0 import MemoryClient

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.crewai_knowledge_chatbot.crew import CrewaiKnowledgeChatbot

# Initialize memory client
client = MemoryClient()

st.set_page_config(
    page_title="Therapy Session",
    page_icon="🗣️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Initialize session state
if 'therapy_messages' not in st.session_state:
    st.session_state.therapy_messages = []
if 'therapy_complete' not in st.session_state:
    st.session_state.therapy_complete = False
if 'current_question' not in st.session_state:
    st.session_state.current_question = None
if 'question_count' not in st.session_state:
    st.session_state.question_count = 0
if 'therapy_transcript' not in st.session_state:
    st.session_state.therapy_transcript = []
if 'initial_context' not in st.session_state:
    st.session_state.initial_context = None

# Check if user has completed basic info
if 'user_data' not in st.session_state or not st.session_state.user_data:
    st.warning("Please provide your information on the User Input page first.")
    if st.button("Go to User Input Page"):
        st.switch_page("pages/1_user_input.py")
else:
    st.title("Therapy Session")
    st.markdown("I'd like to understand your situation better. Please take your time answering these questions.")

    # Create initial context if not already created
    if st.session_state.initial_context is None:
        user_data = st.session_state.user_data
        st.session_state.initial_context = f"""
        User Profile:
        - Name: {user_data.get('name', 'Not provided')}
        - Age Group: {user_data.get('age_group', 'Not provided')}
        - Current Mood: {user_data.get('mood', 'Not provided')}
        - Concerns: {', '.join(user_data.get('concerns', [])) or 'None'}
        - Additional Info: {user_data.get('additional_info', 'None')}
        """

    # Display chat messages
    for message in st.session_state.therapy_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Generate first question if not already done
    if st.session_state.question_count == 0 and not st.session_state.current_question:
        # Generate first question
        with st.spinner("Preparing questions..."):
            try:
                crew_instance = CrewaiKnowledgeChatbot().therapy_crew()
                inputs = {
                    "user_context": st.session_state.initial_context,
                    "conversation_history": "",
                    "question_number": "1"
                }
                result = crew_instance.kickoff(inputs=inputs)
                
                # Extract the question from the result
                if hasattr(result, 'raw'):
                    question = result.raw
                else:
                    question = str(result)
                
                st.session_state.current_question = question
                st.session_state.therapy_messages.append({"role": "assistant", "content": question})
                st.session_state.therapy_transcript.append(f"Therapist: {question}")
                st.rerun()
            except Exception as e:
                st.error(f"Error generating question: {e}")

    # Display input field if there's a current question
    if st.session_state.current_question and not st.session_state.therapy_complete:
        user_response = st.chat_input("Your response...")
        
        if user_response:
            # Add user response to messages
            st.session_state.therapy_messages.append({"role": "user", "content": user_response})
            st.session_state.therapy_transcript.append(f"User: {user_response}")
            
            # Store in memory
            client.add(user_response, user_id="User")
            
            # Increment question count
            st.session_state.question_count += 1
            
            # Check if we've reached the maximum number of questions (7)
            if st.session_state.question_count >= 4:
                st.session_state.therapy_complete = True
                
                # Store the complete therapy session in session state
                st.session_state.therapy_session_data = {
                    "transcript": st.session_state.therapy_transcript,
                    "user_data": st.session_state.user_data,
                    "timestamp": os.environ.get('CURRENT_TIMESTAMP', 'Unknown')
                }
                
                st.session_state.therapy_messages.append({
                    "role": "assistant", 
                    "content": "Thank you for sharing with me. I now have a better understanding of your situation. Let's proceed to get you the support you need."
                })
                st.rerun()
            else:
                # Generate next question
                with st.spinner("Thinking..."):
                    try:
                        crew_instance = CrewaiKnowledgeChatbot().therapy_crew()
                        conversation_history = "\n".join(st.session_state.therapy_transcript)
                        inputs = {
                            "user_context": st.session_state.initial_context,
                            "conversation_history": conversation_history,
                            "question_number": str(st.session_state.question_count + 1)
                        }
                        result = crew_instance.kickoff(inputs=inputs)
                        
                        if hasattr(result, 'raw'):
                            question = result.raw
                        else:
                            question = str(result)
                        
                        st.session_state.current_question = question
                        st.session_state.therapy_messages.append({"role": "assistant", "content": question})
                        st.session_state.therapy_transcript.append(f"Therapist: {question}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error generating next question: {e}")

    # Show completion options
    if st.session_state.therapy_complete:
        st.success("Therapy session completed!")
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("View Session Summary", type="secondary"):
                with st.expander("Session Summary", expanded=True):
                    st.markdown("### Your Information")
                    user_data = st.session_state.user_data
                    st.markdown(f"**Name:** {user_data.get('name', 'Not provided')}")
                    st.markdown(f"**Age Group:** {user_data.get('age_group', 'Not provided')}")
                    st.markdown(f"**Mood:** {user_data.get('mood', 'Not provided')}")
                    st.markdown(f"**Concerns:** {', '.join(user_data.get('concerns', [])) or 'None'}")
                    
                    st.markdown("### Therapy Session Transcript")
                    for entry in st.session_state.therapy_transcript:
                        st.markdown(entry)
        
        with col2:
            if st.button("Continue to Support Chat", type="primary"):
                st.switch_page("pages/3_chatbot.py")