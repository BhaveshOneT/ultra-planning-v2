# Ultra-Planning V3: Zero-Manual Intelligence

**Transformation:** V2 (60% manual) → V3 (95% automated)

---

## What Changed in V3?

### V2 (Manual Documentation)
- ❌ User manually fills templates
- ❌ User manually copies errors to failures.md
- ❌ User manually extracts patterns
- ❌ User manually updates index.md
- ❌ User manually runs vector-search.py --generate

### V3 (Intelligent Automation)
- ✅ Templates auto-filled with relevant past knowledge
- ✅ Errors auto-captured from terminal
- ✅ Patterns auto-extracted by Claude Code (uses existing subscription!)
- ✅ Index.md auto-generated with cross-references
- ✅ Vector embeddings auto-updated on knowledge changes

---

## 7 Automation Modules

### Module 1: Template Injector ⚡
**Auto-fill templates with past knowledge**

**Before (V2):**
```bash
./scripts/init-session.sh "jwt-auth"
# Template created with placeholders
# User manually fills:
#   - Pre-Task Intelligence (search patterns.md)
#   - Known failures to avoid (search failures.md)
#   - Related decisions (search decisions.md)
# Time: 5+ minutes
```

**After (V3):**
```bash
./scripts/init-session.sh "jwt-auth"
# Template auto-filled with:
#   ✓ 3 relevant patterns (JWT, auth, token)
#   ✓ 2 known failures (jwt.verify missing secret)
#   ✓ 1 related decision (OAuth vs JWT)
#   ✓ Suggested phases from similar tasks
# Time: 30 seconds
```

**How it works:**
- Extracts keywords from task name
- Searches knowledge base with relevance scoring
- Injects top matches into template
- Suggests phases from archived similar tasks

---

### Module 2: Error Monitor 🔥
**Auto-capture errors from terminal**

**Before (V2):**
```bash
npm test
# Error: jwt.verify() secret or public key must be provided
# User manually:
#   1. Copy error message
#   2. Open knowledge/failures.md
#   3. Write error entry with template
#   4. Update task_plan.md error log table
# Time: 2-3 minutes per error
```

**After (V3):**
```bash
npm test 2>&1 | scripts/error-monitor.py
# OR
scripts/error-monitor.py --run npm test

# ✓ Error auto-detected and captured
# ✓ Added to knowledge/failures.md with:
#   - Symptom
#   - Stack trace
#   - Command that failed
#   - Timestamp
# ✓ Updated error log table in task_plan.md
# Time: 0 seconds (automatic)
```

**How it works:**
- Monitors stdout/stderr for error patterns
- Extracts error context (20 lines around error)
- Auto-documents to failures.md
- Updates task plan error table
- Notifies user

---

### Module 3: Claude Code Integration 🧠
**Zero extra API costs, uses existing subscription**

**Before (V2):**
```bash
# Daemon only flags for manual review:
# "→ Manual review recommended for: patterns.md"
# User must write pattern descriptions manually
```

**After (V3):**
```bash
# After 2+ discoveries or 1+ phase completion:
# System creates: active/.extraction_needed.txt
# Contains prompt for Claude Code:
#   "Extract patterns from context.md to patterns.md"
#   "Document decisions to decisions.md"

# User asks Claude Code:
#   "Read active/.extraction_needed.txt and extract learnings"

# Claude Code (during your active session):
#   ✓ Reads discoveries from context.md
#   ✓ Extracts patterns with proper formatting
#   ✓ Documents decisions from commits
#   ✓ Updates failures.md with solutions
#   ✓ Uses existing Claude Code subscription (zero extra cost!)
```

**Git Hook Integration:**
```bash
git commit -m "Add JWT auth"
# Post-commit hook shows:
#   "📝 Commit detected: Claude Code can extract learnings!"
#   "Ask Claude Code: 'Extract pattern from this commit'"
```

**How it works:**
- smart-prompt-helper.py generates extraction prompts
- Prompts saved to active/.extraction_needed.txt
- Claude Code sees prompt during session
- Git hooks remind (no API calls, just text)
- 85% automated, zero extra costs

