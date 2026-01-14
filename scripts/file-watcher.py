#!/usr/bin/env python3
"""
Ultra-Planning V3: File Watcher
Real-time monitoring of file changes with intelligent reactions
"""

import os
import sys
import time
import re
from pathlib import Path
from datetime import datetime
from typing import Optional

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("❌ Error: watchdog library not installed")
    print("   Install with: pip install watchdog")
    sys.exit(1)


# Get project memory directory
MEMORY_DIR = Path(__file__).parent.parent
ACTIVE_DIR = MEMORY_DIR / 'active'
KNOWLEDGE_DIR = MEMORY_DIR / 'knowledge'
LEDGERS_DIR = MEMORY_DIR / 'ledgers'


class SmartFileWatcher(FileSystemEventHandler):
    """Intelligent file watcher with automated reactions"""

    def __init__(self):
        self.last_task_plan_update = 0
        self.last_context_update = 0
        self.last_knowledge_update = 0
        self.debounce_seconds = 2  # Avoid rapid-fire triggers

    def on_modified(self, event):
        """React to file modifications"""
        if event.is_directory:
            return

        file_path = Path(event.src_path)
        current_time = time.time()

        # Handle task_plan.md changes
        if file_path.name == 'task_plan.md' and file_path.parent == ACTIVE_DIR:
            if current_time - self.last_task_plan_update > self.debounce_seconds:
                self.last_task_plan_update = current_time
                self.handle_task_plan_update(file_path)

        # Handle context.md changes
        elif file_path.name == 'context.md' and file_path.parent == ACTIVE_DIR:
            if current_time - self.last_context_update > self.debounce_seconds:
                self.last_context_update = current_time
                self.handle_context_update(file_path)

        # Handle knowledge/ changes
        elif file_path.parent == KNOWLEDGE_DIR and file_path.suffix == '.md':
            if current_time - self.last_knowledge_update > self.debounce_seconds:
                self.last_knowledge_update = current_time
                self.handle_knowledge_update(file_path)

    def handle_task_plan_update(self, file_path: Path):
        """React to task_plan.md changes - update continuity ledger"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()

            # Parse phases
            phases_match = re.search(r'## Phases\n(.+?)(?=\n##|\Z)', content, re.DOTALL)
            if not phases_match:
                return

            phases_text = phases_match.group(1)

            # Count completed and total phases
            completed_phases = re.findall(r'- \[x\](.+)', phases_text, re.IGNORECASE)
            all_phases = re.findall(r'- \[[ x]\](.+)', phases_text)

            completed_count = len(completed_phases)
            total_count = len(all_phases)

            if total_count == 0:
                return

            # Get current phase (first uncompleted)
            current_phase = None
            for phase_match in re.finditer(r'- \[ \](.+)', phases_text):
                current_phase = phase_match.group(1).strip()
                break

            if not current_phase and completed_count > 0:
                current_phase = "All phases complete! 🎉"

            # Update continuity ledger
            self.update_continuity_ledger(completed_count, total_count, current_phase)

            print(f"📊 Progress tracked: {completed_count}/{total_count} phases completed")

        except Exception as e:
            print(f"⚠️  Error tracking task_plan.md: {e}")

    def handle_context_update(self, file_path: Path):
        """React to context.md changes - check for extraction triggers"""
        try:
            # Count discoveries
            with open(file_path, 'r') as f:
                content = f.read()

            discoveries = 0
            discoveries += len(re.findall(r'^\d+\.', content, re.MULTILINE))
            discoveries += len(re.findall(r'^[-*]\s+.{20,}', content, re.MULTILINE))
            discoveries += len(re.findall(r'(Discovered|Found|Learned):', content, re.IGNORECASE))

            # Check if extraction should be triggered (2-action rule)
            if discoveries >= 2:
                print(f"💡 2+ discoveries found ({discoveries}), ready for extraction")
                print("   Run: python3 scripts/smart-prompt-helper.py --create")

        except Exception as e:
            print(f"⚠️  Error checking context.md: {e}")

    def handle_knowledge_update(self, file_path: Path):
        """React to knowledge/ file changes"""
        print(f"📚 Knowledge updated: {file_path.name}")
        print("   (Auto-embedder and indexer will process this)")

    def update_continuity_ledger(self, completed: int, total: int, current_phase: Optional[str]):
        """Update the continuity ledger with progress"""
        ledger_file = LEDGERS_DIR / 'CONTINUITY_active.md'

        if not ledger_file.exists():
            return

        try:
            with open(ledger_file, 'r') as f:
                content = f.read()

            # Update progress percentage
            progress_pct = int((completed / total) * 100) if total > 0 else 0

            # Update "Current Status" section
            status_pattern = r'(## Current Status\n\n)(.+?)(\n\n##|\Z)'
            status_replacement = f'''\\1**Progress:** {completed}/{total} phases ({progress_pct}%)
**Current Phase:** {current_phase if current_phase else "Starting..."}
**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\3'''

            content = re.sub(status_pattern, status_replacement, content, flags=re.DOTALL)

            # Update "What's Complete" section with checkmarks
            complete_pattern = r'(## What\'s Complete\n\n)(.+?)(\n\n##|\Z)'

            completed_items = []
            for i in range(completed):
                completed_items.append(f"- ✅ Phase {i+1}")

            if completed > 0:
                completed_text = '\n'.join(completed_items)
                complete_replacement = f'\\1{completed_text}\\3'
                content = re.sub(complete_pattern, complete_replacement, content, flags=re.DOTALL)

            # Write back
            with open(ledger_file, 'w') as f:
                f.write(content)

        except Exception as e:
            print(f"⚠️  Error updating continuity ledger: {e}")


def start_watching(watch_dirs: list = None):
    """Start the file watcher daemon"""
    if watch_dirs is None:
        watch_dirs = [ACTIVE_DIR, KNOWLEDGE_DIR]

    print("👁️  File Watcher: Starting...")
    print()
    print(f"   Watching:")
    for watch_dir in watch_dirs:
        print(f"   • {watch_dir}")
    print()
    print("   Monitoring:")
    print("   • active/task_plan.md → Updates continuity ledger")
    print("   • active/context.md → Checks extraction triggers")
    print("   • knowledge/*.md → Flags for re-indexing/embedding")
    print()
    print("   Press Ctrl+C to stop")
    print()

    event_handler = SmartFileWatcher()
    observer = Observer()

    for watch_dir in watch_dirs:
        if watch_dir.exists():
            observer.schedule(event_handler, str(watch_dir), recursive=False)

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 File watcher stopped")
        observer.stop()

    observer.join()


def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print("Ultra-Planning V3: File Watcher")
        print()
        print("Usage:")
        print("  file-watcher.py              # Start watching (default dirs)")
        print("  file-watcher.py --help       # Show this help")
        print()
        print("Monitors file changes and triggers automatic actions:")
        print("  • task_plan.md updates → continuity ledger updated")
        print("  • context.md changes → extraction readiness checked")
        print("  • knowledge/ changes → flagged for re-indexing")
        print()
        print("Requires: pip install watchdog")
        sys.exit(0)

    start_watching()


if __name__ == '__main__':
    main()
