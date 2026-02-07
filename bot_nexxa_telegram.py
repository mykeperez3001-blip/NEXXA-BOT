"""
BOT TELEGRAM - NEXXA GLOBAL
Comunidad de IA + Oportunidades de Inversión
Captura leads y envía al grupo de WhatsApp
"""

import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import json
from datetime import datetime

# ============= CONFIGURACIÓN =============

# TOKEN del bot (lo obtienes de @BotFather)
TELEGRAM_BOT_TOKEN = "8199694460:AAFjzFVyjmlPND6UtHX8GD3XsLJqVHgWqJQ"

# Tu información
EMPRESA = "NEXXA GLOBAL"
LINK_GRUPO_WHATSAPP = "https://chat.whatsapp.com/CojyqeFJABl6l4jAMijo0f"
TU_WHATSAPP = "+573223008423"

# Estados de la conversación
ESPERANDO_CONFIRMACION, ESPERANDO_NOMBRE, ESPERANDO_EMAIL, ESPERANDO_TELEFONO, ESPERANDO_PAIS = range(5)

# Base de datos de registros
registros = []

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ============= MENSAJES =============

MENSAJE_BIENVENIDA = """🚀 *¡Bienvenido a NEXXA GLOBAL\\!*

Únete a nuestra comunidad exclusiva donde aprenderás sobre Inteligencia Artificial y tecnologías que están transformando el mundo\\.

💎 *¿Qué obtienes?*
• Contenido diario sobre IA
• Networking con emprendedores
• Herramientas y recursos exclusivos

¿Quieres unirte al grupo VIP? 👇"""

MENSAJE_PEDIR_NOMBRE = """¡Excelente decisión\\! 🎉

Para enviarte el acceso, necesito algunos datos\\.

Primero, dime tu *nombre completo*:"""

MENSAJE_PEDIR_EMAIL = """Gracias \\{nombre\\}\\! 📧

Ahora tu *email*:"""

MENSAJE_PEDIR_TELEFONO = """Perfecto\\! 📱

Dime tu *número de teléfono* \\(con código de país\\):
Ejemplo: \\+573001234567"""

MENSAJE_PEDIR_PAIS = """Genial\\! 🌎

¿De qué *país* nos escribes?"""

MENSAJE_FINAL = """🎊 *¡Bienvenido a NEXXA GLOBAL, \\{nombre\\}\\!*

✅ Registro exitoso

📋 *Tu información:*
👤 {nombre}
📧 {email}
📱 {telefono}
🌎 {pais}

━━━━━━━━━━━━━━━━━

🔥 *AQUÍ ESTÁ TU ACCESO AL GRUPO VIP:*

{link_grupo}

👆 *HAZ CLIC PARA UNIRTE AHORA*

━━━━━━━━━━━━━━━━━

📌 *Instrucciones importantes:*

1\\. Preséntate cuando entres
2\\. Activa las notificaciones
3\\. Participa activamente
4\\. Respeta a la comunidad

━━━━━━━━━━━━━━━━━

💡 *Recuerda:* En este grupo compartiremos conocimiento valioso sobre IA y oportunidades para crecer juntos\\.

¡Nos vemos adentro\\! 🚀

_\\- Equipo NEXXA GLOBAL_"""

# ============= FUNCIONES =============

