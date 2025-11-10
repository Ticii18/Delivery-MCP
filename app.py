import json
import requests
import streamlit as st
import re

MCP_URL = "http://localhost:8000/mcp"

def normalize_result(res):
    if isinstance(res, dict):
        sc = res.get("structuredContent")
        if isinstance(sc, dict) and isinstance(sc.get("result"), list):
            return sc["result"]
        content = res.get("content")
        if isinstance(content, list):
            texts = [c.get("text") for c in content 
                    if isinstance(c, dict) and c.get("type") == "text" and c.get("text")]
            if texts:
                return texts
    return res

def render_bulleted_list(title: str, items, icon: str = "•"):
    st.markdown(f"### {title}")
    if isinstance(items, list) and items:
        for it in items:
            st.markdown(f"- {icon} {it}")
    elif isinstance(items, list) and not items:
        st.info("No se encontraron resultados.")
    elif isinstance(items, str):
        st.write(items)
    else:
        st.json(items)

def call_tool(tool_name: str, arguments: dict):
    payload = {
        "jsonrpc": "2.0",
        "id": "1",
        "method": "tools/call",
        "params": {"name": tool_name, "arguments": arguments},
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"
    }
    resp = requests.post(MCP_URL, headers=headers, data=json.dumps(payload), timeout=15)
    resp.raise_for_status()
    data = resp.json()
    if "error" in data:
        raise RuntimeError(data["error"])
    return data.get("result")

st.set_page_config(page_title="FoodDelivery MCP Chat", page_icon="🍕", layout="centered")
st.title("🍕 Chat FoodDelivery MCP")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

prompt = st.chat_input(
    "Pregunta libre: 'dame restaurantes', 'menú Don Pizza', 'menú de hamburguesas', 'pedir Pizza Margarita a Calle 123', etc."
)

def tipo_comida_normalizado(texto):
    # Simplificación: busca keywords más comunes
    tipos = ["pizza", "pizzas", "sushi", "hamburguesa", "hamburguesas"]
    for t in tipos:
        if t in texto:
            return t.rstrip("s")  # quita 's' final para estandarizar con el backend
    return ""

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    reply = ""
    input_text = prompt.lower()
    try:
        # Restaurantes (flexibles)
        if re.search(r"(restaurantes|lista\s*de\s*restaurantes|mostr(a|ame).*restaurantes|dime\s*restaurantes)", input_text):
            # Si menciona tipo de comida: "restaurantes de pizza"/"restaurantes de sushi" etc.
            tipo = tipo_comida_normalizado(input_text)
            result = call_tool("buscar_restaurantes", {"tipo_comida": tipo}) if tipo else call_tool("buscar_restaurantes", {"tipo_comida": ""})
            items = normalize_result(result)
            with st.chat_message("assistant"):
                render_bulleted_list(f"Restaurantes{f' de {tipo}' if tipo else ''}", items, icon="🍽️")

        # Menús (flexibles, distinguir tipo de comida y restaurante)
        elif re.search(r"men[uú]|ver\s*men[uú]|qué hay en|quiero saber el men[uú]", input_text):
            # Buscamos de <tipo> o de <restaurante>
            match_de = re.search(r"men[uú]\s*de\s*([\w\sáéíóúñ]+)", input_text)
            match_en = re.search(r"en\s*([\w\sáéíóúñ]+)", input_text)
            nombre = ""
            if match_de:
                nombre = match_de.group(1).strip()
            elif match_en:
                nombre = match_en.group(1).strip()
            # Si el nombre coincide con tipo, busca restaurantes de ese tipo; si coincide con restaurante, busca menú
            tipo = tipo_comida_normalizado(nombre)
            if tipo:
                result = call_tool("buscar_restaurantes", {"tipo_comida": tipo})
                items = normalize_result(result)
                with st.chat_message("assistant"):
                    render_bulleted_list(f"Restaurantes de {tipo}", items, icon="🍽️")
            else:
                # menú de <restaurante>
                nombre = nombre.replace(" de", "").strip()  # Elimina duplicado si hay doble "de"
                result = call_tool("ver_menu", {"restaurante": nombre})
                items = normalize_result(result)
                with st.chat_message("assistant"):
                    render_bulleted_list(f"Menú de {nombre}", items, icon="🍕")
        # Pedido
        elif re.search(r"(pedir|quiero pedir|haz un pedido|realiza un pedido)", input_text):
            match = re.search(r"(pedir|pedido)\s*(.*?)(?:\s*a\s*)(.+)", prompt, re.IGNORECASE)
            if match:
                items_text = match.group(2).strip()
                direccion = match.group(3).strip()
                items = [s.strip() for s in items_text.split(",") if s.strip()]
                result = call_tool("realizar_pedido", {"items": items, "direccion": direccion})
                with st.chat_message("assistant"):
                    if isinstance(result, str) and result.lower().startswith("error"):
                        st.error(result)
                    else:
                        st.success(result)
            else:
                reply = "Formato esperado: por ejemplo 'pedir Pizza Margarita a Calle 123' o 'haz un pedido de Pizza Margarita a Calle 123'."

        elif re.search(r"(limpiar|reset|empezar de nuevo|nuevo chat)", input_text):
            result = call_tool("limpiar_chat", {})
            st.session_state.messages = []
            with st.chat_message("assistant"):
                st.info(f"{result} (historial local reiniciado)")

        else:
            # fallback: tipo comida suelto
            tipo = tipo_comida_normalizado(input_text)
            if tipo:
                result = call_tool("buscar_restaurantes", {"tipo_comida": tipo})
                items = normalize_result(result)
                with st.chat_message("assistant"):
                    render_bulleted_list(f"Restaurantes de {tipo}", items, icon="🍽️")
            else:
                reply = (
                    "No entendí la consulta. Prueba frases como:\n"
                    "- Mostrame los restaurantes de pizza\n"
                    "- Quiero menú de Don Pizza\n"
                    "- Hazme un pedido de Pizza Margarita a Calle 123"
                )

    except Exception as e:
        reply = f"Error: {e}"

    if reply:
        with st.chat_message("assistant"):
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply or "(renderizado)"})