---

### Module 4: File Watcher 👁️
**Real-time monitoring and auto-updates**

**Before (V2):**
```bash
# User manually updates task_plan.md:
- [x] Phase 3: Implement token generation

# User manually updates CONTINUITY ledger:
Progress: 3/5 phases (60%)
Current Phase: Phase 4: Add middleware
Last Updated: [manually entered]
```

**After (V3):**
```bash
# File watcher detects changes to task_plan.md
# Automatically:
#   ✓ Counts completed vs total phases
#   ✓ Updates CONTINUITY ledger in real-time
#   ✓ Tracks current phase
#   ✓ Updates progress percentage
#   ✓ Timestamps last update

# Also monitors:
#   • context.md → Triggers extraction on 2+ discoveries
#   • knowledge/*.md → Flags for re-indexing/embedding
```

**How it works:**
- Uses watchdog library for filesystem events
- Debounces rapid changes (2 second threshold)
- Parses markdown for phase checkboxes
- Auto-updates continuity ledger
- Notifies when extraction triggers met

---

### Module 5: Auto-Embedder 🔮
**Always-fresh semantic search**

**Before (V2):**
```bash
# Manual one-time embedding:
python3 scripts/vector-search.py --generate
# Embeddings go stale as knowledge grows
# Must manually re-run to update
```

**After (V3):**
```bash
# Embeddings auto-update when knowledge changes
# Triggered by:
#   • File watcher detecting knowledge/*.md changes
#   • Session idle processing
#   • Archive task completion

# Smart caching:
#   ✓ Only re-embeds changed files (hash-based)
#   ✓ Skips unchanged content
#   ✓ Runs in background

# Check status anytime:
python3 scripts/auto-embedder.py --status
```

**How it works:**
- SHA256 hash cache tracks file changes
- Only embeds when hash differs from cache
- Uses BGE-large-en-v1.5 model
- Saves embeddings as .npy + metadata .json
- Always available for semantic search

---

### Module 6: Knowledge Indexer 📇
**Auto-generated index with cross-references**

**Before (V2):**
```markdown
# knowledge/index.md (manually maintained)
**Patterns documented:** 0  ← Hardcoded, never updated
**Failures prevented:** 0
**Total knowledge entries:** 0

Keywords: (manually added)
```

**After (V3):**
```markdown
# knowledge/index.md (auto-generated)
**Last updated:** 2026-01-14 15:30
**Auto-generated** by knowledge-indexer.py

## Statistics
**Patterns documented:** 12  ← Live count
**Failures prevented:** 8
**Decisions recorded:** 5
**Gotchas tracked:** 3
**Total knowledge entries:** 28

## Most Common Keywords
- **authentication** (3 in patterns.md, 2 in failures.md)
- **jwt** (2 in patterns.md, 1 in decisions.md)
- **token** (4 in patterns.md, 1 in failures.md)

## Cross-References (Related Entries)
- **patterns.md** ↔️ **decisions.md** (82% similar)
  - JWT Authentication pattern
  - OAuth vs JWT decision
```

**How it works:**
- Parses all knowledge files
- Counts sections automatically
- Extracts keywords (NLP-style filtering)
- Builds reverse index (keyword → locations)
- Uses embeddings for semantic cross-references (75%+ similarity)
- Auto-triggered by file watcher and daemon

---

### Module 7: Session Orchestrator 🎯
**Master controller coordinating everything**

**Session Start:**
```bash
./scripts/init-session.sh "build-api"

# Orchestrator coordinates:
#   1. ✓ Template injection (auto-fill with past knowledge)
#   2. ✓ Embedding status check
#   3. ✓ File watcher start (background monitoring)
#   4. ✓ Load previous session handoff (if exists)

# Output:
#   "✅ Session ready! Automation active."
#   "Just code - the system handles the rest! 🚀"
```

**Session Idle (>5 min):**
```bash
# Daemon triggers: scripts/session-orchestrator.py idle

# Orchestrator runs:
#   1. ✓ Check if extraction needed (smart-prompt-helper)
#   2. ✓ Update knowledge index
#   3. ✓ Update embeddings (if knowledge changed)
#   4. ✓ Create YAML handoff

# Output:
#   "✅ Idle processing complete!"
```

