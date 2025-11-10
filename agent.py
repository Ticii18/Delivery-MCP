from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=api_key)

client = MultiServerMCPClient(
    {
        "demo": {
            "transport": "streamable_http",
            "url": "http://localhost:8000/mcp",
        }
    }
)

async def invoke_agent():
    tools = await client.get_tools()
    agent = create_agent(model, tools)
    while True:
        user_text = input("Tú (escribe 'salir' para terminar): ").strip()
        if not user_text:
            continue
        if user_text.lower() in ("salir", "exit", "quit"):
            print("Saliendo...")
            break

        response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": user_text}]},
            stream_mode="messages"
        )

        for (message, metadata) in response:
            try:
                message.pretty_print()
            except Exception:
                print(message)
if __name__ == "__main__":
    import asyncio
    asyncio.run(invoke_agent())