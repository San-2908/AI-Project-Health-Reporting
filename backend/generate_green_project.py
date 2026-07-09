import pandas as pd

# Create a dummy "Tasks" sheet (100% completion)
tasks_df = pd.DataFrame({
    "Task Name": ["Phase 1", "Phase 2", "Phase 3"],
    "Assignee": ["Alice", "Bob", "Charlie"],
    "Status": ["Completed", "Completed", "Completed"]
})

# Create a "Risks" sheet with no critical blockers
risks_df = pd.DataFrame({
    "Risk Description": ["Minor delay", "Coffee machine broke"],
    "Severity": ["Low", "Low"]
})

# Create a "Milestones" sheet with all completed
milestones_df = pd.DataFrame({
    "Milestone": ["Beta Release", "Final Launch"],
    "Status": ["Completed", "Completed"]
})

# Write to Excel
with pd.ExcelWriter("Project_Green_Success.xlsx") as writer:
    tasks_df.to_excel(writer, sheet_name="Tasks", index=False)
    risks_df.to_excel(writer, sheet_name="Risks", index=False)
    milestones_df.to_excel(writer, sheet_name="Milestones", index=False)

print("Created Project_Green_Success.xlsx")