**Session End:**
```bash
./scripts/archive-task.sh

# Orchestrator runs:
#   1. ✓ Final extraction pass
#   2. ✓ Stop file watcher (gracefully)
#   3. ✓ Archive files
#   4. ✓ Update handoff

# Output:
#   "✅ Session ended. Knowledge preserved!"
```

**How it works:**
- Python master script coordinates all modules
- Subprocess management for background tasks
- Graceful shutdown with signal handlers
- Fallback to V2 if dependencies missing
- Error-tolerant (continues even if modules fail)

---

## Configuration (config.yaml)

All automation can be customized:

```yaml
automation:
  template_injection: true      # Auto-fill templates
  error_monitoring: true         # Capture errors
  file_watching: true            # Real-time tracking
  auto_embedding: true           # Vector updates
  auto_indexing: true            # Index generation
  claude_extraction: true        # Smart extraction

monitoring:
  idle_threshold_minutes: 5      # Extraction trigger
  file_debounce_seconds: 2       # Change detection

template_injection:
  relevance_threshold: 0.3       # Keyword matching (0.0-1.0)
  max_patterns: 3                # Top N patterns
  max_failures: 3                # Top N failures
  max_decisions: 2               # Top N decisions

extraction:
  discovery_trigger: 2           # N discoveries
  phase_trigger: 1               # N phases
  error_trigger: 2               # N errors
```

---

## Dependencies

### Core (Required for V3):
```bash
pip install watchdog
```

### Semantic Search (Recommended):
```bash
pip install sentence-transformers numpy
```

### Quick Install:
```bash
./scripts/install-v3.sh
```

### Optional (V3 works without these):
- Git hooks (manual install)
- Semantic embeddings (fallback to keyword search)

---

## V2 vs V3 Comparison

| Feature | V2 | V3 |
|---------|----|----|
| **Template filling** | Manual (5 min) | Auto (30 sec) |
| **Error capture** | Manual copy-paste | Auto-captured |
| **Pattern extraction** | Manual writing | Claude Code (during session) |
| **Knowledge index** | Manual maintenance | Auto-generated |
| **Vector embeddings** | Manual one-time | Auto-updated |
| **Progress tracking** | Manual ledger updates | Real-time auto-update |
| **Session start** | Blank templates | Pre-filled with intelligence |
| **Idle processing** | Flags for review | Smart extraction + index |
| **Cross-references** | None | Semantic similarity (75%+) |
| **Extra API costs** | N/A | Zero (uses Claude Code subscription) |
| **Manual work** | 60% | 5% |
| **Automation level** | 40% | 95% |

---

## Real-World Workflow (V3)

```bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DAY 1: Start new task
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

$ ./scripts/init-session.sh "add-payment-api"

# Orchestrator output:
#   📚 Injecting past knowledge...
#      ✓ 2 relevant patterns found (REST API, Stripe)
#      ✓ 1 known failure (API key leakage)
#      ✓ Suggested phases from similar tasks
#   👁️  File watcher started (background)
#   ✅ Session ready! Just code!

# You edit: active/task_plan.md
# (Template already has past Stripe pattern pre-filled!)

# You start coding:
$ npm run dev

# Hit an error:
$ npm test 2>&1 | scripts/error-monitor.py
# Error: Missing STRIPE_API_KEY

#   🔥 ERROR DETECTED:
#      Missing STRIPE_API_KEY
#   ✓ Auto-captured to knowledge/failures.md
#   ✓ Updated task_plan.md error log

# You fix it, commit:
$ git commit -m "Add Stripe payment endpoint"

# Git hook shows:
#   📝 Commit detected: Claude Code can extract learnings!
#      Ask Claude Code: "Extract pattern from this commit"

# You ask Claude Code (during session):
#   "Read active/.extraction_needed.txt and extract learnings"

# Claude Code (using your subscription):
#   ✓ Extracted payment API pattern to patterns.md
#   ✓ Documented Stripe key decision to decisions.md
#   ✓ Updated error solution in failures.md

# You mark phase complete:
# - [x] Phase 3: Implement payment endpoint

# File watcher detects:
#   📊 Progress tracked: 3/5 phases completed
#   ✓ Continuity ledger auto-updated

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SESSION IDLE (coffee break)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Daemon triggers after 5 min:
#   ⏰ Session idle, processing learnings...
#   ✓ Knowledge index updated (15 entries)
#   ✓ Embeddings refreshed
#   ✓ YAML handoff created

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# END OF DAY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

$ ./scripts/archive-task.sh

# Orchestrator:
#   🤖 Final extraction pass...
#   🛑 File watcher stopped
#   📦 Archived to: archive/2026-01-14_add-payment-api/
#   ✅ Knowledge preserved!

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# WHAT YOU DID MANUALLY:
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#   ✓ Coded your feature
#   ✓ Asked Claude Code to extract (once)
#   ✓ That's it!

# WHAT WAS AUTOMATED:
#   ✓ Template pre-filled with Stripe pattern
#   ✓ Error auto-captured
#   ✓ Progress auto-tracked
#   ✓ Pattern extracted by Claude Code
#   ✓ Index auto-updated
#   ✓ Embeddings refreshed
#   ✓ Task archived with full context
```

