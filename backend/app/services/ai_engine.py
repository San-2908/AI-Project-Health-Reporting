from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from app.models.schemas import ProjectData, ProjectStatus
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

def calculate_rag_score(data: ProjectData) -> str:
    # Schedule = 25%, Budget = 20%, Milestones = 20%, Task Completion = 15%, Blockers = 10%, Stakeholder = 10%
    score = 100
    
    # Simple naive calculation for assignment scope
    if data.completion_percentage == 0:
        score -= 25 # Force to AMBER if not started
    elif data.completion_percentage < 50:
        score -= 15
    
    if data.milestones_at_risk > 0:
        score -= (data.milestones_at_risk * 5)
        
    if data.blockers_count > 0:
        score -= (data.blockers_count * 10)

    if score > 80:
        return "GREEN"
    elif score > 60:
        return "AMBER"
    else:
        return "RED"

async def generate_project_status(data: ProjectData) -> ProjectStatus:
    rag_score = calculate_rag_score(data)
    
    if not settings.OPENROUTER_API_KEY:
        logger.warning("OPENROUTER_API_KEY not set. Using mock AI response.")
        return ProjectStatus(
            rag_score=rag_score,
            confidence=85,
            summary="Mock summary: Project is proceeding as expected.",
            top_risks=["Mock risk: Resource constraint"],
            recommended_actions=["Mock action: Monitor closely"],
            reasoning=f"Mock reasoning: Calculated RAG score is {rag_score} based on {data.blockers_count} blockers."
        )
        
    try:
        llm = ChatOpenAI(
            model="google/gemini-2.5-flash",
            api_key=settings.OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
            temperature=0.2,
            max_tokens=1000
        )
        
        prompt = PromptTemplate(
            input_variables=["project_name", "rag_score", "completion", "blockers", "milestones"],
            template="""You are a Senior PMO Director analyzing a project. 
Project Name: {project_name}
Calculated RAG Score: {rag_score}
Completion: {completion}%
Blockers: {blockers}
Milestones at Risk: {milestones}

Based on these metrics, provide a JSON response with the following keys:
- "confidence": integer from 0 to 100 representing confidence in this assessment
- "summary": A brief executive summary (2 sentences max)
- "top_risks": A list of 2-3 top risks (strings)
- "recommended_actions": A list of 2-3 recommended actions (strings)
- "reasoning": A detailed explanation of WHY the project received this RAG score.

Ensure the output is ONLY valid JSON. Do NOT wrap it in markdown backticks.
"""
        )
        
        chain = prompt | llm
        response = await chain.ainvoke({
            "project_name": data.project_name,
            "rag_score": rag_score,
            "completion": data.completion_percentage,
            "blockers": data.blockers_count,
            "milestones": data.milestones_at_risk
        })
        
        import json
        import re
        
        # Clean potential markdown from response
        content = response.content.strip()
        if content.startswith('```json'):
            content = content[7:]
        if content.startswith('```'):
            content = content[3:]
        if content.endswith('```'):
            content = content[:-3]
        content = content.strip()
            
        parsed = json.loads(content)
        
        return ProjectStatus(
            rag_score=rag_score,
            confidence=parsed.get("confidence", 80),
            summary=parsed.get("summary", ""),
            top_risks=parsed.get("top_risks", []),
            recommended_actions=parsed.get("recommended_actions", []),
            reasoning=parsed.get("reasoning", "")
        )
        
    except Exception as e:
        logger.error(f"AI generation failed: {e}. Raw content: {response.content if 'response' in locals() else 'None'}. Falling back to mock response.")
        return ProjectStatus(
            rag_score=rag_score,
            confidence=85,
            summary="Mock summary: Project is proceeding as expected (LLM fallback).",
            top_risks=["Mock risk: Resource constraint"],
            recommended_actions=["Mock action: Monitor closely"],
            reasoning=f"Fallback Mock Reasoning (API Key or connection failed: {e}): Calculated RAG score is {rag_score} based on {data.blockers_count} blockers."
        )

async def generate_recovery_plan(data: ProjectData) -> str:
    if not settings.OPENROUTER_API_KEY:
        return "## Mock Recovery Plan\n\n1. **Immediate Assessment**: Review all current blockers.\n2. **Resource Reallocation**: Shift resources to critical path items.\n3. **Daily Standups**: Implement daily monitoring until back to GREEN."
        
    try:
        llm = ChatOpenAI(
            model="google/gemini-2.5-flash",
            api_key=settings.OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
            temperature=0.4,
            max_tokens=1000
        )
        
        prompt = PromptTemplate(
            input_variables=["project_name", "rag_score", "blockers"],
            template="""You are a Senior PMO Director. 
The project '{project_name}' is currently in a {rag_score} state with {blockers} critical blockers.
Generate a structured, 3-step, 30-day tactical recovery plan to get this project back to GREEN.
Use markdown formatting with headers and bullet points. Be concise but actionable. Do NOT wrap in json."""
        )
        
        chain = prompt | llm
        response = await chain.ainvoke({
            "project_name": data.project_name,
            "rag_score": data.status.rag_score if data.status else "RED",
            "blockers": data.blockers_count
        })
        
        return response.content.strip()
    except Exception as e:
        logger.error(f"Recovery plan generation failed: {e}")
        return f"## Error Generating Plan\nCould not generate the recovery plan due to an API error: {e}"
