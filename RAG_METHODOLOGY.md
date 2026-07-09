# RAG Methodology Framework

This document outlines the methodology used to calculate the Red, Amber, Green (RAG) status of a project within the AI Project Health Reporting Agent. 

The framework is designed to ingest raw data from Excel project plans and synthesize a mathematical health score, which is then contextualized by a Large Language Model.

## Calculation Mechanics

The agent uses a 100-point scoring system. A project starts with a perfect score (100) and receives deductions based on negative indicators found in the project data.

### Point Deductions

| Indicator | Deduction Rule | Rationale |
| :--- | :--- | :--- |
| **Completion Percentage** | `-25 points` if completion is exactly 0%.<br>`-15 points` if completion is > 0% but < 50%. | Projects that haven't started yet carry inherent risks and cannot be considered "healthy" (Green). Low completion rates also indicate potential schedule slippage. |
| **Milestones at Risk** | `-5 points` per milestone flagged as 'delayed' or 'at risk'. | Missed milestones are strong leading indicators of schedule and budget overruns. |
| **Blockers / Risks** | `-10 points` per critical/high severity issue. | Active blockers immediately halt progress and require immediate stakeholder intervention. |

## RAG Status Thresholds

Once the final score is calculated, it is mapped to a RAG status using the following thresholds:

### 🟢 GREEN (Score > 80)
- **Definition:** The project is progressing as planned. No critical blockers exist, and milestones are on track.
- **AI Treatment:** The AI validates the momentum and suggests minor monitoring optimizations.

### 🟡 AMBER (Score > 60 and <= 80)
- **Definition:** The project faces some friction. This includes projects that have 0% completion (not started), or projects with a few delayed milestones but no critical blockers.
- **AI Treatment:** The AI identifies the specific areas causing friction and recommends preventative actions to steer the project back to Green.

### 🔴 RED (Score <= 60)
- **Definition:** The project is in critical condition. Multiple high-severity blockers exist or significant milestones are severely at risk.
- **AI Treatment:** The AI will output an urgent tone, explicitly outlining the blockers and demanding immediate escalation.

## Assumptions & Data Handling

- **Data Completeness:** The system assumes that project plans may be messy. If specific sheets (e.g., "Risks") are missing, the system gracefully defaults those indicators to 0 rather than failing.
- **Status Normalization:** The parser normalizes text (ignoring case) so that "Completed", "COMPLETED", and "completed" are treated equally.
- **Subjective Metrics:** Stakeholder sentiment and budget variance are currently captured as neutral defaults, with the intention of being enriched by the LLM based on qualitative notes in future iterations.
