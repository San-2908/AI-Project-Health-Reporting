import pandas as pd
import io
from app.models.schemas import ProjectData
from fastapi import UploadFile
import logging

logger = logging.getLogger(__name__)

async def parse_excel_file(file: UploadFile) -> ProjectData:
    """
    Parses an uploaded Excel project plan and extracts structured information.
    Handles messy data gracefully.
    """
    contents = await file.read()
    
    # Read all sheets
    try:
        xls = pd.ExcelFile(io.BytesIO(contents))
        sheets = {sheet_name: xls.parse(sheet_name) for sheet_name in xls.sheet_names}
    except Exception as e:
        logger.error(f"Error parsing Excel file: {e}")
        raise ValueError(f"Could not parse Excel file: {e}")

    # Initialize default values
    project_name = file.filename.split('.')[0]
    tasks_completed = 0
    total_tasks = 0
    completion_percentage = 0.0
    schedule_variance = 0.0
    budget_variance = 0.0
    milestones_at_risk = 0
    total_milestones = 0
    blockers_count = 0
    stakeholder_sentiment = "Neutral"

    # Naive extraction logic (can be improved based on actual template)
    for sheet_name, df in sheets.items():
        sheet_name_lower = sheet_name.lower()
        
        if "task" in sheet_name_lower or "schedule" in sheet_name_lower:
            total_tasks += len(df)
            if 'Status' in df.columns:
                tasks_completed += len(df[df['Status'].astype(str).str.lower() == 'completed'])
                
        if "milestone" in sheet_name_lower:
            total_milestones += len(df)
            if 'Status' in df.columns:
                milestones_at_risk += len(df[df['Status'].astype(str).str.lower().isin(['delayed', 'at risk'])])
                
        if "risk" in sheet_name_lower or "issue" in sheet_name_lower:
            if 'Severity' in df.columns:
                blockers_count += len(df[df['Severity'].astype(str).str.lower().isin(['high', 'critical'])])
            else:
                blockers_count += len(df)

    if total_tasks > 0:
        completion_percentage = (tasks_completed / total_tasks) * 100

    return ProjectData(
        project_name=project_name,
        tasks_completed=tasks_completed,
        total_tasks=total_tasks,
        completion_percentage=completion_percentage,
        schedule_variance=schedule_variance,
        budget_variance=budget_variance,
        milestones_at_risk=milestones_at_risk,
        total_milestones=total_milestones,
        blockers_count=blockers_count,
        stakeholder_sentiment=stakeholder_sentiment
    )
