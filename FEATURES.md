# Features Documentation

## Core Features

### 🤖 AI Capabilities

1. **Conversational AI**
   - Powered by Google Gemini 2.5 Flash Lite
   - Context-aware responses
   - Natural language understanding
   - Multi-turn conversations

2. **Tool Integration**
   - **Web Search**: Real-time web search via DuckDuckGo
   - **Stock Prices**: Live stock quotes from Alpha Vantage
   - **Calculator**: Arithmetic operations (add, subtract, multiply, divide)

3. **Smart Tool Selection**
   - Automatically chooses the right tool for the query
   - Seamless tool chaining
   - Fallback to general knowledge when tools aren't needed

### 💬 Conversation Management

1. **Multiple Threads**
   - Create unlimited conversation threads
   - Each thread maintains its own context
   - Easy switching between conversations

2. **Persistent History**
   - All conversations saved to SQLite database
   - Resume conversations anytime
   - Full message history preserved

3. **Thread Naming**
   - Auto-generated names from first message
   - Preview shows first 25 characters
   - Identifies conversations at a glance

4. **Thread Operations**
   - Create new threads
   - Delete individual threads
   - Load previous conversations
   - Export thread data (via API)

### 🎨 User Interface

1. **Modern Design**
   - Clean, intuitive interface
   - Responsive layout
   - Dark sidebar with light chat area
   - Smooth animations

2. **Real-time Updates**
   - Live message streaming
   - Loading indicators
   - Status updates for tool usage
   - Auto-scroll to latest message

3. **Message Display**
   - Clear user/assistant distinction
   - Formatted messages
   - Word wrapping for long text
   - Proper spacing and readability

4. **Sidebar Navigation**
   - Conversation list
   - Quick thread switching
   - Delete buttons per thread
   - New chat button

### ⚡ Performance

1. **Fast Response Times**
   - Streaming responses
   - Optimized API calls
   - Efficient state management
   - Minimal re-renders

2. **Resource Efficiency**
   - Lazy loading of conversations
   - Pagination support (ready to implement)
   - Optimized database queries
   - Memory-efficient state handling

### 🔒 Data & Privacy

1. **Local Storage**
   - SQLite database on your machine
   - No cloud storage of conversations
   - Full data control
   - Easy backup (just copy .db file)

2. **API Key Security**
   - Environment variables for keys
   - .gitignore prevents key commits
   - Example files for safe sharing

### 🛠️ Developer Features

1. **RESTful API**
   - Well-documented endpoints
   - JSON request/response
   - CORS configured
   - Error handling

2. **Modular Architecture**
   - Separate frontend/backend
   - Reusable components
   - Easy to extend
   - Clear separation of concerns

3. **Hot Reload**
   - Backend auto-restart on changes
   - Frontend HMR (Hot Module Replacement)
   - Instant feedback during development

4. **Type Safety**
   - Pydantic models for API
   - PropTypes ready (can be added)
   - Strong validation

## Example Use Cases

### 1. Research Assistant
```
You: "Search for the latest developments in quantum computing"
Assistant: *Uses DuckDuckGo* → Provides recent findings
```

### 2. Stock Market Helper
```
You: "What's the current price of Apple stock?"
Assistant: *Uses Alpha Vantage* → Returns AAPL price data
```

### 3. Math Helper
```
You: "Calculate 1234 multiplied by 5678"
Assistant: *Uses calculator tool* → Returns 7,006,652
```

### 4. General Knowledge
```
You: "Explain how photosynthesis works"
Assistant: *Uses LLM knowledge* → Detailed explanation
```

### 5. Mixed Queries
```
You: "Search for Tesla stock news and tell me the current price"
Assistant: *Uses search + stock tool* → Comprehensive response
```

## Technical Capabilities

### Backend (FastAPI)

**Endpoints:**
- `GET /` - API health check
- `GET /threads` - List all conversation threads
- `POST /thread/new` - Create new conversation
- `POST /chat` - Send message & get AI response
- `GET /conversation/{thread_id}` - Get full conversation history
- `DELETE /thread/{thread_id}` - Delete specific thread

**Features:**
- Async/await support
- Request validation with Pydantic
- Automatic API documentation (Swagger UI)
- Error handling and logging
- CORS middleware for cross-origin requests

### Frontend (React)

**Components:**
- `App.jsx` - Main application component
- Sidebar - Thread management
- Chat area - Message display
- Input form - Message submission

**State Management:**
- React hooks (useState, useEffect, useRef)
- Local state for messages
- API integration with Axios
- Optimistic UI updates

**Styling:**
- Custom CSS with modern design
- Flexbox layouts
- Smooth transitions
- Responsive scrolling
- Custom scrollbars