def guardar_registro(nombre, email, telefono, pais, username, user_id):
    """Guarda el registro del usuario"""
    registro = {
        "nombre": nombre,
        "email": email,
        "telefono": telefono,
        "pais": pais,
        "telegram_username": username,
        "telegram_id": user_id,
        "fecha": datetime.now().isoformat(),
        "hora": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    
    registros.append(registro)
    
    # Guardar en archivo JSON
    try:
        with open('registros_nexxa_telegram.json', 'w', encoding='utf-8') as f:
            json.dump(registros, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error guardando registro: {e}")
    
    return registro

def escape_markdown(text):
    """Escapa caracteres especiales para MarkdownV2"""
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    return text

# ============= COMANDOS =============

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Inicia la conversación"""
    user = update.effective_user
    
    # Teclado con opciones
    keyboard = [['✅ SÍ, QUIERO UNIRME'], ['❌ No, gracias']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(
        MENSAJE_BIENVENIDA,
        reply_markup=reply_markup,
        parse_mode='MarkdownV2'
    )
    
    logger.info(f"Usuario {user.username} ({user.id}) inició el bot")
    
    return ESPERANDO_CONFIRMACION

async def confirmacion(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Procesa la confirmación del usuario"""
    respuesta = update.message.text.lower()
    
    if 'sí' in respuesta or 'si' in respuesta or 'quiero' in respuesta:
        await update.message.reply_text(
            MENSAJE_PEDIR_NOMBRE,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode='MarkdownV2'
        )
        return ESPERANDO_NOMBRE
    else:
        await update.message.reply_text(
            "No hay problema\\! 😊\n\nSi cambias de opinión, escribe /start nuevamente\\.\n\n¡Que tengas un gran día\\!",
            parse_mode='MarkdownV2'
        )
        return ConversationHandler.END

async def recibir_nombre(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Recibe el nombre del usuario"""
    nombre = update.message.text
    context.user_data['nombre'] = nombre
    
    mensaje = MENSAJE_PEDIR_EMAIL.replace('{nombre}', escape_markdown(nombre))
    
    await update.message.reply_text(
        mensaje,
        parse_mode='MarkdownV2'
    )
    
    return ESPERANDO_EMAIL

async def recibir_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Recibe el email del usuario"""
    email = update.message.text
    context.user_data['email'] = email
    
    await update.message.reply_text(
        MENSAJE_PEDIR_TELEFONO,
        parse_mode='MarkdownV2'
    )
    
    return ESPERANDO_TELEFONO

async def recibir_telefono(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Recibe el teléfono del usuario"""
    telefono = update.message.text
    context.user_data['telefono'] = telefono
    
    await update.message.reply_text(
        MENSAJE_PEDIR_PAIS,
        parse_mode='MarkdownV2'
    )
    
    return ESPERANDO_PAIS

async def recibir_pais(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Recibe el país y finaliza el registro"""
    pais = update.message.text
    context.user_data['pais'] = pais
    
    # Obtener datos
    nombre = context.user_data['nombre']
    email = context.user_data['email']
    telefono = context.user_data['telefono']
    user = update.effective_user
    
    # Guardar registro
    guardar_registro(
        nombre=nombre,
        email=email,
        telefono=telefono,
        pais=pais,
        username=user.username or "sin_username",
        user_id=user.id
    )
    
    logger.info(f"✅ NUEVO REGISTRO: {nombre} - {email} - {telefono} - {pais}")
    
    # Enviar mensaje final con link
    mensaje_final = MENSAJE_FINAL.format(
        nombre=escape_markdown(nombre),
        email=escape_markdown(email),
        telefono=escape_markdown(telefono),
        pais=escape_markdown(pais),
        link_grupo=LINK_GRUPO_WHATSAPP
    )
    
    await update.message.reply_text(
        mensaje_final,
        parse_mode='MarkdownV2',
        disable_web_page_preview=False
    )
    
    # Enviar notificación al admin (opcional - requiere configurar)
    # await context.bot.send_message(
    #     chat_id=TU_TELEGRAM_ID,
    #     text=f"🔔 NUEVO REGISTRO\n\n👤 {nombre}\n📧 {email}\n📱 {telefono}\n🌎 {pais}"
    # )
    
    return ConversationHandler.END

async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancela la conversación"""
    await update.message.reply_text(
        "Registro cancelado\\. Si cambias de opinión, escribe /start\\.",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode='MarkdownV2'
    )
    return ConversationHandler.END

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra estadísticas (solo para admin)"""
    total = len(registros)
    hoy = datetime.now().strftime("%Y-%m-%d")
    registros_hoy = len([r for r in registros if r['fecha'].startswith(hoy)])
    
    mensaje = f"""📊 *ESTADÍSTICAS NEXXA GLOBAL*

📋 Total registros: {total}
📅 Registros hoy: {registros_hoy}

🕐 Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M')}"""
    
    await update.message.reply_text(
        escape_markdown(mensaje),
        parse_mode='MarkdownV2'
    )

# ============= MAIN =============

def main():
    """Inicia el bot"""
    
    print("=" * 70)
    print("🤖 BOT NEXXA GLOBAL - TELEGRAM")
    print("=" * 70)
    print(f"📱 Empresa: {EMPRESA}")
    print(f"🔗 Link grupo WhatsApp: {LINK_GRUPO_WHATSAPP}")
    print(f"📊 Registros actuales: {len(registros)}")
    print("=" * 70)
    print("⏳ Iniciando bot...")
    print("=" * 70)
    
    # Crear aplicación
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Configurar conversación
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ESPERANDO_CONFIRMACION: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirmacion)],
            ESPERANDO_NOMBRE: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_nombre)],
            ESPERANDO_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_email)],
            ESPERANDO_TELEFONO: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_telefono)],
            ESPERANDO_PAIS: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_pais)],
        },
        fallbacks=[CommandHandler('cancelar', cancelar)],
    )
    
    # Agregar handlers
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('stats', stats))
    
    # Iniciar bot
    print("✅ Bot iniciado correctamente!")
    print("💡 Busca tu bot en Telegram y escribe /start")
    print("=" * 70)
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
