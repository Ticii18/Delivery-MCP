const chatContainer = document.getElementById('chatContainer');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const clearBtn = document.getElementById('clearBtn');

// Base de datos simulada
const db = {
    restaurantes: {
        pizza: ['Don Pizza', 'Pizza Fest'],
        sushi: ['Sushinato', 'Sushi Express'],
        hamburguesas: ['Burger Time', 'Big Burger']
    },
    menus: {
        'Don Pizza': ['Pizza Margarita', 'Pizza Napolitana', 'Pizza Cuatro Quesos'],
        'Pizza Fest': ['Pizza Americana', 'Pizza Pepperoni'],
        'Sushinato': ['Sushi Maki', 'Sushi Nigiri', 'Sushi Ebi'],
        'Sushi Express': ['Sushi Salmón', 'Sushi Atún'],
        'Burger Time': ['Hamburguesa Clásica', 'Hamburguesa BBQ'],
        'Big Burger': ['Hamburguesa Doble', 'Hamburguesa de Pollo']
    }
};

function addMessage(content, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.innerHTML = content;
    
    const timestamp = document.createElement('div');
    timestamp.className = 'timestamp';
    const now = new Date();
    timestamp.textContent = now.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
    
    contentDiv.appendChild(timestamp);
    messageDiv.appendChild(contentDiv);
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function showLoading() {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot';
    messageDiv.id = 'loadingMessage';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'loading';
    loadingDiv.innerHTML = '<span></span><span></span><span></span>';
    
    contentDiv.appendChild(loadingDiv);
    messageDiv.appendChild(contentDiv);
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function removeLoading() {
    const loading = document.getElementById('loadingMessage');
    if (loading) loading.remove();
}

function normalizarTexto(texto) {
    return texto.toLowerCase().trim().replace(/[áàäâ]/g, 'a').replace(/[éèëê]/g, 'e').replace(/[íìïî]/g, 'i').replace(/[óòöô]/g, 'o').replace(/[úùüû]/g, 'u');
}

async function procesarMensaje(texto) {
    const lower = normalizarTexto(texto);
    let respuesta = '';

    // Buscar restaurantes - Pizza
    if (lower.includes('pizza')) {
        respuesta = `<strong>🍕 Restaurantes de Pizza:</strong><br><br>` +
            db.restaurantes.pizza.map((r, i) => `${i+1}. ${r}`).join('<br>') +
            `<br><br>¿Cuál te interesa? Puedo mostrarte el menú.`;
    }
    // Buscar restaurantes - Sushi
    else if (lower.includes('sushi')) {
        respuesta = `<strong>🍣 Restaurantes de Sushi:</strong><br><br>` +
            db.restaurantes.sushi.map((r, i) => `${i+1}. ${r}`).join('<br>') +
            `<br><br>¿Cuál prefieres? Dime el nombre para ver el menú.`;
    }
    // Buscar restaurantes - Hamburguesas
    else if (lower.includes('hamburguesa') || lower.includes('burger')) {
        respuesta = `<strong>🍔 Restaurantes de Hamburguesas:</strong><br><br>` +
            db.restaurantes.hamburguesas.map((r, i) => `${i+1}. ${r}`).join('<br>') +
            `<br><br>¿Cuál es tu favorito?`;
    }
    // Ver menú específico
    else if (lower.includes('don pizza')) {
        respuesta = `<strong>📋 Menú de Don Pizza:</strong><br><br>` +
            db.menus['Don Pizza'].map((item, i) => `${i+1}. ${item}`).join('<br>') +
            `<br><br>¿Qué deseas ordenar?`;
    }
    else if (lower.includes('pizza fest')) {
        respuesta = `<strong>📋 Menú de Pizza Fest:</strong><br><br>` +
            db.menus['Pizza Fest'].map((item, i) => `${i+1}. ${item}`).join('<br>') +
            `<br><br>¿Qué deseas ordenar?`;
    }
    else if (lower.includes('sushinato')) {
        respuesta = `<strong>📋 Menú de Sushinato:</strong><br><br>` +
            db.menus['Sushinato'].map((item, i) => `${i+1}. ${item}`).join('<br>') +
            `<br><br>¿Qué deseas ordenar?`;
    }
    else if (lower.includes('sushi express')) {
        respuesta = `<strong>📋 Menú de Sushi Express:</strong><br><br>` +
            db.menus['Sushi Express'].map((item, i) => `${i+1}. ${item}`).join('<br>') +
            `<br><br>¿Qué deseas ordenar?`;
    }
    else if (lower.includes('burger time')) {
        respuesta = `<strong>📋 Menú de Burger Time:</strong><br><br>` +
            db.menus['Burger Time'].map((item, i) => `${i+1}. ${item}`).join('<br>') +
            `<br><br>¿Qué deseas ordenar?`;
    }
    else if (lower.includes('big burger')) {
        respuesta = `<strong>📋 Menú de Big Burger:</strong><br><br>` +
            db.menus['Big Burger'].map((item, i) => `${i+1}. ${item}`).join('<br>') +
            `<br><br>¿Qué deseas ordenar?`;
    }
    // Ver menú genérico
    else if (lower.includes('menu') || lower.includes('menú')) {
        respuesta = `<strong>📋 ¿De qué restaurante quieres ver el menú?</strong><br><br>` +
            `Opciones disponibles:<br>` +
            `🍕 Don Pizza<br>` +
            `🍕 Pizza Fest<br>` +
            `🍣 Sushinato<br>` +
            `🍣 Sushi Express<br>` +
            `🍔 Burger Time<br>` +
            `🍔 Big Burger`;
    }
    // Procesar pedido
    else if (lower.includes('pedir') || lower.includes('orden') || lower.includes('pedido')) {
        respuesta = `<strong>🛒 Procesando tu pedido...</strong><br><br>` +
            `Necesito:<br>` +
            `✓ Nombre del restaurante<br>` +
            `✓ Platos que deseas<br>` +
            `✓ Tu dirección de entrega<br><br>` +
            `¿Cuál es tu dirección?`;
    }
    // Confirmación de dirección
    else if (lower.includes('calle') || lower.includes('avenida') || lower.includes('av.') || 
             lower.includes('numero') || lower.includes('nro') || lower.includes('n°') ||
             lower.includes('casa') || lower.includes('apt') || lower.includes('piso')) {
        respuesta = `<strong>✅ ¡Pedido Confirmado!</strong><br><br>` +
            `📍 Dirección: ${texto}<br>` +
            `⏱️ Tiempo estimado: 30-45 minutos<br>` +
            `💰 Tu pedido será entregado en la dirección indicada<br><br>` +
            `¡Gracias por tu orden! 🎉`;
    }
    // Respuesta por defecto
    else {
        respuesta = `<strong>❓ Opciones disponibles:</strong><br><br>` +
            `🔍 <strong>Buscar restaurantes:</strong><br>` +
            `Prueba: "pizza", "sushi" o "hamburguesas"<br><br>` +
            `📋 <strong>Ver menú:</strong><br>` +
            `Prueba: "Don Pizza", "Sushinato", etc.<br><br>` +
            `🛒 <strong>Hacer pedido:</strong><br>` +
            `Prueba: "Quiero pedir"`;
    }

    return respuesta;
}

async function enviarMensaje() {
    const texto = messageInput.value.trim();
    if (!texto) return;

    addMessage(texto, true);
    messageInput.value = '';
    messageInput.focus();
    
    showLoading();
    
    // Simular delay del servidor
    await new Promise(resolve => setTimeout(resolve, 800));
    
    removeLoading();
    
    const respuesta = await procesarMensaje(texto);
    addMessage(respuesta, false);
}

function limpiarChat() {
    if (confirm('¿Estás seguro de que quieres limpiar la conversación?')) {
        chatContainer.innerHTML = `
            <div class="message bot">
                <div class="message-content">
                    <div class="welcome-message">
                        <h2>¡Conversación Limpia!</h2>
                        <p>¿En qué puedo ayudarte?</p>
                        <p style="margin-top: 15px; font-size: 13px;">💡 Prueba: "pizza", "sushi" o "hamburguesas"</p>
                    </div>
                </div>
            </div>
        `;
        messageInput.focus();
    }
}

sendBtn.addEventListener('click', enviarMensaje);
clearBtn.addEventListener('click', limpiarChat);
messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        enviarMensaje();
    }
});

messageInput.focus();
