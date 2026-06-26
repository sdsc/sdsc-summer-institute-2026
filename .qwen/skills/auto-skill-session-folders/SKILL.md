---
name: session-folders
description: Create session folder structure for SDSC Summer Institute with README templates for instructors
source: auto-skill
extracted_at: '2026-06-26T21:30:09.690Z'
updated_at: '2026-06-26T21:45:00.000Z'
---

# Session Folders Skill

This skill creates a standardized folder structure for SDSC Summer Institute sessions, with README.md templates that instructors can fill in.

## When to Use

- Organizing multi-day conference or institute materials
- Creating session-specific documentation folders
- Setting up templates for multiple presenters/instructors

## Approach

1. **Parse the AGENDA.md** to extract:
   - Session dates and times
   - Session titles/topics
   - Presenter names and links

2. **Create folder structure** following the pattern:
   - `0_Preparation/` - Pre-event materials
   - `X.Y_session_name/` - Numbered sessions (e.g., `1.0_welcome`, `2.1_parallel_computing`)
   - Each folder contains a `README.md`

3. **README.md template format**:
   ```markdown
   ### SDSC Summer Institute 2026
   # Session X.Y Session Title

   **Date:** Day, Month Date, Year

   **Time:** Start - End Pacific

   **Summary:** 

   **Presented by:** [Presenter Name](link)
   ```

4. **Key principles**:
   - **Leave Summary field empty** for instructors to fill in (do not pre-write summaries)
   - **Include date and time** from agenda
   - **Include presenter names with links** - use existing URLs from previous year's repo or AGENDA.md
   - **Do NOT include** navigation links like "Back to Top"
   - **Do NOT include** TASKS sections unless specifically needed
   - **Actually create the PR** - don't just provide a link, use `gh pr create` to submit it

5. **Git workflow**:
   - Create a feature branch (e.g., `add-session-folders-structure`)
   - Commit all folder/README changes
   - Push with `git push -u origin branch-name`
   - **Create PR using gh CLI** (don't be lazy):
     ```bash
     gh pr create --title "Add session folder structure" --body "Description of changes" --base main --head branch-name
     ```

## Example Session Names

Based on typical SDSC Summer Institute structure:
- `0_Preparation` - Pre-event setup
- `1.0_preparation_day_welcome_and_orientation`
- `2.1_parallel_computing_concepts`
- `2.2_running_batch_and_interactive_jobs`
- `2.3_high_throughput_computing`
- `2.4_code_migration_and_software_environments`
- `3.1_data_management`
- `3.2_getting_help`
- `3.4_parallel_computing_mpi_openmp`
- `4.1_knowledge_management`
- `4.2_deep_learning_pt1`
- `4.3_deep_learning_pt2`
- `5.1_best_practices_for_scientific_computing`
- `5.2_performance_tuning`
- `5.3_gpu_computing_and_programming`
- `6.1_python_for_HPC`
- `6.2_overview_of_sdsc_supercomputers`

## Commands Used

```bash
# Create all session folders
mkdir -p session-folder/{0_Preparation,1.0_session,2.1_session,...}

# Create README in each folder
write_file path/to/session/README.md with template content

# Git workflow
git checkout -b add-session-folders-structure
git add -A
git commit -m "Add session folder structure"
git push -u origin branch-name

# Create PR (do this, don't just provide the link)
gh pr create --title "Add session folder structure" --body "Description" --base main --head branch-name
```

## Notes

- Some presenter URLs from previous years may be outdated - verify with wget if possible
- Match the folder naming convention from previous year (e.g., 2025) for consistency
- Main README.md should link to AGENDA.md rather than duplicating the schedule