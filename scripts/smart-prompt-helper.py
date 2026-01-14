#!/usr/bin/env python3
"""
Ultra-Planning V3: Smart Prompt Helper
Generate extraction prompts for Claude Code to see and act on
Uses existing Claude Code subscription - zero extra API costs!
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime


# Get project memory directory
MEMORY_DIR = Path(__file__).parent.parent
ACTIVE_DIR = MEMORY_DIR / 'active'
KNOWLEDGE_DIR = MEMORY_DIR / 'knowledge'


def count_discoveries(context_file: Path) -> int:
    """Count discoveries/findings in context.md"""
    if not context_file.exists():
        return 0

    with open(context_file, 'r') as f:
        content = f.read()

    # Count sections that look like discoveries
    discoveries = 0

    # Pattern 1: Numbered findings
    discoveries += len(re.findall(r'^\d+\.', content, re.MULTILINE))

    # Pattern 2: Bullet points with insights
    discoveries += len(re.findall(r'^[-*]\s+.{20,}', content, re.MULTILINE))

    # Pattern 3: "Discovered:", "Found:", "Learned:"
    discoveries += len(re.findall(r'(Discovered|Found|Learned):', content, re.IGNORECASE))

    return discoveries


def count_completed_phases(task_plan_file: Path) -> int:
    """Count completed phases in task_plan.md"""
    if not task_plan_file.exists():
        return 0

    with open(task_plan_file, 'r') as f:
        content = f.read()

    # Count completed checkboxes in phases section
    phases_match = re.search(r'## Phases\n(.+?)(?=\n##|\Z)', content, re.DOTALL)
    if not phases_match:
        return 0

    phases_text = phases_match.group(1)
    completed = len(re.findall(r'- \[x\]', phases_text, re.IGNORECASE))

    return completed


def count_errors_in_table(task_plan_file: Path) -> int:
    """Count errors in the error log table"""
    if not task_plan_file.exists():
        return 0

    with open(task_plan_file, 'r') as f:
        content = f.read()

    # Find error log table
    table_match = re.search(r'## Live Error Log.*?\n\|.*?\n\|[-|]+\|(.*?)(##|\Z)', content, re.DOTALL)
    if not table_match:
        return 0

    table_content = table_match.group(1)

    # Count rows (skip empty lines)
    rows = [line for line in table_content.split('\n') if line.strip() and line.startswith('|')]
    return len(rows)


def check_recent_commits() -> int:
    """Check number of commits since session start"""
    try:
        import subprocess
        # Get commits from last 24 hours
        result = subprocess.run(
            ['git', 'log', '--since="24 hours ago"', '--oneline'],
            capture_output=True,
            text=True,
            cwd=MEMORY_DIR.parent  # Project root
        )
        if result.returncode == 0:
            commits = [line for line in result.stdout.split('\n') if line.strip()]
            return len(commits)
    except:
        pass

    return 0


def generate_extraction_prompt(context_path: Path, task_plan_path: Path, trigger_reason: str) -> str:
    """Generate the extraction prompt for Claude Code"""
    discoveries = count_discoveries(context_path)
    completed_phases = count_completed_phases(task_plan_path)
    errors = count_errors_in_table(task_plan_path)
    commits = check_recent_commits()

    prompt = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧠 KNOWLEDGE EXTRACTION NEEDED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Trigger:** {trigger_reason}
**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**Session Progress:**
• Discoveries documented: {discoveries}
• Phases completed: {completed_phases}
• Errors encountered: {errors}
• Recent commits: {commits}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 WHAT TO EXTRACT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You've completed meaningful work in this session. Please extract
learnings to the knowledge base using your existing subscription.

**From active/context.md ({discoveries} discoveries):**
→ Read the discoveries and findings
→ Extract any patterns or successful approaches
→ Add to knowledge/patterns.md using the template format:

   ## Pattern: [Name]
   **Established:** {datetime.now().strftime('%Y-%m-%d')}
   **Used successfully:** 1 time
   **Implementation:** [details from your discoveries]
   **Why it works:** [your analysis]
   **Reuse when:** [applicable scenarios]

**From active/task_plan.md (error log with {errors} errors):**
→ Check the "Live Error Log" table
→ For any errors marked "Fixed" or "Resolved", ensure they are
  properly documented in knowledge/failures.md with solutions
→ Update any entries that only have symptoms but now have solutions

**From your commits ({commits} recent commits):**
→ Review commit messages and code changes
→ Extract any architectural decisions you made
→ Add to knowledge/decisions.md using the template format:

   ## Decision: [Name]
   **Made:** {datetime.now().strftime('%Y-%m-%d')}
   **Context:** [why this decision was needed]
   **Chosen:** [what you chose]
   **Rejected:** [alternatives you considered]
   **Trade-offs:** [pros and cons]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ AFTER EXTRACTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Once you've extracted learnings:
1. Delete this prompt file: active/.extraction_needed.txt
2. The knowledge base is now richer for future sessions!

**This takes 2-3 minutes and prevents knowledge loss.**
**Use the existing templates in knowledge/ files for consistency.**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    return prompt


def should_trigger_extraction(context_path: Path, task_plan_path: Path) -> tuple[bool, str]:
    """
    Determine if extraction should be triggered
    Returns: (should_trigger, reason)
    """
    discoveries = count_discoveries(context_path)
    completed_phases = count_completed_phases(task_plan_path)
    errors = count_errors_in_table(task_plan_path)

    # Trigger conditions (2-action rule and phase completion)
    if discoveries >= 2:
        return (True, f"{discoveries} discoveries documented (2-action rule)")

    if completed_phases >= 1:
        return (True, f"{completed_phases} phase(s) completed")

    if errors >= 2:
        return (True, f"{errors} errors encountered")

    return (False, "No extraction triggers met yet")


def create_extraction_prompt() -> None:
    """Main function to create extraction prompt file"""
    context_path = ACTIVE_DIR / 'context.md'
    task_plan_path = ACTIVE_DIR / 'task_plan.md'
    prompt_file = ACTIVE_DIR / '.extraction_needed.txt'

    # Check if already exists
    if prompt_file.exists():
        print("ℹ️  Extraction prompt already exists")
        print(f"   File: {prompt_file}")
        return

    # Check if extraction should be triggered
    should_trigger, reason = should_trigger_extraction(context_path, task_plan_path)

    if not should_trigger:
        print(f"⏸️  Extraction not triggered yet: {reason}")
        print()
        print("   Triggers:")
        print("   • 2+ discoveries in context.md")
        print("   • 1+ completed phases")
        print("   • 2+ errors documented")
        return

    # Generate prompt
    prompt = generate_extraction_prompt(context_path, task_plan_path, reason)

    # Write prompt file
    with open(prompt_file, 'w') as f:
        f.write(prompt)

    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("💡 KNOWLEDGE EXTRACTION PROMPT CREATED")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()
    print(f"✅ Trigger: {reason}")
    print(f"📄 File: {prompt_file}")
    print()
    print("Ask Claude Code to:")
    print('  "Read active/.extraction_needed.txt and extract the learnings"')
    print()
    print("Or Claude Code will see it automatically in context!")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")


def check_extraction_status() -> None:
    """Check if extraction is needed or already done"""
    prompt_file = ACTIVE_DIR / '.extraction_needed.txt'

    if prompt_file.exists():
        print("⚠️  Extraction prompt exists but not yet processed")
        print(f"   File: {prompt_file}")
        print()
        print("Ask Claude Code to:")
        print('  "Read active/.extraction_needed.txt and extract the learnings"')
    else:
        context_path = ACTIVE_DIR / 'context.md'
        task_plan_path = ACTIVE_DIR / 'task_plan.md'

        should_trigger, reason = should_trigger_extraction(context_path, task_plan_path)

        if should_trigger:
            print(f"✅ Extraction ready: {reason}")
            print()
            print("Run: python3 scripts/smart-prompt-helper.py --create")
        else:
            print(f"✅ No extraction needed yet: {reason}")


def main():
    if len(sys.argv) < 2:
        check_extraction_status()
    elif sys.argv[1] == '--create':
        create_extraction_prompt()
    elif sys.argv[1] == '--check':
        check_extraction_status()
    else:
        print("Ultra-Planning V3: Smart Prompt Helper")
        print()
        print("Usage:")
        print("  smart-prompt-helper.py           # Check extraction status")
        print("  smart-prompt-helper.py --create  # Create extraction prompt")
        print("  smart-prompt-helper.py --check   # Check extraction status")
        print()
        print("This script generates prompts for Claude Code to extract learnings.")
        print("Uses your existing Claude Code subscription - zero extra costs!")
        sys.exit(0)


if __name__ == '__main__':
    main()
