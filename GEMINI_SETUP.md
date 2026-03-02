# 🤖 Google Gemini API Setup Guide

The AI Data Analyzer now uses **Google Gemini API** for intelligent chatbot analysis. Here's how to set it up:

## Step 1: Get Your Gemini API Key

1. Go to **[Google AI Studio](https://aistudio.google.com/app/apikey)**
2. Click **"Get API Key"** (you may need to sign in with your Google account)
3. Copy your API key - it will look like: `AIza...`

## Step 2: Set the Environment Variable

### **Option A: PowerShell (Windows) - Temporary Session**
```powershell
$env:GEMINI_API_KEY = "your-api-key-here"
python app.py
```

### **Option B: PowerShell (Windows) - Permanent**
```powershell
[Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "your-api-key-here", [EnvironmentVariableTarget]::User)
```
Then restart PowerShell and run:
```powershell
python app.py
```

### **Option C: Command Prompt (CMD)**
```cmd
set GEMINI_API_KEY=your-api-key-here
python app.py
```

### **Option D: Create a .env File**
1. Create a file named `.env` in the project directory:
```
GEMINI_API_KEY=your-api-key-here
```

2. Install python-dotenv:
```bash
pip install python-dotenv
```

3. Update `app.py` to load from .env:
```python
from dotenv import load_dotenv
load_dotenv()
```

## Step 3: Install the Package

Run this command to install the Google Generative AI package:
```bash
pip install google-generativeai
```

Or update all requirements:
```bash
pip install -r requirements.txt
```

## Step 4: Restart the Server

```bash
python app.py
```

You should see:
```
✅ Gemini API key detected - AI chatbot will use Google Gemini
```

## Step 5: Use the AI Chatbot

The chatbot will now use Gemini to answer your questions about the data with full natural language understanding!

### Example Questions:
- "How many total records do we have?"
- "What's the average value for [column name]?"
- "Show me trends over time"
- "Compare these two columns"
- "What insights can you find in this data?"

## Troubleshooting

### ❌ "No GEMINI_API_KEY found"
- Make sure you set the environment variable correctly
- Restart your terminal/PowerShell after setting the variable
- Check: `echo $env:GEMINI_API_KEY` (should display your key)

### ❌ "ModuleNotFoundError: No module named 'google'"
- Install the package: `pip install google-generativeai`

### ✅ Not Working? Fallback Mode
If Gemini API isn't available, the app will automatically use the built-in intelligent analysis engine. The chatbot will still work, just with keyword-based analysis instead of AI.

## Free Usage

Google's Gemini API offers:
- ✅ **Free tier**: 60 requests per minute
- ✅ No credit card required for free usage
- ✅ Great for development and small projects

For more info: https://ai.google.dev/

## Security Notes

⚠️ **Never commit your API key to GitHub!**
- Add `.env` to your `.gitignore`
- Use environment variables instead of hardcoding keys
- If you accidentally expose your key, regenerate it in AI Studio

---

🚀 Happy analyzing with Gemini!
