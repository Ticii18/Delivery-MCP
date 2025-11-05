1. Objetivo General
El objetivo de este trabajo es aplicar de forma integral los conocimientos adquiridos en la
materia (especialmente en las Unidades 2 a 5) para diseñar, desarrollar y documentar una
solución de software basada en IA que resuelva un "caso de uso de la vida real".
El entregable final no es solo un trabajo académico, sino la idea es que el estudiante, tenga
un proyecto de portfolio profesional, listo para ser demostrado a futuros empleadores.
2. Requerimientos Comunes (Obligatorios para TODOS los proyectos)
Independientemente del tema que elijan, todos los grupos deben entregar lo siguiente:
1. Repositorio en GitHub:
○ El proyecto debe estar en un repositorio público de GitHub.
○ El enlace al repositorio será el entregable principal.
2. README.md:
○ Este es el documento más importante para un portfolio. Debe incluir:
1. Título del Proyecto: Claro y profesional.
2. Descripción del Problema: Explicar el "caso de la vida real" que
están solucionando y para quién.
3. Demo (GIF Animado): Una demostración visual corta (5-10
segundos) de la aplicación funcionando. Es fundamental.
4. Stack Tecnológico: Listar las librerías, modelos y frameworks clave
(Ej: PyTorch, LangChain, ChromaDB, Ollama, Gemini SDK,
Streamlit).
5. Instrucciones de Instalación: Cómo un tercero puede clonar el repo e
instalar las dependencias (debe incluir un archivo requirements.txt).
6. Instrucciones de Uso: Cómo ejecutar la aplicación (Ej: streamlit run
app.py).
3. Archivo requirements.txt:
○ Un archivo de texto simple con todas las librerías de Python necesarias
(generado con pip freeze > requirements.txt).

4. Código Fuente (.py o .ipynb):
○ El código debe estar comentado, explicando las decisiones de diseño más
importantes.
○ Se valora la separación del código en archivos lógicos (ej. app.py, utils.py,
rag_core.py).


2. MCP (Model Context Protocol)
Requisitos:
● El sistema debe contar con una interfaz de chat simple
● Todas las herramientas deben estar documentadas, con descripciones para cada
argumento. En caso de usar salida estructurada para las herramientas, documentarlas
también.
● El sistema debe manejar los errores que pudieran ocurrir en las herramientas. Debe
retornarse un mensaje que el modelo pueda usar para avisar al usuario y/o reintentar la
llamada con otros argumentos.
● El sistema no debe responder consultas que no tengan que ver con su tarea. En su
lugar, debe explicar por qué la tarea es imposible con las herramientas que tiene
disponibles.
● El sistema debe tener un botón de limpieza de chat, para comenzar una nueva
conversación.

● Agente de Pedidos de Comida (Delivery):
○ Intención: Un cliente quiere pedir comida.
○ Herramientas (Tools): buscar_restaurantes(tipo_comida),
ver_menu(restaurante), realizar_pedido(items, direccion).
○ Requerimientos:

i. El sistema debe permitir a un cliente acceder a una lista de restaurantes
disponibles.
ii. El sistema debe permitir a un cliente consultar el menú de cada
restaurante (simulado).
iii. El sistema tomará el pedido del cliente y le preguntará su dirección
para realizar el pedido (simulado).

