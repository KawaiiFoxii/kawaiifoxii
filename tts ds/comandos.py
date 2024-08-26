import discord
from discord.ext import commands
from discord.ui import Button, View,Modal,TextInput
from torneo import verificarIngreso,guardarIngreso,eliminarIngreso

# Crear Intents y habilitar el mensaje de contenido
intents = discord.Intents.default()
intents.message_content = True  # Asegúrate de habilitar el intent de contenido de mensajes

# Crear una instancia de Bot con los intents configurados
bot = commands.Bot(command_prefix='!', intents=intents)


class BotonView(View):
    def __init__(self):
        super().__init__(timeout=None)  # Sin timeout para que la vista no expire

    @discord.ui.button(label="Anotarme", style=discord.ButtonStyle.success, custom_id="button1")
    async def button1_callback(self, interaction: discord.Interaction, button: Button):
        if verificarIngreso(interaction.user.id):
            await interaction.response.send_message(
                "Ya te encuentras anotado en el torneo. Si te equivocaste de nombre abandona y vuelve a anotarte.",
                ephemeral=True
                )
        else:
            await interaction.response.send_modal(NameModal())

    @discord.ui.button(label="Abandonar", style=discord.ButtonStyle.danger, custom_id="button2")
    async def button2_callback(self, interaction: discord.Interaction, button: Button):
        if verificarIngreso(interaction.user.id):
            await interaction.response.send_modal(ConfirmarAbandonar())
        else:
            await interaction.response.send_message("No estás anotado en el torneo.", ephemeral=True)

class NameModal(Modal):
    def __init__(self):
        super().__init__(title="Anotarse en el Torneo")
        
        # Campo de entrada de texto
        mensaje= ("Ingrese su RiotID en el recuadro de abajo: \n")
        self.add_item(TextInput(
            label= mensaje, 
            placeholder="Escribe tu RiotID aqui",
            required=True))

    # Método que se ejecuta cuando se envía el modal
    async def on_submit(self, interaction: discord.Interaction):
        riotID = self.children[0].value  # Obtener el valor ingresado
        nick = interaction.user.display_name
        guardarIngreso(interaction.user.id,riotID,nick)
        await interaction.response.send_message(
            f"¡Perfecto __**{nick}**__! Has sido anotado en el torneo con el nombre ____**{riotID}**____. Buena suerte :ok_hand:", 
            ephemeral=True
            )


class ConfirmarAbandonar(Modal):
    def __init__(self):
        super().__init__(title="Confirmar Abandono")
        
        # Mensaje de confirmación
        self.add_item(TextInput(
            label="Escribe 'yep' para confirmar.",
            placeholder="Escribe 'yep' para confirmar",
            required=True
        ))

    async def on_submit(self, interaction: discord.Interaction):
        confirmation = self.children[0].value.lower()
        if confirmation == 'yep':
            if verificarIngreso(interaction.user.id):
                # Eliminar al participante
                eliminarIngreso(interaction.user.id)
                await interaction.response.send_message("Has abandonado el torneo. Tu inscripción ha sido eliminada.", ephemeral=True)
            else:
                await interaction.response.send_message("No estás anotado en el torneo.", ephemeral=True)
        else:
            await interaction.response.send_message("Abandono cancelado.", ephemeral=True)


async def configurarBotones(bot):
    channel_id = 1277300198238064713  # Reemplaza con tu canal ID
    message_id = 1277425903978152008  # Reemplaza con tu mensaje ID
    channel = bot.get_channel(channel_id)
    if channel is not None:
        try:
            mensaje = await channel.fetch_message(message_id)
            view = BotonView()
            await mensaje.edit(view=view)
            print("Mensaje editado con nuevos botones.")
        except Exception as e:
            print(f"No se pudo editar el mensaje: {e}")
    else:
        print("No se pudo encontrar el canal con el ID especificado.")

# Comando slash para enviar un saludo
@bot.tree.command(name="saludar", description="Envía un saludo al canal.")
async def saludar(interaction: discord.Interaction):
    
    await interaction.response.send_message("¡Hola enviado al canal!", ephemeral=True)
    
@bot.tree.command(name="enviar_boton", description="Envía un mensaje con botones.")
async def enviar_boton(interaction: discord.Interaction):
    # Define la vista
    view = BotonView()

    # Envía el mensaje con los botones
    mensaje = ("@everyone\n"
               "# Torneo 1v1 Edición Sangrienta\n\n"
               "### Buenas gente, es de mi agrado anunciar una nueva edición de un Torneo 1v1 para la comunidad, esta vez lo haremos mas violento porque es a lo que venimos >:)\n"
               "### Las reglas van a ser bastante fáciles y sin complicaciones:\n "
               "## Reglas: \n"
               "### - :one: - Ganador decidido por primera sangre.\n"
               "### - :two: - Pasados 15mn del inicio del juego, el ganador se decidirá con un tiro de moneda, el que tenga más farm eligirá su lado.\n"
               "### - :three: - Diviertanse, cualquier comportamiento tóxico sera sancionado con descalificación directa.\n\n"
               "## Forma de anotarse: \n"
               "### Clickea en 'Anotarme' abajo del mensaje, ingresa tu ID EXACTO de Riot y listo!\n"
               "### Una vez inscrito, podrás verificarlo en la Lista de Participantes. \n"
               "### Nota: No se realizaran modificaciones en los nombres anotados, si te equivocaste de riotID o lo cambiaste la unica solución es Abandonar y volver a Anotarte.\n\n"
               "### Les dejo la lista de participantes para que puedan chusmear a gusto: \n\n"
               "[Lista de Participantes](<https://docs.google.com/spreadsheets/d/1-SeTK2DDOJ3Md6FldM0gJPtFX2c58LG1/edit?usp=sharing&ouid=102253690445538210913&rtpof=true&sd=true>)\n"
               "_ _"
               )
    
    
    await interaction.channel.send(content=mensaje, view=view, allowed_mentions=discord.AllowedMentions(everyone=True))
    await interaction.response.send_message("¡Botón enviado al canal!", ephemeral=True)

    
    
