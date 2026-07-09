import asyncio
from app.models.schemas import ProjectData
from app.services.ai_engine import generate_project_status
from app.core.config import settings

async def main():
    data = ProjectData(
        project_name="Test",
        completion_percentage=0,
        blockers_count=0,
        milestones_at_risk=0
    )
    res = await generate_project_status(data)
    print("Result:", res)

if __name__ == "__main__":
    asyncio.run(main())
