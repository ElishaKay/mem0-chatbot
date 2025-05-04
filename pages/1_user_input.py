import streamlit as st

st.set_page_config(
    page_title="User Information",
    page_icon="📝",
    layout="wide",
)

st.title("Step 1: Tell Us About Yourself")
st.markdown("Please provide some basic information to help personalize your experience.")

# Initialize session state for user data
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

with st.form("user_info_form"):
    st.subheader("Personal Information")
    
    # User inputs
    name = st.text_input("What's your name? (Optional)", 
                        value=st.session_state.user_data.get('name', ''))
    
    age_group = st.selectbox(
        "Age Group",
        ["Prefer not to say", "Under 18", "18-25", "26-35", "36-50", "51-65", "Over 65"],
        index=["Prefer not to say", "Under 18", "18-25", "26-35", "36-50", "51-65", "Over 65"]
              .index(st.session_state.user_data.get('age_group', 'Prefer not to say'))
    )
    
    st.subheader("How are you feeling today?")
    
    mood = st.select_slider(
        "Current Mood",
        options=["Very Low", "Low", "Neutral", "Good", "Very Good"],
        value=st.session_state.user_data.get('mood', 'Neutral')
    )
    
    concerns = st.multiselect(
        "What would you like to discuss today?",
        ["Stress", "Anxiety", "Depression", "Sleep Issues", "Relationships", 
         "Work/School", "Self-esteem", "Other"],
        default=st.session_state.user_data.get('concerns', [])
    )
    
    additional_info = st.text_area(
        "Is there anything specific you'd like to share before we begin?",
        value=st.session_state.user_data.get('additional_info', ''),
        height=100
    )
    
    preferred_style = st.radio(
        "How would you prefer the conversation style?",
        ["Supportive and empathetic", "Direct and solution-focused", "Educational and informative"],
        index=["Supportive and empathetic", "Direct and solution-focused", "Educational and informative"]
              .index(st.session_state.user_data.get('preferred_style', 'Supportive and empathetic'))
    )
    
    submitted = st.form_submit_button("Save and Continue")
    
    if submitted:
        # Store user data in session state
        st.session_state.user_data = {
            'name': name,
            'age_group': age_group,
            'mood': mood,
            'concerns': concerns,
            'additional_info': additional_info,
            'preferred_style': preferred_style
        }
        
        st.session_state.form_submitted = True
        st.success("Information saved! Redirecting to therapy session...")
        
        # Navigate to therapy session page
        st.switch_page("pages/2_therapy_session.py")

# Display saved information (only shows if not redirected)
if st.session_state.get('form_submitted', False) and not submitted:
    st.divider()
    st.subheader("Your Information")
    st.write("Your information has been saved. You can now proceed to the therapy session.")
    
    with st.expander("View your information"):
        st.json(st.session_state.user_data)
    
    # Add manual navigation button
    if st.button("Continue to Therapy Session"):
        st.switch_page("pages/2_therapy_session.py")

with st.sidebar:
        # Add information about next steps
        st.title("What Happens Next?")
        st.markdown("""
                    After you submit this form, you'll proceed to:
                    1. **Therapy Session**: Our AI therapist will ask you a few questions to better understand your situation
                    2. **Support Chat**: You'll have access to personalized support based on your complete profile
                    All information is used to provide more relevant and helpful support.
        """)