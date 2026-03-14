# MiroFish Setup with Conda

Quick setup guide for running the minimal example with your conda `ml` environment.

## ⚡ Super Quick (5 minutes)

```bash
# 1. Navigate to project
cd /Users/rahulgk/Documents/code/MiroFish

# 2. Activate your ML environment
conda activate ml

# 3. Install 2 packages (should be fast)
pip install openai python-dotenv

# 4. Setup environment file
cp .env.example .env
# Edit .env and add your LLM_API_KEY

# 5. Run the demo
python example_standalone_demo.py
```

That's it! ✓

---

## 🔧 Detailed Steps

### Step 1: Activate Conda Environment

```bash
conda activate ml
```

Verify it worked:
```bash
python --version  # Should be 3.11+
pip --version     # Should show pip from conda ml env
```

### Step 2: Install Minimal Dependencies

This demo only needs **2 packages**:

```bash
pip install openai python-dotenv
```

These are small and fast to install. Your `ml` environment should already have numpy, pandas, etc.

Verify installation:
```bash
python -c "import openai; print(openai.__version__)"
python -c "import dotenv; print('dotenv OK')"
```

### Step 3: Configure API Keys

Create/edit `.env` file in project root:

```bash
cp .env.example .env
nano .env  # or use your favorite editor
```

Add your API keys:

```env
# Required: LLM API Key
LLM_API_KEY=sk-xxxxxxxxxxxxx
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_MODEL_NAME=qwen-plus

# Optional: Zep (only needed for full pipeline)
# ZEP_API_KEY=your_zep_key
```

**Where to get API keys:**

1. **LLM_API_KEY** (Required for demo)
   - **Alibaba Qwen** (recommended): https://bailian.console.aliyun.com/
     - Cheap: ~¥0.50 per test
     - Free trial available
   - **OpenAI**: https://platform.openai.com/api-keys
     - More expensive but reliable
   - **Other**: Any OpenAI-compatible API

2. **ZEP_API_KEY** (Optional, only for full pipeline)
   - https://app.getzep.com/
   - Free tier is sufficient

### Step 4: Run the Demo

```bash
python example_standalone_demo.py
```

Expected output:
```
🐟  🐟  🐟  MiroFish Standalone Ontology Demo
...
1️⃣ Initializing...
   ✓ OpenAI client ready

2️⃣ Loading example text...
   ✓ Loaded 2400 characters

3️⃣ Generating ontology from text...
🔄 Calling LLM API (this may take 20-30 seconds)...
   Model: qwen-plus
   Base URL: https://dashscope.aliyuncs.com/compatible-mode/v1

✓ ONTOLOGY GENERATED SUCCESSFULLY!

📦 ENTITY TYPES (10)

  • Professor
    └─ Academic faculty member
    ...

✅ DEMO COMPLETED SUCCESSFULLY!
```

### Step 5: Check Results

Results saved to `ontology_output.json`:

```bash
cat ontology_output.json | python -m json.tool
```

Should show:
```json
{
  "entity_types": [
    {
      "name": "Professor",
      "description": "Academic faculty member",
      "attributes": [...],
      "examples": [...]
    },
    ...
  ],
  "edge_types": [
    {
      "name": "WORKS_FOR",
      "description": "Employment relationship",
      ...
    }
  ],
  "analysis_summary": "..."
}
```

---

## 🚀 Using the Quick Start Script

Or just run:
```bash
chmod +x QUICK_START.sh
./QUICK_START.sh
```

It will:
- Check Python version
- Verify .env is setup
- Install dependencies
- Run the demo

---

## 🎯 Customizing the Demo

Edit the input text file:

```bash
nano example_data/university_incident.md
```

Then run again:
```bash
python example_standalone_demo.py
```

Your custom ontology will be generated!

---

## ❓ Troubleshooting

### Error: "ModuleNotFoundError: No module named 'openai'"

```bash
# Make sure conda ml environment is activated
conda activate ml

# Install the package
pip install openai

# Verify
python -c "import openai"
```

### Error: "LLM_API_KEY not set in .env file"

```bash
# Check if .env exists
ls -la .env

# Check if it has the key
grep LLM_API_KEY .env

# If not, edit it
nano .env
# Add: LLM_API_KEY=your_key_here
```

### Error: API call fails with auth error

```bash
# Check your API key is correct
grep LLM_API_KEY .env

# Verify you have quota/balance in your API account
# https://bailian.console.aliyun.com/ (for Alibaba)
# https://platform.openai.com/account/billing/overview (for OpenAI)
```

### Script runs very slowly

This is normal! LLM API calls take 20-30 seconds.
- First call: slower (cold start)
- Subsequent calls: faster

### Error: "json.JSONDecodeError"

Sometimes the LLM output isn't valid JSON. The script has fallback handling.
Just run again - usually succeeds on retry.

---

## 📊 What This Demo Does

1. **Reads** example text file (500-word story)
2. **Calls** LLM API to analyze content
3. **Extracts** 10 entity types + 6-10 relationship types
4. **Outputs** structured ontology as JSON
5. **Saves** results to `ontology_output.json`

**Cost**: ~$0.05-0.10 per run

**Time**: ~30 seconds (mostly waiting for LLM)

---

## 🔄 Next Steps

After running the demo successfully:

### Option 1: Custom Data
```bash
# Edit with your own event/text
nano example_data/university_incident.md

# Run again
python example_standalone_demo.py
```

### Option 2: Full Pipeline
Install all backend dependencies:
```bash
cd backend
pip install -r requirements.txt
# or with uv:
uv sync
```

Then run full web interface:
```bash
npm run dev
```

---

## 📚 Files

- `example_standalone_demo.py` - Main demo script (no backend deps)
- `example_minimal_demo.py` - Full demo (needs backend deps)
- `example_data/university_incident.md` - Input text example
- `ontology_output.json` - Generated output
- `QUICK_START.sh` - Automated setup script

---

## 💡 Tips

✅ **Use conda ml environment** - It has most packages you need
✅ **Start small** - The included example is ~500 words, perfect for testing
✅ **Test API keys first** - Make sure they work before running
✅ **Save output** - Check `ontology_output.json` to see results
✅ **Re-run with custom text** - It's fast and cheap to iterate

---

## 🆘 Still Having Issues?

1. Verify Python version:
   ```bash
   python --version  # Should be 3.11+
   ```

2. Verify conda environment:
   ```bash
   conda info --envs | grep ml
   which python  # Should be in conda/envs/ml/
   ```

3. Verify packages installed in right environment:
   ```bash
   conda activate ml
   pip list | grep openai
   ```

4. Test API key manually:
   ```bash
   python -c "
   from openai import OpenAI
   import os
   key = os.getenv('LLM_API_KEY')
   if not key: print('❌ No LLM_API_KEY')
   else: print('✓ API key loaded')
   "
   ```

Still stuck? Check the .env file and API quotas first!

Good luck! 🐟
