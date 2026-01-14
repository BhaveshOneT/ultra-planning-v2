#!/bin/bash
# Initialize a new session with planning files
# Usage: ./init-session.sh "task-name-slug"

set -e

MEMORY_DIR="${PROJECT_MEMORY_DIR:-.project-memory}"
TASK_NAME="${1:-unnamed-task}"
SESSION_ID="sess_$(date +%Y%m%d_%H%M%S)"

echo "════════════════════════════════════════════════════"
echo "  🚀 Ultra-Planning V3: Initialize Session"
echo "════════════════════════════════════════════════════"
echo ""
echo "Task: $TASK_NAME"
echo "Session ID: $SESSION_ID"
echo ""

# Create active directory if it doesn't exist
mkdir -p "$MEMORY_DIR/active"

# Copy templates to active directory
if [ -f "$MEMORY_DIR/active/TEMPLATE_task_plan.md" ]; then
    cp "$MEMORY_DIR/active/TEMPLATE_task_plan.md" "$MEMORY_DIR/active/task_plan.md"
    cp "$MEMORY_DIR/active/TEMPLATE_context.md" "$MEMORY_DIR/active/context.md"

    # Replace placeholders
    sed -i.bak "s/\[Task Name\]/$TASK_NAME/g" "$MEMORY_DIR/active/task_plan.md"
    sed -i.bak "s/\[Task Name\]/$TASK_NAME/g" "$MEMORY_DIR/active/context.md"
    sed -i.bak "s/\[Generate unique ID\]/$SESSION_ID/g" "$MEMORY_DIR/active/task_plan.md"
    sed -i.bak "s/\[Same as task_plan.md\]/$SESSION_ID/g" "$MEMORY_DIR/active/context.md"
    sed -i.bak "s/YYYY-MM-DD HH:MM:SS/$(date '+%Y-%m-%d %H:%M:%S')/g" "$MEMORY_DIR/active/task_plan.md"
    sed -i.bak "s/YYYY-MM-DD HH:MM:SS/$(date '+%Y-%m-%d %H:%M:%S')/g" "$MEMORY_DIR/active/context.md"

    rm "$MEMORY_DIR/active"/*.bak 2>/dev/null || true

    echo "✓ Created task_plan.md"
    echo "✓ Created context.md"
fi

# Create continuity ledger
if [ -f "$MEMORY_DIR/ledgers/TEMPLATE_CONTINUITY.md" ]; then
    cp "$MEMORY_DIR/ledgers/TEMPLATE_CONTINUITY.md" "$MEMORY_DIR/ledgers/CONTINUITY_active.md"

    sed -i.bak "s/\[task_name\]/$TASK_NAME/g" "$MEMORY_DIR/ledgers/CONTINUITY_active.md"
    sed -i.bak "s/\[session_id\]/$SESSION_ID/g" "$MEMORY_DIR/ledgers/CONTINUITY_active.md"
    sed -i.bak "s/YYYY-MM-DD HH:MM:SS/$(date '+%Y-%m-%d %H:%M:%S')/g" "$MEMORY_DIR/ledgers/CONTINUITY_active.md"

    rm "$MEMORY_DIR/ledgers"/*.bak 2>/dev/null || true

    echo "✓ Created continuity ledger"
fi

# V3: Start session orchestrator for intelligent automation
echo ""
echo "🤖 Starting V3 automation..."
echo ""

# Check if Python is available
if command -v python3 &> /dev/null; then
    python3 "$MEMORY_DIR/scripts/session-orchestrator.py" start "$TASK_NAME"
else
    echo "⚠️  Python3 not found, falling back to V2 mode..."
    echo ""

    # V2 fallback: Load previous knowledge
    echo "📚 Loading knowledge base..."

    if [ -f "$MEMORY_DIR/knowledge/patterns.md" ]; then
        PATTERN_COUNT=$(grep -c "^## Pattern:" "$MEMORY_DIR/knowledge/patterns.md" 2>/dev/null || echo "0")
        echo "   • Patterns available: $PATTERN_COUNT"
    fi

    if [ -f "$MEMORY_DIR/knowledge/failures.md" ]; then
        FAILURE_COUNT=$(grep -c "^## Error:\|^## Anti-Pattern:" "$MEMORY_DIR/knowledge/failures.md" 2>/dev/null || echo "0")
        echo "   • Known failures: $FAILURE_COUNT"
    fi

    # Check for previous handoff
    if [ -f "$MEMORY_DIR/handoffs/latest.yaml" ]; then
        echo ""
        echo "📦 Previous session found:"
        grep "^task:\|^status:" "$MEMORY_DIR/handoffs/latest.yaml" | sed 's/^/   /'
    fi

    echo ""
    echo "════════════════════════════════════════════════════"
    echo "  ✅ Session initialized successfully!"
    echo "════════════════════════════════════════════════════"
    echo ""
    echo "Next steps:"
    echo "  1. Edit .project-memory/active/task_plan.md"
    echo "  2. Install V3 dependencies: scripts/install-v3.sh"
    echo "  3. Start working!"
    echo ""
fi
