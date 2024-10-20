from agents import CompanyResearchAgents
from job_manager import append_event
from tasks import CompanyResearchTasks
from crewai import Crew


class CompanyResearchCrew:
  def __init__(self, job_id: str):
    self.job_id = job_id
    self.crew = None
    
  def setup_crew(self, companies: list[str], positions: list[str]):
    print(f"Setting up crew for {self.job_id} with companies {companies} and positions {positions}")    

    # SETUP AGENTS
    agents = CompanyResearchAgents()
    reseach_manager = agents.reseach_manager(companies, positions)
    company_research_agent = agents.company_research_agent()    
    
    # SETUP TASKS
    task = CompanyResearchTasks(job_id=self.job_id)
    company_research_task = [
      task.company_research(company_research_agent, company, positions) for company in companies
    ]
    
    manage_task = task.manage_research(reseach_manager, companies, positions, company_research_task)
    
    # CREATE CREW
    self.crew = Crew(
      agents=[reseach_manager, company_research_agent],
      tasks=[*company_research_task, manage_task],
      verbose=2
    )
    

  def kickoff(self):
    if not self.crew:
      print("Crew not setup")
      return
    
    append_event(self.job_id, "CREW_STARTED")
    
    try:
      print(f"Running crew for {self.job_id}")
      results = self.crew.kickoff()
      append_event(self.job_id, "CREW COMPLETED")
      return results
    
    except Exception as e:
      print(f"CREW FAILED: {e}")
      return str(e)    
      