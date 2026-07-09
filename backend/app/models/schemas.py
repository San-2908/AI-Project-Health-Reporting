from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ProjectStatus(BaseModel):
    rag_score: str
    confidence: int
    summary: str
    top_risks: List[str]
    recommended_actions: List[str]
    reasoning: str

class ProjectData(BaseModel):
    project_name: str
    tasks_completed: int = 0
    total_tasks: int = 0
    completion_percentage: float = 0.0
    schedule_variance: float = 0.0
    budget_variance: float = 0.0
    milestones_at_risk: int = 0
    total_milestones: int = 0
    blockers_count: int = 0
    stakeholder_sentiment: str = "Neutral"
    status: Optional[ProjectStatus] = None

class PortfolioReport(BaseModel):
    portfolio_health: str
    common_trends: List[str]
    escalations: List[str]
    recurring_blockers: List[str]
    budget_observations: str
    resource_constraints: str
    recommendations: List[str]

