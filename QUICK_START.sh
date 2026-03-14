#!/bin/bash
# Quick start script for MiroFish minimal example
# Run this from project root

echo "🐟 MiroFish Minimal Example Quick Start"
echo "======================================"
echo ""

# Step 1: Check Python
echo "✓ Checking Python..."
python --version

# Step 2: Prepare environment
echo "✓ Setting up .env file..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "  📝 .env created from .env.example"
    echo "  ⚠️  IMPORTANT: Edit .env and add your API keys:"
    echo "     LLM_API_KEY=your_key_here"
    echo ""
    exit 1
else
    echo "  ℹ .env already exists"
fi

# Step 3: Verify .env has API keys
echo "✓ Checking .env configuration..."
if ! grep -q "^LLM_API_KEY" .env || grep "^LLM_API_KEY=your" .env > /dev/null; then
    echo "  ❌ LLM_API_KEY not configured in .env"
    echo "  Please edit .env and add your API keys"
    exit 1
fi
echo "  ✓ LLM_API_KEY configured"

# Step 4: Install minimal deps
echo "✓ Installing Python packages..."
pip install -q openai python-dotenv 2>/dev/null && echo "  ✓ Dependencies installed" || {
    echo "  Installing with verbose output..."
    pip install openai python-dotenv
}

# Step 5: Run demo
echo ""
echo "🚀 Starting standalone ontology demo..."
echo "======================================"
echo ""
python example_standalone_demo.py

echo ""
echo "======================================"
echo "✓ Demo completed!"
echo ""
echo "Next steps:"
echo "  1. Review ontology_output.json"
echo "  2. Edit example_data/university_incident.md with your own text"
echo "  3. Run again: python example_standalone_demo.py"
echo "  4. For full pipeline: npm run dev"
echo ""
