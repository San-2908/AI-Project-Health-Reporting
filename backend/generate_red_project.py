import pandas as pd

# Create a dummy "Tasks" sheet (0% completion)
tasks_df = pd.DataFrame({
    "Task Name": ["Phase 1", "Phase 2", "Phase 3"],
    "Assignee": ["Alice", "Bob", "Charlie"],
    "Status": ["Not Started", "Not Started", "Not Started"]
})

# Create a "Risks" sheet to trigger blockers
# The parser looks for a "Severity" column with 'high' or 'critical'
risks_df = pd.DataFrame({
    "Risk Description": ["Server crash", "Vendor bankrupt", "Key developer left", "Budget cut"],
    "Severity": ["Critical", "Critical", "High", "High"]
})

# Create a "Milestones" sheet to trigger at-risk milestones
# The parser looks for a "Status" column with 'delayed' or 'at risk'
milestones_df = pd.DataFrame({
    "Milestone": ["Beta Release", "Final Launch"],
    "Status": ["Delayed", "At Risk"]
})

# Write to Excel
with pd.ExcelWriter("Project_Red_Alert.xlsx") as writer:
    tasks_df.to_excel(writer, sheet_name="Tasks", index=False)
    risks_df.to_excel(writer, sheet_name="Risks", index=False)
    milestones_df.to_excel(writer, sheet_name="Milestones", index=False)

print("Created Project_Red_Alert.xlsx")
