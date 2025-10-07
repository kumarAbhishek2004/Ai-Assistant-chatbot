# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Backend Setup (2 minutes)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# The .env file is already configured with your API keys
# Start the server
python main.py
```

✅ Backend should now be running on http://localhost:8000

### Step 2: Frontend Setup (2 minutes)

Open a **new terminal** window:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

✅ Frontend should now be running on http://localhost:3000

### Step 3: Start Chatting! (1 minute)

1. Open your browser to http://localhost:3000
2. Type a message in the input box
3. Press Enter or click Send

## 📝 Example Prompts to Try

```
"Search for the latest news about artificial intelligence"
"What's the stock price of Tesla?"
"Calculate 1234 multiplied by 5678"
"Tell me a joke"
"What's the weather like today?"
```

## 🔧 Troubleshooting

### Backend won't start?
- Make sure Python 3.9+ is installed: `python --version`
- Check if port 8000 is free
- Verify .env file exists with GOOGLE_API_KEY

### Frontend won't start?
- Make sure Node.js is installed: `node --version`
- Try deleting node_modules and reinstalling: `rm -rf node_modules && npm install`
- Check if port 3000 is free

### Can't connect to backend?
- Verify backend is running on http://localhost:8000
- Check browser console for errors
- Try accessing http://localhost:8000 directly (should see {"message": "Personal Assistant Chatbot API"})

## 📂 File Structure

```
personal_assistant_chatbot/
├── backend/
│   ├── main.py              ← FastAPI routes
│   ├── chatbot_engine.py    ← LangGraph logic
│   ├── requirements.txt     ← Python packages
│   ├── .env                 ← Your API keys
│   └── chatbot.db          ← SQLite database (auto-created)
│
└── frontend/
    ├── src/
    │   ├── App.jsx          ← Main UI component
    │   ├── api.js           ← Backend API calls
    │   └── App.css          ← Styles
    └── package.json         ← Node packages
```

## 🎯 Next Steps

- Create multiple conversation threads using the **+** button
- Switch between conversations using the sidebar
- Delete old conversations with the trash icon
- Try different types of questions!

## 💡 Tips

- The chatbot remembers conversation context within each thread
- Web searches are powered by DuckDuckGo
- Stock prices are real-time from Alpha Vantage
- The calculator supports: add, sub, mul, div operations

## 🆘 Need Help?

Check the main README.md for detailed documentation.
