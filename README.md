# Personal Assistant Chatbot

A full-stack AI chatbot application with React frontend and FastAPI backend, powered by LangGraph and Google Gemini.

## Features

- 💬 Conversational AI with Google Gemini 2.5 Flash
- 🔍 Web search using DuckDuckGo
- 📊 Real-time stock prices
- 🧮 Calculator tool
- 💾 Persistent conversation history with SQLite
- 🧵 Multiple conversation threads
- 🎨 Modern React UI with real-time updates

## Tech Stack

### Backend
- FastAPI
- LangGraph
- LangChain
- Google Gemini API
- SQLite for persistence
- DuckDuckGo Search API
- Alpha Vantage for stock prices

### Frontend
- React 18
- Vite
- Axios
- Lucide React Icons

## Project Structure

```
personal_assistant_chatbot/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── chatbot_engine.py    # LangGraph chatbot logic
│   ├── requirements.txt     # Python dependencies
│   ├── .env                 # Environment variables
│   └── .env.example         # Example environment variables
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── App.css          # Styles
│   │   ├── api.js           # API client
│   │   ├── main.jsx         # Entry point
│   │   └── index.css        # Global styles
│   ├── package.json         # Node dependencies
│   ├── vite.config.js       # Vite configuration
│   └── index.html           # HTML template
└── README.md                # This file
```

## Installation & Setup

### Prerequisites
- Python 3.9+
- Node.js 18+
- Google API Key (for Gemini)
- Alpha Vantage API Key (for stock prices)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Mac/Linux:
```bash
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Configure environment variables:
- Copy `.env.example` to `.env`
- Add your Google API key to `.env`:
```
GOOGLE_API_KEY=your_google_api_key_here
```

6. Run the backend server:
```bash
python main.py
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Usage

1. Start both backend and frontend servers
2. Open your browser to `http://localhost:3000`
3. Start chatting with your personal assistant!

### Available Commands

The chatbot can help you with:
- **Web searches**: "Search for the latest news about AI"
- **Stock prices**: "What's the current price of AAPL stock?"
- **Calculations**: "Calculate 25 * 4 + 100"
- **General questions**: Ask anything!

### Managing Conversations

- Click **+** button to create a new conversation
- Click on a conversation in the sidebar to switch to it
- Click the **trash icon** to delete a conversation

## API Endpoints

### Backend API

- `GET /` - Health check
- `GET /threads` - Get all conversation threads
- `POST /thread/new` - Create a new thread
- `POST /chat` - Send a message
- `GET /conversation/{thread_id}` - Get conversation history
- `DELETE /thread/{thread_id}` - Delete a thread

## Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
GOOGLE_API_KEY=your_google_api_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_langchain_api_key_here
LANGCHAIN_PROJECT=personal-assistant-chatbot
```

### API Keys

1. **Google API Key**: Get it from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Alpha Vantage** (for stocks): Already included in code, or get your own from [Alpha Vantage](https://www.alphavantage.co/support/#api-key)

## Building for Production

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm run build
npm run preview
```

## Troubleshooting

### Backend Issues

1. **Import Errors**: Make sure all dependencies are installed
```bash
pip install -r requirements.txt
```

2. **Database Errors**: Delete `chatbot.db` and restart the server

3. **API Key Errors**: Verify your `.env` file has the correct keys

### Frontend Issues

1. **Connection Errors**: Ensure backend is running on port 8000

2. **CORS Errors**: Check that CORS is properly configured in `main.py`

3. **Build Errors**: Clear node_modules and reinstall
```bash
rm -rf node_modules package-lock.json
npm install
```

## Development

### Backend Development

The backend uses FastAPI with hot reload enabled. Any changes to Python files will automatically restart the server.

### Frontend Development

Vite provides hot module replacement (HMR). Changes to React components will update instantly.

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License

## Author

Kumar Abhishek

## Acknowledgments

- LangChain & LangGraph for the conversational AI framework
- Google for Gemini API
- FastAPI for the excellent backend framework
- React team for the amazing frontend library
