from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource

# Create a PDF knowledge source
pdf_source = PDFKnowledgeSource(
    file_paths=["first_resource.pdf", "second_resource.pdf", "third_resource.pdf"], 
    name="mental health knowledge base",
    description="Authorized mental health resource containing approved information"
)

memory_config = {
    "provider": "mem0",
    "config": {"user_id": "User"},
}

@CrewBase
class CrewaiKnowledgeChatbot():
    """CrewaiKnowledgeChatbot crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def therapist(self) -> Agent:
        """Agent 1: Therapist for understanding user's condition"""
        return Agent(
            config=self.agents_config['therapist'],
            memory=True,
            memory_config=memory_config,
            verbose=False,
        )

    @agent
    def knowledge_specialist(self) -> Agent:
        """Agent 2: Searches knowledge base for mental health information"""
        return Agent(
            config=self.agents_config['knowledge_specialist'],
            memory=True,
            memory_config=memory_config,
            verbose=False,
        )

    @agent
    def summarizer(self) -> Agent:
        """Agent 3: Creates digestible information for the user"""
        return Agent(
            config=self.agents_config['summarizer'],
            memory=True,
            memory_config=memory_config,
            verbose=False,
        )

    @task
    def therapy_question_task(self) -> Task:
        """Task for generating therapy questions"""
        return Task(
            config=self.tasks_config["therapy_question_task"],
        )

    @task
    def knowledge_search_task(self) -> Task:
        """Task for searching knowledge base"""
        return Task(
            config=self.tasks_config["knowledge_search_task"],
        )

    @task
    def summary_task(self) -> Task:
        """Task for creating final summary"""
        return Task(
            config=self.tasks_config["summary_task"],
            context=[self.knowledge_search_task()],
        )

    @crew
    def therapy_crew(self) -> Crew:
        """Creates the therapy session crew"""
        return Crew(
            agents=[self.therapist()],
            tasks=[self.therapy_question_task()],
            process=Process.sequential,
            verbose=False,
        )

    @crew
    def chatbot_crew(self) -> Crew:
        """Creates the main chatbot crew"""
        return Crew(
            agents=[self.knowledge_specialist(), self.summarizer()],
            tasks=[self.knowledge_search_task(), self.summary_task()],
            process=Process.sequential,
            knowledge_sources=[pdf_source],
            verbose=False,
        )