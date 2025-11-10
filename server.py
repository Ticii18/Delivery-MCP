# Importamos la clase principal FastMCP que permite crear un servidor MCP (Model Context Protocol)
from mcp.server.fastmcp import FastMCP


# Inicializamos la instancia principal del MCP. 
# "FoodDeliveryMCP" será el identificador del agente MCP y "stateless_http=True" 
# indica que cada solicitud se procesa de forma independiente (sin almacenar contexto entre peticiones).
mcp = FastMCP("FoodDeliveryMCP", stateless_http=True, json_response=True)


# Base de datos simulada (en memoria) con los tipos de comida y restaurantes asociados.
restaurantes_db: dict[str, list[str]] = {
    "pizza": ["Don Pizza", "Pizza Fest"],
    "sushi": ["Sushinato", "Sushi Express"],
    "hamburguesa": ["Burger Time", "Big Burger"]
}


# Base de datos simulada con los menús correspondientes a cada restaurante.
menus_db: dict[str, list[str]] = {
    "Don Pizza": ["Pizza Margarita", "Pizza Napolitana", "Pizza Cuatro Quesos"],
    "Pizza Fest": ["Pizza Americana", "Pizza Pepperoni"],
    "Sushinato": ["Sushi Maki", "Sushi Nigiri", "Sushi Ebi"],
    "Sushi Express": ["Sushi Salmón", "Sushi Atún"],
    "Burger Time": ["Hamburguesa Clásica", "Hamburguesa BBQ"],
    "Big Burger": ["Hamburguesa Doble", "Hamburguesa de Pollo"]
}


# HERRAMIENTAS DEL MCP (TOOLS)
# Cada función decorada con @mcp.tool representa una "herramienta" accesible 
# desde el cliente MCP. Estas herramientas exponen operaciones controladas 
# como buscar restaurantes, ver menús o realizar pedidos.


@mcp.tool("buscar_restaurantes")
def buscar_restaurantes(tipo_comida: str) -> list[str]:
    """
    Busca los restaurantes disponibles según el tipo de comida.
    Comparación insensible a mayúsculas/minúsculas.

    Args:
      tipo_comida (str): Tipo de comida a buscar. Valores esperados: "pizza", "sushi", "hamburguesas".
        Se convierte a minúsculas internamente para evitar problemas de capitalización.

    Returns:
      list[str]: Lista de nombres de restaurantes que coinciden con el tipo de comida.
        Si no hay coincidencias, retorna una lista vacía.
        En caso de excepción inesperada, retorna una lista con un único elemento que describe el error.
    """
    try:
        if not tipo_comida:
            todos_los_restaurantes = []
            for lista_de_tipo in restaurantes_db.values():
                todos_los_restaurantes.extend(lista_de_tipo)
            return todos_los_restaurantes

        tipo_normalizado = tipo_comida.casefold()
        for key in restaurantes_db:
            if key.casefold() == tipo_normalizado:
                return restaurantes_db[key]
        
        return []

    except Exception as e:
        return [f"Error: {e}"]

@mcp.tool("ver_menu")
def ver_menu(restaurante: str) -> list[str]:
    """
    Devuelve el menú del restaurante solicitado (búsqueda case-insensitive).

    Args:
      restaurante (str): Nombre exacto del restaurante, tal como aparece en menus_db.

    Returns:
      list[str]: Lista de platos del menú si el restaurante existe.
        Si el restaurante no existe, retorna ["Error: restaurante no encontrado."].
        En caso de excepción inesperada, retorna ["Error: <detalle>"].

    """
    try:
            if not restaurante:
                return []

            objetivo = None
            buscado = restaurante.casefold()
            for nombre in menus_db.keys():
                if nombre.casefold() == buscado:
                    objetivo = nombre
                    break
            if not objetivo:
                return []

            return menus_db[objetivo]
    except Exception as e:
            return [f"Error: {e}"]


@mcp.tool("realizar_pedido")
def realizar_pedido(items: list[str], direccion: str) -> str:
    """
    Simula el proceso de realizar un pedido y devuelve una confirmación.

    Args:
      items (list[str]): Lista de platos elegidos. Debe contener al menos un elemento.
      direccion (str): Dirección de envío. No puede ser cadena vacía.

    Returns:
      str: Mensaje de confirmación con el resumen del pedido y la dirección de envío.
        Si faltan datos, retorna mensajes de error:
          - "Error: Debes seleccionar al menos un plato."
          - "Error: Falta la dirección de envío."
        En caso de excepción inesperada, retorna "Error: <detalle>".
    """
    try:
        # Validaciones básicas para asegurar datos mínimos del pedido
        if not items:
            return "Error: Debes seleccionar al menos un plato."
        if not direccion:
            return "Error: Falta la dirección de envío."
        
        # Confirmación del pedido como cadena concatenada
        return f"Pedido confirmado: {', '.join(items)} hacia {direccion}. ¡Gracias!"
    except Exception as e:
        return f"Error: {e}"


@mcp.tool("limpiar_chat")
def limpiar_chat() -> str:
    """
    Limpia el contexto de la conversación para iniciar un nuevo pedido.

    Returns:
      str: Mensaje confirmando que la conversación fue reiniciada.

    Notes:
      En modo stateless (stateless_http=True) esto es simbólico, ya que no existe
      sesión persistente del lado del servidor; se ofrece por ergonomía del cliente.
    """
    return "Chat limpio. Nueva conversación iniciada."


@mcp.tool("no_soy_capaz")
def no_soy_capaz(pregunta: str) -> str:
    """
    Responde cuando la consulta del usuario está fuera del alcance de las herramientas disponibles.

    Args:
      pregunta (str): Texto de la consulta fuera de alcance.

    Returns:
      str: Mensaje explicando la limitación de ámbito del servidor MCP.
    """
    return "Esa consulta no es posible: solo ayudo con delivery y menú de restaurantes."


# Punto de entrada principal del script.
# Se ejecuta el servidor MCP usando transporte 'streamable-http', 
# lo que permite comunicación interactiva con clientes compatibles (por ejemplo, APIs o chat UIs).
if __name__ == "__main__":
    mcp.run(transport="streamable-http")
