from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from langchain_core.tools import tool
from dotenv import load_dotenv
from ddgs import DDGS  # ✅ Updated import
import sqlite3
import requests
import os

# -------------------- LOAD ENV --------------------
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# -------------------- LLM INITIALIZATION --------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=api_key,
)

# -------------------- TOOLS --------------------

@tool
def duckduckgo_search(query: str, max_results: int = 5) -> str:
    """
    Search DuckDuckGo and return summarized text for the model.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        if not results:
            return "Sorry, I couldn't find any top news related to that topic."
        # Format title + URL for each result
        formatted = "\n".join([f"- {r['title']}: {r['href']}" for r in results if r.get("title") and r.get("href")])
        return formatted
    except Exception as e:
        return f"An error occurred: {e}"


@tool
def calculator(first_num: float, second_num: float, operation: str) -> dict:
    """
    Perform a basic arithmetic operation on two numbers.
    Supported operations: add, sub, mul, div
    """
    try:
        if operation == "add":
            result = first_num + second_num
        elif operation == "sub":
            result = first_num - second_num
        elif operation == "mul":
            result = first_num * second_num
        elif operation == "div":
            if second_num == 0:
                return {"error": "Division by zero is not allowed"}
            result = first_num / second_num
        else:
            return {"error": f"Unsupported operation '{operation}'"}

        return {
            "first_num": first_num,
            "second_num": second_num,
            "operation": operation,
            "result": result,
        }
    except Exception as e:
        return {"error": str(e)}


@tool
def get_stock_price(symbol: str) -> dict:
    """
    Fetch latest stock price for a given symbol (e.g. 'AAPL', 'TSLA') 
    using Alpha Vantage API.
    """
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=C9PE94QUEW9VWGFM"
    try:
        r = requests.get(url)
        return r.json()
    except Exception as e:
        return {"error": str(e)}


# -------------------- COMBINE TOOLS --------------------
tools = [duckduckgo_search, get_stock_price, calculator]
llm_with_tools = llm.bind_tools(tools)

# -------------------- GRAPH STATE --------------------
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# -------------------- NODES --------------------
def chat_node(state: ChatState):
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


def tool_node(state: ChatState):
    messages = state["messages"]
    last_message = messages[-1]
    tool_calls = getattr(last_message, "tool_calls", [])

    if not tool_calls:
        return {"messages": []}

    tool_messages = []
    for tool_call in tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        tool_id = tool_call["id"]

        # Execute the correct tool
        tool_result = None
        for t in tools:
            if t.name == tool_name:
                try:
                    tool_result = t.invoke(tool_args)
                except Exception as e:
                    tool_result = {"error": str(e)}
                break

        tool_message = ToolMessage(content=str(tool_result), tool_call_id=tool_id)
        tool_messages.append(tool_message)

    return {"messages": tool_messages}


def tools_condition(state: ChatState):
    messages = state["messages"]
    if not messages:
        return "__end__"

    last_message = messages[-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return "__end__"

# -------------------- CHECKPOINT + GRAPH --------------------
conn = sqlite3.connect(database="chatbot.db", check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_node("tools", tool_node)

graph.add_edge(START, "chat_node")
graph.add_conditional_edges(
    "chat_node",
    tools_condition,
    {"tools": "tools", "__end__": END},
)
graph.add_edge("tools", "chat_node")

chatbot = graph.compile(checkpointer=checkpointer)

# -------------------- THREAD MANAGEMENT --------------------
def retrieve_all_threads():
    all_threads = {}
    i = 1
    for checkpoint in checkpointer.list(None):
        cfg = checkpoint.config.get("configurable", {})
        thread_id = cfg.get("thread_id")
        name = cfg.get("name")

        if not name:
            try:
                config = {"configurable": {"thread_id": thread_id}}
                state = chatbot.get_state(config=config)
                messages = state.values.get("messages", []) if state.values else []

                for msg in messages:
                    if isinstance(msg, HumanMessage):
                        name = msg.content[:50] + "..." if len(msg.content) > 50 else msg.content
                        chatbot.update_state(
                            config={"configurable": {"thread_id": thread_id, "name": name}},
                            values=None,
                        )
                        break

                if not name:
                    name = f"Chat {i}"

            except Exception as e:
                print(f"Error generating name for thread {thread_id}: {e}")
                name = f"Chat {i}"

        all_threads[thread_id] = name
        i += 1

    return all_threads

# -------------------- TEST --------------------
if __name__ == "__main__":
    # Thread config for checkpointer
    config = {"configurable": {"thread_id": "ai-news"}}

    # User query
    user_message = HumanMessage(content="AI latest news 2025")

    # Invoke chatbot
    response = chatbot.invoke(
        {"messages": [user_message]},
        config=config,
    )

    # Extract only the content from the first message in response
    if response and "messages" in response:
        for msg in response["messages"]:
           
            print(msg.content)