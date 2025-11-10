import streamlit as st
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=api_key)

client = MultiServerMCPClient({
    "demo": {
        "transport": "streamable_http",
        "url": "http://localhost:8000/mcp",
    }
})

# === FUNCIONES ASÍNCRONAS ===
async def get_agent():
    tools = await client.get_tools()
    agent = create_agent(model, tools)
    return agent

async def run_agent(agent, chat_history):
    # Convertir historial de Streamlit en formato LangChain
    messages = [{"role": m["role"], "content": m["content"]} for m in chat_history]

    response = await agent.ainvoke(
        {"messages": messages},
        stream_mode="messages"
    )

    full_response = ""
    for (message, metadata) in response:
        if hasattr(message, "content"):
            msg_content = message.content
            if isinstance(msg_content, list):
                # ✅ Evita duplicación de listas anidadas
                for item in msg_content:
                    if isinstance(item, dict) and "text" in item:
                        full_response += item["text"] + "\n"
                    elif isinstance(item, str):
                        full_response += item + "\n"
            else:
                full_response += str(msg_content) + "\n"
        else:
            full_response += str(message) + "\n"

    return full_response.strip()

# === INTERFAZ DE STREAMLIT ===
st.set_page_config(page_title="Chat FoodDelivery MCP", page_icon="🍕", layout="centered")


if "messages" not in st.session_state:
    st.session_state.messages = []


col1, col2 = st.columns([3,1])
with col1:
    st.title("🍕 Chat FoodDelivery MCP")
with col2:
    if st.button("🧹 Limpiar chat"):
        st.session_state.messages = []
        st.rerun()

st.write("Ejemplo: 'quiero una pizza americana de Pizza Fest', luego 'mandalo a Napoleón Uriburu' — el agente recordará el contexto y completará el pedido.")

# Mostrar historial
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada del usuario
if user_input := st.chat_input("Escribe tu mensaje..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("_Pensando..._")

        try:
            agent = asyncio.run(get_agent())
            response_text = asyncio.run(run_agent(agent, st.session_state.messages))
            message_placeholder.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
        except Exception as e:
            message_placeholder.markdown(f"⚠️ Error: {e}")
