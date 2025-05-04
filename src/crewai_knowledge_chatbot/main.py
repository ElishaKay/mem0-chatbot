#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from crewai_knowledge_chatbot.crew import CrewaiKnowledgeChatbot
from mem0 import MemoryClient

client = MemoryClient()

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="chromadb")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="mem0")
warnings.filterwarnings("ignore", message=".*'model_fields' attribute.*")
warnings.filterwarnings("ignore", message=".*output_format='v1.0' is deprecated.*")

def conduct_therapy_session(crew_instance, initial_message, history):
    """
    Conducts a therapy session by having the therapist ask questions
    and collecting user responses.
    """
    session_transcript = []
    current_history = history.copy()
    
    # Initial message from user
    session_transcript.append(f"User: {initial_message}")
    current_history.append(f"User: {initial_message}")
    
    # Start therapy session
    print("Therapist: Let me understand your situation better...")
    
    # First therapist response
    inputs = {
        "user_message": initial_message,
        "history": "\n".join(current_history),
    }
    
    # Get therapist's first response/questions
    therapist_response = crew_instance.tasks[0].execute(inputs)
    
    # Extract questions from therapist response
    questions = extract_questions(therapist_response)
    
    for i, question in enumerate(questions):
        print(f"Therapist: {question}")
        session_transcript.append(f"Therapist: {question}")
        
        user_response = input("You: ")
        session_transcript.append(f"User: {user_response}")
        current_history.append(f"Therapist: {question}")
        current_history.append(f"User: {user_response}")
        
        # Add to memory
        client.add(user_response, user_id="User")
    
    return "\n".join(session_transcript), current_history

def extract_questions(therapist_response):
    """
    Extract individual questions from therapist response.
    This is a simple implementation - you might want to make it more sophisticated.
    """
    lines = therapist_response.split('\n')
    questions = [line.strip() for line in lines if line.strip().endswith('?')]
    return questions[:7]  # Limit to maximum 7 questions

def run():
    history = []
    """
    Run the crew.
    """
    print("Mental Health Support Chatbot")
    print("Type 'exit', 'quit', or 'bye' to end the conversation")
    print("-" * 50)
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Chatbot: Thank you for sharing with me today. Take care of yourself, and remember that seeking help is a sign of strength.")
            break
        
        # Create crew instance
        crew_instance = CrewaiKnowledgeChatbot().crew()
        
        # Conduct therapy session
        print("\nStarting therapy session...\n")
        therapy_transcript, updated_history = conduct_therapy_session(
            crew_instance, 
            user_input, 
            history
        )
        
        # Update history
        history = updated_history
        
        print("\nProcessing your information to find the best resources...\n")
        
        # Prepare inputs for the full crew execution
        inputs = {
            "user_message": user_input,
            "history": "\n".join(history),
            "therapy_session_output": therapy_transcript,
        }
        
        # Execute the remaining tasks
        try:
            result = crew_instance.kickoff(inputs=inputs)
            
            # The final output will be the summary from the last task
            final_response = result.tasks_output[-1].raw
            
            # Display the final response
            print("\n" + "="*50)
            print("Mental Health Support Response:")
            print("="*50)
            print(final_response)
            print("="*50 + "\n")
            
            # Update history with the final interaction
            history.append(f"Assistant: {final_response}")
            
        except Exception as e:
            print(f"An error occurred: {e}")
            print("I apologize for the technical difficulty. Please try again or seek professional help if urgent.")
        
        # Option to continue or end session
        continue_session = input("\nWould you like to discuss another concern? (yes/no): ")
        if continue_session.lower() not in ["yes", "y"]:
            print("\nChatbot: Thank you for trusting me with your concerns. Remember, professional help is always available if you need it. Take care!")
            break

if __name__ == "__main__":
    run()