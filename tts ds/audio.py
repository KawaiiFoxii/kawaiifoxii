import pyttsx3
from tkinter import scrolledtext
import tkinter as tk
from variables import *
import discord

messages = []
last_message_count = 0

# Inicializar el motor de texto a voz
engine = pyttsx3.init()


def update_messages(text_area):
    """Actualizar el área de texto con los mensajes más recientes."""
    global last_message_count
    text_area.config(state=tk.NORMAL)  # Habilitar la edición temporalmente para actualizar el texto
    # Agregar solo nuevos mensajes
    new_messages = messages[last_message_count:]
    for msg in new_messages:
        text_area.insert(tk.END, msg + '\n')
    text_area.yview(tk.END)  # Desplazar al final del área de texto
    text_area.config(state=tk.DISABLED)  # Deshabilitar la edición para hacer el área solo de lectura
    # Actualizar el conteo de mensajes
    last_message_count += len(new_messages)
    text_area.after(1000, update_messages, text_area)  # Actualizar cada 1 segundo
    
def show_messages(icon, item):
    """Función para mostrar una ventana con todos los mensajes."""
    root = tk.Tk()
    root.title("Mensajes Leídos")

    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20, state=tk.DISABLED)
    text_area.pack(expand=True, fill='both')

    # Iniciar la actualización en tiempo real
    update_messages(text_area)

    root.mainloop()



def speak(text):
    """Función para convertir texto en voz."""
    engine.setProperty('rate', 120)  # Velocidad de habla
    """Cambiar voz"""
    engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0')

    engine.say(text)
    engine.runAndWait()


def configurarEventos(client):    

    @client.event
    async def on_message(message):
        # Ignorar mensajes del propio bot
        if message.author == client.user:
            return

        if message.author.id == 241737361220698112:
            return
        # Verificar que el mensaje proviene del canal específico
        if message.channel.id == CHANNEL_ID:
            print(f'#{message.channel.name} ||  {message.author.name}: {message.content}')
            messages.append(f'#{message.channel.name} ||  {message.author.name}: {message.content}') 
            speak(message.content)