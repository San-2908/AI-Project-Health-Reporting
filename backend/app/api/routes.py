from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from typing import List
from app.models.schemas import ProjectData, PortfolioReport
from app.services.excel_parser import parse_excel_file
from app.services.ai_engine import generate_project_status, generate_recovery_plan
from app.services.ppt_generator import create_ppt_presentation
router = APIRouter()

# In-memory storage for the assignment
projects_db: List[ProjectData] = []

@router.post("/upload", response_model=List[ProjectData])
async def upload_project_plan(files: List[UploadFile] = File(...)):
    global projects_db
    new_projects = []
    
    for file in files:
        if not file.filename.endswith(('.xls', '.xlsx')):
            continue
        try:
            data = await parse_excel_file(file)
            status = await generate_project_status(data)
            data.status = status
            new_projects.append(data)
            projects_db.append(data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to process {file.filename}: {e}")
            
    return new_projects

@router.post("/analyze", response_model=List[ProjectData])
async def analyze_projects():
    return projects_db

@router.post("/weekly-report")
async def generate_weekly_report():
    return {"message": "Weekly report generated", "data": projects_db}

@router.post("/monthly-report")
async def generate_monthly_report():
    return {"message": "Monthly report generated", "data": projects_db}

@router.get("/projects", response_model=List[ProjectData])
async def get_projects():
    return projects_db

@router.post("/recovery-plan/{project_name}")
async def get_recovery_plan(project_name: str):
    global projects_db
    project = next((p for p in projects_db if p.project_name == project_name), None)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    plan = await generate_recovery_plan(project)
    return {"recovery_plan": plan}

@router.get("/download-ppt")
async def download_ppt():
    if not projects_db:
        raise HTTPException(status_code=400, detail="No projects available to generate presentation.")
    ppt_stream = create_ppt_presentation(projects_db)
    return StreamingResponse(
        ppt_stream,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        headers={"Content-Disposition": "attachment; filename=Portfolio_Report.pptx"}
    )

@router.get("/health")
async def get_health():
    return {"status": "ok"}
