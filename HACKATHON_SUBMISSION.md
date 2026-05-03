# ⚡ reB0ot - Hackathon Submission

## Problem and Solution Statement

Every developer has experienced this frustration: you close your IDE after a productive coding session, then return hours or days later only to spend 20 precious minutes just figuring out where you left off. You scroll through files, re-read code comments, check git logs, and try to reconstruct your mental model of what you were building and why. This "context-switching tax" is especially brutal for developers juggling multiple projects, returning from meetings, or picking up work the next morning. The problem isn't just lost time—it's the cognitive load of rebuilding your entire mental state from scratch.

**⚡ reB0ot** solves this by transforming IBM Bob IDE session exports into instant cognitive restoration. When you finish a coding session in Bob, you export it. ⚡ reB0ot reads that export and generates a **Restoration String**—a hyper-compressed summary containing exactly what you were building, why you chose that approach over alternatives, which files are in progress, the precise next step, and crucially, what dead ends you already ruled out. When you return to work, you paste this string into a fresh Bob session and—boom—you're instantly back in the zone, no mental reloading required.

### Target Users and Interaction

The target users are professional developers who context-switch frequently: those working across multiple codebases, returning from meetings, or resuming work after breaks. They interact with ⚡ reB0ot through a simple command-line interface. After exporting a Bob session (**Views → More Actions → History → Export**), they run:

```bash
python reboot.py --export session.md --format structured
```

They receive either a structured card with labeled fields (`PROJECT`, `STATE`, `LAST ACTION`, `NEXT`, `DEAD ENDS`) or a dense paragraph format—both optimized for pasting directly into Bob as context.

### What Makes It Unique

What makes ⚡ reB0ot creative and unique is its **meta-recursive nature**: it was built entirely using itself. Every development session was exported and fed back through ⚡ reB0ot to resume work. The `bob_sessions/` folder contains proof—exported task histories from the project's own development. This isn't just a tool for Bob; it's a tool built by Bob, for Bob users, using Bob.

The solution addresses context-switching in a way judges have never seen: by treating developer cognitive state as compressible data that can be extracted, stored, and restored on demand. Instead of forcing developers to manually reconstruct their mental model, ⚡ reB0ot automates the extraction and restoration of that exact cognitive state, turning a 20-minute catch-up ritual into a 5-second paste operation.

### Impact and Innovation

The efficiency gain is dramatic: developers reclaim those lost 20 minutes every single time they context-switch. For a developer who switches contexts 3 times per day, that's an hour saved daily—**5 hours per week, 260 hours per year**. But the real innovation isn't just time savings; it's the elimination of cognitive friction. ⚡ reB0ot doesn't just tell you what you were doing—it tells you what you already tried and rejected, preventing you from wasting time re-exploring dead ends. It captures not just the "what" but the "why" and the "why not," preserving the full decision-making context that makes expert developers effective.

---

## How IBM Bob and watsonx Were Used

**IBM Bob IDE** was the exclusive development environment for ⚡ reB0ot—every single line of code was written, edited, and debugged using Bob's Code mode. The project demonstrates Bob's capabilities across multiple dimensions:

### Code Generation and Iteration

Bob wrote the initial `reboot.py` implementation, including the core `generate_restoration_string()` function that orchestrates the entire workflow. When bugs emerged (like Unicode encoding issues on Windows), Bob diagnosed and fixed them by modifying the `main()` function to wrap stdout with UTF-8 encoding. When the output format needed refinement, Bob implemented the `format_card()` function to create visually structured cards with proper text wrapping.

### Architecture Decisions

Bob designed the two-format system (paragraph vs. structured) and implemented the logic to handle both. The `INSTRUCTION` and `INSTRUCTION_STRUCTURED` prompts were crafted through iterative refinement with Bob, optimizing for conciseness and accuracy. Bob also implemented the smart text truncation strategy (first 1500 + last 1500 characters) to capture both task context and outcome within token limits.

### Testing and Debugging

Bob created `test_debug.py`, a comprehensive test suite covering syntax validation, environment variable handling, file operations, text processing, API payload structure, argument parsing, and output parsing. The `debug_report.md` was generated through Bob's analysis, documenting all 16 tests with zero failures.

### Documentation

Bob wrote the entire `README.md`, including usage instructions, setup steps, and the meta-narrative about the tool being built using itself. Bob also created `SECURITY.md` and the PowerShell template `run.ps1.template` for convenient credential management.

### watsonx.ai Integration

The project uses **watsonx.ai's `meta-llama/llama-3-3-70b-instruct` model** as its cognitive extraction engine. The `generate_restoration_string()` function constructs prompts with few-shot examples, sends them to watsonx.ai via the `/ml/v1/text/generation` endpoint, and processes the responses. The model parameters were tuned specifically for this task:

- `max_new_tokens`: 175 for paragraph format, 250 for structured format
- `repetition_penalty`: 1.3 to prevent redundancy
- `decoding_method`: greedy for deterministic output

The `get_iam_token()` function handles IBM Cloud authentication, exchanging API keys for bearer tokens.

### Meta-Development Process

The most compelling demonstration of Bob's power is in the `bob_sessions/` folder. Files like `bob_task_reboot.md`, `bob_task_format_argument.md`, and `bob_task_max_new_tokens.md` show actual exported sessions from building ⚡ reB0ot. Each session was exported, processed through ⚡ reB0ot itself, and the resulting Restoration String was pasted back into Bob to resume work. This recursive workflow—using the tool to build itself—validates both Bob's capabilities and ⚡ reB0ot's effectiveness.

### Specific Bob Features Used

- **Code Mode**: Primary development environment for all Python code
- **Ask Mode**: Used for architectural discussions and design decisions (evidenced by `bob_ask_mode.PNG`)
- **Session Export**: Core feature that ⚡ reB0ot depends on—Bob's ability to export complete task histories as markdown
- **File Operations**: Bob's `read_file`, `write_to_file`, and `apply_diff` tools were used extensively
- **Terminal Integration**: Bob executed Python scripts, ran tests, and validated output through `execute_command`

### The Synergy

The synergy between Bob and watsonx.ai is what makes ⚡ reB0ot possible: Bob provides the structured development environment and session export capability, while watsonx.ai provides the language understanding to compress those sessions into actionable Restoration Strings. Without Bob's session export feature, there would be no raw material to process. Without watsonx.ai's language model, there would be no way to intelligently extract and compress the cognitive state. Together, they create a closed loop: **Bob helps you code, ⚡ reB0ot helps you remember, and you paste that memory back into Bob to continue coding.**