from mcp.server.fastmcp import FastMCP

mcp = FastMCP("FoodDeliveryMCP", stateless_http=True)

restaurantes_db = {
    "pizza": ["Don Pizza", "Pizza Fest"],
    "sushi": ["Sushinato", "Sushi Express"],
    "hamburguesas": ["Burger Time", "Big Burger"]
}

menus_db = {
    "Don Pizza": ["Pizza Margarita", "Pizza Napolitana", "Pizza Cuatro Quesos"],
    "Pizza Fest": ["Pizza Americana", "Pizza Pepperoni"],
    "Sushinato": ["Sushi Maki", "Sushi Nigiri", "Sushi Ebi"],
    "Sushi Express": ["Sushi Salmón", "Sushi Atún"],
    "Burger Time": ["Hamburguesa Clásica", "Hamburguesa BBQ"],
    "Big Burger": ["Hamburguesa Doble", "Hamburguesa de Pollo"]
}

@mcp.tool("buscar_restaurantes")
def buscar_restaurantes(tipo_comida: str) -> list:
    """
    Busca restaurantes disponibles según el tipo de comida.
    Args:
        tipo_comida (str): "pizza", "sushi", "hamburguesas".
    Returns:
        list: Nombres de restaurantes o vacío.
    """
    try:
        return restaurantes_db.get(tipo_comida.lower(), [])
    except Exception as e:
        return [f"Error: {e}"]

@mcp.tool("ver_menu")
def ver_menu(restaurante: str) -> list:
    """
    Devuelve el menú simulado de un restaurante.
    Args:
        restaurante (str): Nombre exacto.
    Returns:
        list: Platos del menú o error.
    """
    try:
        if restaurante not in menus_db:
            return ["Error: restaurante no encontrado."]
        return menus_db[restaurante]
    except Exception as e:
        return [f"Error: {e}"]

@mcp.tool("realizar_pedido")
def realizar_pedido(items: list, direccion: str) -> str:
    """
    Realiza el pedido simulado y confirma.
    Args:
        items (list): Platos elegidos.
        direccion (str): Dirección de envío.
    Returns:
        str: Confirmación o error.
    """
    try:
        if not items:
            return "Error: Debes seleccionar al menos un plato."
        if not direccion:
            return "Error: Falta la dirección de envío."
        return f"Pedido confirmado: {', '.join(items)} hacia {direccion}. ¡Gracias!"
    except Exception as e:
        return f"Error: {e}"

@mcp.tool("limpiar_chat")
def limpiar_chat() -> str:
    """
    Limpia la conversación. El usuario puede empezar un nuevo pedido.
    Returns:
        str: Mensaje confirmando limpieza.
    """
    return "Chat limpio. Nueva conversación iniciada."

@mcp.tool("no_soy_capaz")
def no_soy_capaz(pregunta: str) -> str:
    """
    Responde si la consulta no tiene relación con herramientas.
    Args:
        pregunta (str): Consulta fuera de alcance.
    Returns:
        str: Mensaje explicando limitación.
    """
    return "Esa consulta no es posible: solo ayudo con delivery y menú de restaurantes."

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
