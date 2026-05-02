![A developer staring at their screen trying to remember where they left off](developer.png)
*AI Generated image*

# Session Resume Card

Every developer knows the feeling: you open your IDE after a break and spend 
the first 20 minutes just figuring out where you left off. **Session Resume Card**
fixes that.

## What it does

**Session Resume Card** reads an IBM Bob IDE session export and produces a 
Restoration String — a compact summary of exactly where you were, what you 
were doing, and what to do next. Paste it into a new Bob session and you're 
back up to speed instantly.

## Who it's for

Developers who context-switch often — working across multiple projects, 
picking up where they left off after meetings, or resuming work the next day.

## Demo

![Session Resume Card output](bob_sessions/demo.png)
*Example output from analyzing a Bob session where a developer was exploring the [F1 Race Replay](https://github.com/IAmTomShaw/f1-race-replay) codebase architecture. The Restoration String shows exactly where they were (high-level overview), what they accomplished (extracted GUI components), and what to tackle next (dive into tyre degradation module).*

## How to use it

**Requirements:**
- Python 3.11+
- IBM Cloud account with watsonx.ai access
- `requests` library: `pip install requests`

**Setup:**

Option 1: Use the convenience script (recommended):
```powershell
# Copy the template and add your credentials
copy run.ps1.template run.ps1
# Edit run.ps1 with your actual API key and project ID
```

Option 2: Set environment variables manually:
```powershell
# Set your credentials (PowerShell)
$env:WATSONX_API_KEY = "your-ibm-cloud-api-key"
$env:PROJECT_ID = "your-watsonx-project-id"
```

**Run:**
```powershell
# Using the convenience script (if you created run.ps1)
.\run.ps1 --export your_session_export.md --format structured

# Or run directly with Python (if environment variables are set)
python resume.py --export your_session_export.md --format structured

# Paragraph output
python resume.py --export your_session_export.md --format paragraph
```

**Output (structured mode):**



## How to export a Bob session

1. In Bob IDE: Views → More Actions → History
2. Select a task → click the Export icon
3. Save the `.md` file
4. Run `resume.py` against it

## How it was built

Built entirely using IBM Bob IDE and watsonx.ai — every session was exported 
and fed back into the tool itself. The bob_sessions/ folder contains the 
exported task histories from this project's own development.

**Stack:**
- IBM Bob IDE (Code mode) — wrote and edited all code
- watsonx.ai — llama-3-3-70b-instruct for summarization
- Python — CLI, API calls, card rendering

## The meta angle

This tool was built using itself. Every Bob session during development was 
exported and processed through Session Resume Card. The bob_sessions/ folder 
is proof.

## Bob sessions

All exported Bob task sessions are in the `bob_sessions/` folder, including 
consumption summary screenshots and full task history markdown files.
