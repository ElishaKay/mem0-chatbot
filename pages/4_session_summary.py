import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Session Summary",
    page_icon="📋",
    layout="wide",
)

# Check if user has completed a session
if 'therapy_session_data' not in st.session_state:
    st.warning("No session data found. Please complete a session first.")
    if st.button("Go to Home"):
        st.switch_page("app.py")
else:
    st.title("Session Summary")
    st.markdown("Thank you for using our Mental Health Support Chat. Here's a summary of your session.")
    
    # Create columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 👤 Your Profile")
        if st.session_state.get('user_data'):
            user_data = st.session_state.user_data
            profile_data = {
                "Field": ["Name", "Age Group", "Current Mood", "Concerns", "Preferred Style"],
                "Information": [
                    user_data.get('name', 'Not provided'),
                    user_data.get('age_group', 'Not provided'),
                    user_data.get('mood', 'Not provided'),
                    ', '.join(user_data.get('concerns', [])) or 'None specified',
                    user_data.get('preferred_style', 'Not provided')
                ]
            }
            df_profile = pd.DataFrame(profile_data)
            st.table(df_profile)
    
    with col2:
        st.markdown("### 📊 Session Statistics")
        stats_data = {
            "Metric": [
                "Therapy Questions Answered",
                "Chat Messages Exchanged",
                "Session Duration",
                "Support Topics Discussed"
            ],
            "Value": [
                f"{st.session_state.get('question_count', 0)} questions",
                f"{len(st.session_state.get('messages', []))} messages",
                "Completed",
                len(st.session_state.get('user_data', {}).get('concerns', []))
            ]
        }
        df_stats = pd.DataFrame(stats_data)
        st.table(df_stats)
    
    st.markdown("---")
    
    # Therapy Session Summary
    st.markdown("### 🗣️ Therapy Session Insights")
    if st.session_state.get('therapy_transcript'):
        with st.expander("View Therapy Conversation", expanded=False):
            for entry in st.session_state.therapy_transcript:
                if entry.startswith("Therapist:"):
                    st.markdown(f"**{entry}**")
                else:
                    st.markdown(f"_{entry}_")
    
    # Key Takeaways
    st.markdown("### 💡 Key Takeaways")
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("#### What We Discussed")
        if st.session_state.get('user_data', {}).get('concerns'):
            for concern in st.session_state.user_data['concerns']:
                st.markdown(f"- {concern}")
        else:
            st.markdown("- General mental health support")
    
    with col4:
        st.markdown("#### Recommended Next Steps")
        st.markdown("- Practice the coping strategies discussed")
        st.markdown("- Maintain regular self-care routines")
        st.markdown("- Consider professional support if needed")
        st.markdown("- Return for follow-up sessions as needed")
    
    st.markdown("---")
    
    # Resources and Reminders
    st.markdown("### 📚 Resources & Reminders")
    
    col5, col6 = st.columns(2)
    
    with col5:
        st.markdown("#### Self-Care Reminders")
        st.markdown("""
        - Take breaks when feeling overwhelmed
        - Practice mindfulness or meditation
        - Maintain healthy sleep habits
        - Stay connected with supportive people
        - Engage in activities you enjoy
        """)
    
    with col6:
        st.markdown("#### Crisis Resources")
        st.markdown("""
        **If you're in crisis, please reach out:**
        - National Suicide Prevention Lifeline: 988
        - Crisis Text Line: Text HOME to 741741
        - Emergency Services: 911
        
        *These resources are available 24/7*
        """)
    
    st.markdown("---")
    
    # Feedback Section
    st.markdown("### 📝 Session Feedback")
    st.markdown("Your feedback helps us improve our service.")
    
    feedback_col1, feedback_col2 = st.columns(2)
    
    with feedback_col1:
        helpful_rating = st.select_slider(
            "How helpful was this session?",
            options=["Not Helpful", "Somewhat Helpful", "Helpful", "Very Helpful", "Extremely Helpful"],
            value="Helpful"
        )
    
    with feedback_col2:
        likelihood_return = st.select_slider(
            "How likely are you to return?",
            options=["Very Unlikely", "Unlikely", "Neutral", "Likely", "Very Likely"],
            value="Likely"
        )
    
    feedback_text = st.text_area("Any additional feedback or suggestions?", height=100)
    
    if st.button("Submit Feedback"):
        st.success("Thank you for your feedback!")
        # In a real app, you would save this feedback
    
    st.markdown("---")
    
    # Action Buttons
    st.markdown("### What would you like to do next?")
    
    col7, col8, col9 = st.columns(3)
    
    with col7:
        if st.button("Start New Session", type="primary"):
            # Clear existing session data but keep user profile
            user_data = st.session_state.get('user_data', {})
            for key in list(st.session_state.keys()):
                if key != 'user_data':
                    del st.session_state[key]
            st.session_state.user_data = user_data
            st.switch_page("pages/1_user_input.py")
    
    with col8:
        if st.button("Return to Chat"):
            st.switch_page("pages/3_chatbot.py")
    
    with col9:
        if st.button("Exit Application"):
            # Clear all session data
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.switch_page("app.py")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>Thank you for trusting us with your mental health journey.</p>
            <p>Remember: It's okay to ask for help, and you're not alone.</p>
        </div>
        """,
        unsafe_allow_html=True
    )