---

## Migration from V2 to V3

### Existing V2 Users:

1. **Install V3 dependencies:**
   ```bash
   ./scripts/install-v3.sh
   ```

2. **Generate initial embeddings (optional):**
   ```bash
   python3 scripts/auto-embedder.py --embed
   ```

3. **Regenerate index:**
   ```bash
   python3 scripts/knowledge-indexer.py
   ```

4. **Start using V3:**
   ```bash
   ./scripts/init-session.sh "your-next-task"
   ```

### Compatibility:
- ✅ All V2 knowledge files work as-is
- ✅ V3 scripts detect missing dependencies and fallback to V2 mode
- ✅ No breaking changes to existing workflows
- ✅ Can use V2 and V3 features side-by-side

---

## Benefits

### Time Savings:
- **Session start:** 5 min → 30 sec (90% faster)
- **Error documentation:** 2 min/error → 0 sec (100% automated)
- **Pattern extraction:** 5 min/pattern → Claude Code (existing subscription)
- **Index maintenance:** 10 min/week → 0 sec (100% automated)

### Quality Improvements:
- **No missed errors** - All captured automatically
- **Consistent formatting** - Templates ensure structure
- **Smart cross-references** - Semantic similarity finds connections
- **Always searchable** - Embeddings stay fresh

### Cost:
- **Zero extra API costs** - Uses Claude Code subscription
- **Open source dependencies** - All libraries free (MIT/Apache)

---

## Troubleshooting

### File Watcher Not Starting:
```bash
# Install watchdog
pip3 install watchdog

# Verify
python3 -c "import watchdog; print('OK')"
```

### Embeddings Failing:
```bash
# Install sentence-transformers (large download)
pip3 install sentence-transformers numpy

# May take 5-10 minutes first time (downloads ~1GB model)
```

### V3 Features Not Working:
```bash
# Check Python version (need 3.7+)
python3 --version

# Re-run installer
./scripts/install-v3.sh

# Check for errors in output
```

### Fallback to V2:
- V3 gracefully falls back to V2 if dependencies missing
- Core functionality (templates, knowledge base) always works
- Advanced features (auto-embedding, file watching) require dependencies

---

## Future Enhancements (V4?)

Ideas for even more automation:
- **Live Code Analysis:** Auto-detect patterns from git diffs
- **Automatic Test Generation:** Extract test cases from errors
- **Multi-Project Intelligence:** Share knowledge across repositories
- **Voice Integration:** Dictate discoveries, auto-transcribe to context.md
- **IDE Extensions:** VSCode/JetBrains integration
- **Team Knowledge Sharing:** Merge knowledge bases across team

---

**Ultra-Planning V3: You code. System learns. Knowledge compounds. Zero extra costs.**

**Ready to get started? Run `./scripts/install-v3.sh`**
