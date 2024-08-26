import pystray
import asyncio
from pystray import MenuItem as item
from PIL import Image
import threading
import sys
import discord
from variables import TOKEN, SERVER_ID
from audio import show_messages,configurarEventos
from comandos import bot,configurarBotones

def quit_program(icon, item):
    """Función para detener el cliente de Discord y salir del programa."""
    print("Cerrando el bot de Discord...")
    asyncio.run_coroutine_threadsafe(bot.close(), bot.loop)  # Detener el bot de Discord
    icon.stop()  # Detener el icono de la bandeja del sistema
    sys.exit(0)  # Salir del programa

def setup(icon):
    icon.visible = True

def run_bot():
    bot.run(TOKEN)

@bot.event
async def on_ready():
    print(f'Conectado como {bot.user}')
    try:
        # Sincronizar comandos globales y del servidor
        synced = await bot.tree.sync()  # Sincroniza globalmente
        await configurarBotones(bot)
        print(f'Sincronizado globalmente con {len(synced)} comandos')
        guild = discord.Object(id=SERVER_ID)  # Reemplaza con el ID del servidor
        synced_guild = await bot.tree.sync(guild=guild)  # Sincroniza en el servidor específico
        print(f'Sincronizado en el servidor con ID {SERVER_ID}')
        print(f'Sincronizado en el servidor con {len(synced_guild)} comandos')
        print('Bot listo')
    except Exception as e:
        print(f'Error al sincronizar comandos: {e}')



if __name__ == "__main__":
    
    configurarEventos(bot)
    # Crear un icono para la bandeja del sistema
    image = Image.open("icon.ico")
    menu = (
        item('Mostrar Mensajes', show_messages),
        item('Salir', quit_program),
    )
    icon = pystray.Icon("TTS", image, "TTS", menu)

    # Ejecutar el bot en un hilo separado
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()

    # Mostrar el icono de la bandeja del sistema
    icon.run(setup)