### Database (SQLite)

**Schema:**
- Managed by LangGraph checkpointer
- Stores conversation threads
- Maintains message history
- Thread metadata (names, IDs)

**Operations:**
- Automatic checkpoint creation
- Thread-based isolation
- Efficient querying
- Easy backup/restore

## Extensibility

### Add New Tools

```python
# In chatbot_engine.py

@tool
def your_new_tool(parameter: str) -> dict:
    """
    Description of what your tool does
    """
    # Your implementation
    return {"result": "value"}

# Add to tools list
tools = [search_tool, get_stock_price, calculator, your_new_tool]
```

### Add New API Endpoints

```python
# In main.py

@app.post("/your-endpoint")
async def your_function(request: YourModel):
    # Your implementation
    return {"response": "data"}
```

### Customize UI

```css
/* In App.css */

.your-custom-class {
    /* Your styles */
}
```

```jsx
// In App.jsx

function YourNewComponent() {
    return <div>Your component</div>;
}
```

## Limitations & Future Enhancements

### Current Limitations

1. No user authentication
2. Single-user design
3. No file uploads
4. No image generation
5. No voice input/output
6. Limited error recovery

### Planned Enhancements

1. **User Authentication**
   - Multi-user support
   - Login/signup system
   - User-specific threads

2. **Advanced Features**
   - File upload support
   - Image analysis
   - Voice input/output
   - Export conversations (PDF, TXT)

3. **UI Improvements**
   - Markdown rendering
   - Code syntax highlighting
   - Message reactions
   - Thread tags/categories

4. **Performance**
   - Message pagination
   - Virtual scrolling
   - Response caching
   - Rate limiting

5. **Deployment**
   - Docker containerization
   - Cloud deployment guides
   - PostgreSQL migration
   - Environment configs

6. **Monitoring**
   - Usage analytics
   - Error tracking
   - Performance metrics
   - LangSmith integration (already configured)

## API Response Examples

### Thread List Response
```json
{
  "threads": [
    {
      "thread_id": "abc-123-def-456",
      "name": "Search for AI news..."
    },
    {
      "thread_id": "xyz-789-uvw-012",
      "name": "Stock price inquiry"
    }
  ]
}
```

### Chat Response
```json
{
  "response": "According to my search, the latest developments...",
  "thread_id": "abc-123-def-456"
}
```

### Conversation History
```json
{
  "messages": [
    {
      "role": "user",
      "content": "Hello!"
    },
    {
      "role": "assistant",
      "content": "Hi! How can I help you today?"
    }
  ]
}
```

## Tool Examples

### Web Search Tool
```python
search_tool = DuckDuckGoSearchRun(region="us-en")
# Automatically searches when query needs current information
```

### Stock Price Tool
```python
@tool
def get_stock_price(symbol: str) -> dict:
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=KEY"
    response = requests.get(url)
    return response.json()
```

### Calculator Tool
```python
@tool
def calculator(first_num: float, second_num: float, operation: str) -> dict:
    operations = {
        "add": first_num + second_num,
        "sub": first_num - second_num,
        "mul": first_num * second_num,
        "div": first_num / second_num if second_num != 0 else "error"
    }
    return {"result": operations.get(operation)}
```

## Configuration Options

### Backend Configuration
```python
# main.py
app = FastAPI(
    title="Personal Assistant Chatbot API",
    version="1.0.0",
    description="AI-powered chatbot with tools"
)

# CORS settings
allow_origins=["http://localhost:3000", "http://localhost:5173"]
```

### Frontend Configuration
```javascript
// api.js
const API_BASE_URL = 'http://localhost:8000';

// vite.config.js
export default defineConfig({
  server: {
    port: 3000
  }
})
```

### Environment Variables
```bash
# .env
GOOGLE_API_KEY=your_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_key_here
LANGCHAIN_PROJECT=personal-assistant-chatbot
```

## Best Practices

### For Users
1. Start conversations with clear questions
2. Use specific queries for better tool selection
3. Create separate threads for different topics
4. Delete old threads to keep sidebar clean
5. Backup chatbot.db regularly

### For Developers
1. Keep API keys in .env file
2. Test changes with hot reload
3. Use meaningful commit messages
4. Document new features
5. Handle errors gracefully
6. Validate user inputs
7. Keep dependencies updated

## Support & Resources

- **README.md** - Comprehensive setup guide
- **QUICKSTART.md** - 5-minute quick start
- **PROJECT_SUMMARY.md** - Project overview
- **This file (FEATURES.md)** - Feature documentation

For issues:
1. Check terminal for errors
2. Review browser console
3. Verify API keys in .env
4. Ensure both servers are running
5. Check port availability (8000, 3000)
