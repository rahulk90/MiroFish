# MiroFish Minimal Example

This is a **minimal working example** of the MiroFish pipeline that you can run locally.

## 📁 What's Included

```
example_data/
├── university_incident.md       # Sample input text (~500 words)

example_minimal_demo.py          # Standalone demo script
```

## 🚀 Quick Start

### Option 1: Use Existing ML Conda Environment

```bash
# Activate your conda environment with ML packages
conda activate ml

# Install missing packages (if needed)
pip install openai zep-cloud pydantic python-dotenv

# Setup .env file with API keys
cp .env.example .env
# Edit .env and add your API keys:
#   LLM_API_KEY=...
#   ZEP_API_KEY=...

# Run the demo
python example_minimal_demo.py
```

### Option 2: Quick Setup with Project Commands

```bash
# From project root
npm run setup:backend  # Installs all Python deps

# Or manually:
cd backend
uv sync

# Then run demo
cd ..
python example_minimal_demo.py
```

## 📊 What the Demo Does

The script runs through all **3 major steps** of MiroFish:

### Step 1: Ontology Generation ✓
- Analyzes the example text about a university plagiarism scandal
- LLM extracts entity types (Professor, Student, Journalist, etc.)
- LLM extracts relationship types (STUDIES_AT, WORKS_FOR, etc.)
- **No external services needed** - pure LLM analysis

**Output example:**
```
Entity Types:
  • Professor: Academic faculty member
  • Student: University student
  • Journalist: Media professional
  • University: Educational institution

Edge Types:
  • WORKS_FOR: Employment relationship
  • STUDIES_AT: Academic enrollment
  • REPORTS_ON: News coverage
```

### Step 2: Graph Building (Requires Zep API)
- Chunks the text into pieces
- Sends to Zep Cloud API for entity/relationship extraction
- Builds knowledge graph in Zep backend
- **Requires**: ZEP_API_KEY

**Output**: Graph ID and entity count

### Step 3: Persona Generation (Mock Demo)
- Generates detailed agent personas for key entities
- Includes demographics, MBTI, background, personality
- Shows what personas would look like
- **No API needed** - uses hardcoded examples

**Output example:**
```json
{
  "name": "Professor Zhang Wei",
  "age": 45,
  "gender": "male",
  "mbti": "INTJ",
  "bio": "Tenured CS professor with 20+ years experience",
  "persona": "Professor Zhang is a 45-year-old computer scientist..."
}
```

## 🔧 Configuration

### Required: API Keys

Create/update `.env` file in project root:

```env
# LLM API (OpenAI-compatible format)
# Option A: Alibaba Qwen (recommended - cheaper)
LLM_API_KEY=sk-xxxxx
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_MODEL_NAME=qwen-plus

# Option B: OpenAI
# LLM_API_KEY=sk-proj-xxxxx
# LLM_BASE_URL=https://api.openai.com/v1
# LLM_MODEL_NAME=gpt-4-turbo

# Zep Cloud (free tier available)
ZEP_API_KEY=your_zep_api_key_here
```

### Optional: Custom Input

Edit `example_data/university_incident.md` to use your own text, or create a new file and modify the script.

## 💰 Cost Estimate

For this minimal example:

| Step | Cost | Notes |
|------|------|-------|
| Ontology Generation | ~$0.05 | 1 LLM call |
| Graph Building | ~$0.05 | 1 Zep API call |
| Persona Generation | ~$0.20 | Mock - no cost |
| **Total** | **~$0.10** | Very cheap! |

If using Alibaba Qwen: ~¥0.50-1 CNY

## 🎯 What It Demonstrates

✅ **Ontology Generation**: Extract schema from raw text
✅ **Knowledge Graph Building**: Parse entities and relationships
✅ **Persona Development**: Create rich character profiles
✅ **Data Pipeline**: End-to-end workflow integration

❌ **Not Included**: Actual simulation (requires more complex setup)

## 🔄 Understanding the Flow

```
Input Text
    ↓
[Step 1] OntologyGenerator → Entity/Relationship Types
    ↓
[Step 2] GraphBuilderService → Zep Knowledge Graph
    ↓
[Step 3] OasisProfileGenerator → Agent Personas
    ↓
Output: Personas ready for simulation
```

## 📝 Example Input

The included `university_incident.md` describes:
- A plagiarism scandal at a university
- Key figures: professor, student, journalist, dean
- Timeline and reactions
- Multiple perspectives

This is enough for the system to:
1. Identify 10 entity types (specific + generic)
2. Create ~20-30 relationship types
3. Generate personas for 3+ characters

## 🐛 Troubleshooting

### Error: "LLM_API_KEY not configured"
```bash
# Make sure .env exists and has valid keys
cp .env.example .env
# Edit and add your API keys
```

### Error: "zep_cloud not installed"
```bash
pip install zep-cloud
```

### Error: "OpenAI not installed"
```bash
pip install openai>=1.0.0
```

### Slow Response
- Ontology generation typically takes 30-60 seconds
- Graph building depends on Zep API response time
- Normal behavior!

### API Errors
- Check your API keys are valid
- Check API quotas/billing
- Check internet connection

## 📚 Next Steps

After running this example:

1. **Modify the input**: Edit `example_data/university_incident.md` with your own event description

2. **Run full pipeline**: Use the web UI
   ```bash
   npm run dev
   # Open http://localhost:3000
   ```

3. **Customize personas**: Edit the generated personas for simulation

4. **Run simulation**: Use the OASIS platform with your personas to simulate social interactions

## 🎓 Learning Resources

- **Ontology Design**: See `backend/app/services/ontology_generator.py`
- **Graph Building**: See `backend/app/services/graph_builder.py`
- **Persona Generation**: See `backend/app/services/oasis_profile_generator.py`
- **Full Workflow**: See `backend/app/api/graph.py` for REST endpoints

## 💡 Tips

- **Start small**: Use short texts (500-1000 words) for testing
- **Clear topics**: The more specific your input, the better the ontology
- **Multiple perspectives**: Include different viewpoints in your text
- **Name entities**: Explicitly name people and organizations

## 📧 Issues?

If you run into problems:

1. Check all API keys are valid
2. Verify Python 3.11+ and Node.js 18+
3. Run `pip install -r backend/requirements.txt`
4. Check logs in terminal output

Good luck! 🐟
