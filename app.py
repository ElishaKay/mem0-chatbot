import streamlit as st

st.set_page_config(
    page_title="Mental Health Chatbot",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("Mental Health Support Application")
st.markdown("""
## Welcome and thanks for taking the step towards your Mental Health!

This application is designed to provide supportive conversations through a structured process:

#### How it works:
1. **Step 1**: Provide your basic information
2. **Step 2**: Complete a therapy session with our AI therapist
3. **Step 3**: Get personalized support based on your needs

### Our Approach:
- We start with understanding your basic information and preferences
- Our AI therapist conducts a gentle, structured interview to better understand your situation
- Based on all the information gathered, our support chat provides personalized mental health resources and guidance

""")

# Add navigation button
if st.button("🚀 Get Started", type="primary"):
    st.switch_page("pages/1_user_input.py")

# Add information about privacy and process
st.markdown("---")
st.markdown("""
### Your Privacy Matters
- All information is kept confidential
- You can choose what to share
- Our AI is designed to be supportive and non-judgmental

### The Process
1. **Basic Information**: Tell us about yourself and your preferences
2. **Therapy Session**: Answer 7 thoughtful questions from our AI therapist
3. **Support Chat**: Get personalized help based on your complete profile

Don't worry - you can take your time at each step.
""")

#Add information about Technical implementation of the chatbot
st.markdown("""
### Technical Implementation Details

**Multi-Agent System:**
- **Therapist Agent**: Conducts structured interviews with empathetic questioning
- **Knowledge Specialist**: Searches our mental health knowledge base for relevant information
- **Summarizer Agent**: Creates personalized, actionable responses based on your context

**Knowledge Base:**
For this demo, we use PDF documents containing mental health resources. The system searches these documents to find information relevant to your specific needs.

**Memory System:**
We use Mem0 to maintain context throughout your session, ensuring personalized and coherent support.
""")