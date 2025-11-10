# Delivery MCP — Agente de Pedidos (HTML + JavaScript frontend)

Proyecto de ejemplo que expone un servidor MCP (Model Context Protocol) en
Python y una interfaz cliente ligera implementada con HTML y JavaScript
(archivos: `index.html`, `app.js`, `styles.css`). Este repositorio NO usa
Streamlit: la UI está en la carpeta raíz como archivos estáticos.

---

## Descripción del problema (caso de la vida real)

Problema real: muchos restaurantes pequeños, foodtrucks y comercios locales
reciben pedidos de múltiples canales (teléfono, WhatsApp, redes sociales) y
no cuentan con una solución técnica mínima para centralizar y automatizar
esas órdenes. El resultado es pérdida de pedidos, errores de toma de nota,
tiempos de preparación imprecisos y esfuerzo manual administrativo.

Casos concretos:
- Un restaurante recibe llamadas y mensajes con pedidos simultáneos y debe
  anotar todo manualmente en papel o en hojas de cálculo.
- Un foodtruck quiere ofrecer un menú actualizado en su web y recibir pedidos
  sin pagar por una plataforma de terceros.

Público objetivo:
- Propietarios de restaurantes pequeños y negocio local (sin equipo dev).
- Equipos técnicos que buscan un prototipo rápido para integrar menús y pedidos.


Beneficios que proporciona este proyecto:
- Probar en minutos un flujo completo (buscar por tipo, ver menú, realizar
  pedido) sin montar infraestructura compleja.
- Evitar errores de transcripción al centralizar peticiones en un agente.
---

## Qué hay en este repositorio

- `index.html` — interfaz web (HTML) que carga `app.js`.
- `app.js` — lógica cliente en JavaScript: realiza peticiones JSON-RPC HTTP al
  servidor MCP para listar restaurantes, ver menús y simular pedidos.
- `styles.css` — estilos para la interfaz web.
- `server.py` — servidor MCP (herramientas: `buscar_restaurantes`, `ver_menu`,
  `realizar_pedido`, `limpiar_chat`, `no_soy_capaz`).
- `requirements.txt` — dependencias de Python para ejecutar `server.py`.

---

## Stack tecnológico

- Frontend: HTML + JavaScript (Vanilla JS). No se requiere Node para ejecutar la
  UI si la abres como archivo estático, aunque en algunos casos es preferible
  servirla desde un servidor HTTP local para evitar problemas de CORS.
- Backend: Python con `mcp` (servidor MCP) y `requests` (en client-side si se usa
  desde Python). El servidor se lanza con `mcp.run(transport="streamable-http")`.

---

## Instalación (rápida)

Clona el repositorio y crea un entorno virtual, luego instala dependencias:

```bash
git clone https://github.com/Ticii18/Delivery-MCP
cd Delivery-MCP
uv venv env
source env/Scripts/activate   # en bash sobre Windows
uv pip install -r requirements.txt
```

Si no tienes `requirements.txt` actualizado, genera uno desde tu entorno:

```bash
uv pip freeze > requirements.txt
```

---


## API / Herramientas MCP (resumen)

Estas herramientas están expuestas por `server.py` y el frontend las consume
mediante JSON-RPC HTTP.

- buscar_restaurantes(tipo_comida: str) -> list
  - Devuelve una lista de restaurantes para el tipo dado (ej.: "pizza").

- ver_menu(restaurante: str) -> list
  - Devuelve el menú del restaurante o un mensaje de error si no existe.

- realizar_pedido(items: list, direccion: str) -> str
  - Valida que haya al menos un item y una dirección; devuelve confirmación.

- limpiar_chat() -> str
  - Limpia la conversación (simbólico en modo stateless).

- no_soy_capaz(pregunta: str) -> str
  - Mensaje cuando la consulta está fuera del alcance.

---

## Manejo común de problemas

- Si la UI no recibe respuesta, confirma que `python server.py` esté corriendo.
- Si el navegador bloquea peticiones por CORS, sirve `index.html` con
  `python -m http.server` u otro servidor estático local.
- Si ves errores del tipo `Bad Request: Missing session ID`, revisa que el
  servidor esté en modo `stateless_http` en `server.py` (así evita requerir
  cabeceras de sesión del cliente).

---

## Pruebas rápidas (manual)

1. Buscar restaurantes por tipo: desde la UI, pedir "sushi" → debería aparecer
   `Sushinato` y `Sushi Express`.
2. Ver menú: pedir menú de `Don Pizza` → listará las pizzas definidas en
   `menus_db`.
3. Realizar pedido: seleccionar items y dar una dirección → recibirás una
   confirmación simulada.

---

## Demo (GIF)

// [GIF]

---
