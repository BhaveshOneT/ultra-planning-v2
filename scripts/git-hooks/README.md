# Ultra-Planning V3: Git Hooks

These git hooks integrate Ultra-Planning with your git workflow.

## Post-Commit Hook

**What it does:**
- Shows a reminder after each commit
- Suggests Claude Code extract learnings from the commit
- No API calls - just a friendly reminder!

**Installation:**

### For project-specific .project-memory:
```bash
cd /path/to/your/project
cp .project-memory/scripts/git-hooks/post-commit .git/hooks/post-commit
chmod +x .git/hooks/post-commit
```

### For global ~/.project-memory:
```bash
# From your project directory
cp ~/.project-memory/scripts/git-hooks/post-commit .git/hooks/post-commit
chmod +x .git/hooks/post-commit
```

### To install for all future repos (global template):
```bash
# Set up global hooks directory
mkdir -p ~/.git-templates/hooks
git config --global init.templatedir ~/.git-templates

# Copy hook
cp ~/.project-memory/scripts/git-hooks/post-commit ~/.git-templates/hooks/post-commit
chmod +x ~/.git-templates/hooks/post-commit

# Future git init or git clone will automatically include this hook!
```

## How It Works

1. You make a commit: `git commit -m "Add JWT authentication"`

2. Hook shows reminder:
   ```
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   📝 Commit created: Claude Code can extract learnings!
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   Commit: [a1b2c3d] Add JWT authentication

   💡 Ask Claude Code:
      "Extract pattern from this commit to patterns.md"
      "Document any decisions to decisions.md"
   ```

3. You ask Claude Code to extract (during your active session, uses existing subscription!)

4. Claude Code reads the commit, extracts patterns/decisions, updates knowledge base

## Benefits

- **Zero extra costs** - Uses existing Claude Code subscription
- **Non-intrusive** - Just a reminder, doesn't block commits
- **Contextual** - Only shows in projects with .project-memory
- **Smart** - Can trigger smart-prompt-helper.py for automatic prompts

## Disable Temporarily

To temporarily disable the hook:
```bash
chmod -x .git/hooks/post-commit
```

To re-enable:
```bash
chmod +x .git/hooks/post-commit
```

## Remove Completely

```bash
rm .git/hooks/post-commit
```
