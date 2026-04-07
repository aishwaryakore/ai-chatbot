from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver
from dotenv import load_dotenv
from typing import TypedDict, Annotated
import sqlite3

load_dotenv()

llm = ChatOpenAI()

class ChatbotState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state : ChatbotState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {'messages' : [response]}

db_connection = sqlite3.connect(database='chatbot.db', check_same_thread=False)

checkpointer = SqliteSaver(conn=db_connection)

graph = StateGraph(ChatbotState)

graph.add_node('chat_node', chat_node)

graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatbot = graph.compile(checkpointer=checkpointer)

def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return list(all_threads)
