import discord
from discord.ext import commands, tasks
import requests
import os
from datetime import datetime

# Configuración del bot con intents específicos
intents = discord.Intents.default()
intents.message_content = True  # Agregar permiso para contenido de mensajes
bot = commands.Bot(command_prefix='!', intents=intents)

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = 1180556157161590864

HEADERS = {
    'x-rapidapi-key': "df0f752139msh9ceb95b678f60a7p1d1c78jsnf9140e769870",
    'x-rapidapi-host': "api-nba-v1.p.rapidapi.com"
}

LOGOS_PATH = "Logos NBA"

def obtener_resultados():
    hoy = datetime.today().strftime('%Y-%m-%d')
    url = "https://api-nba-v1.p.rapidapi.com/games"
    params = {"date": hoy}
    try:
        respuesta = requests.get(url, headers=HEADERS, params=params)
        respuesta.raise_for_status()
        data = respuesta.json()

        juegos = data.get("response", [])

        # Creamos el embed
        embed = discord.Embed(title="Resultados de la NBA", color=0x1e90ff)

        for juego in juegos:
            equipo_local = juego["teams"]["home"]["name"]
            equipo_visitante = juego["teams"]["visitors"]["name"]
            puntos_local = juego["scores"]["home"]["points"]
            puntos_visitante = juego["scores"]["visitors"]["points"]

            if "start" in juego:
                fecha = juego["start"].split("T")[0]
            else:
                fecha = "Fecha no disponible"

            embed.add_field(
                name="Partido:", 
                value=f"🏀 **{equipo_visitante}** ({puntos_visitante}) vs **{equipo_local}** ({puntos_local}) - {fecha}",
                inline=False
            )

        embed.set_footer(text="Resultados actualizados")
        return embed
    except requests.exceptions.RequestException as e:
        return f"Error al obtener los resultados: {str(e)}"

@tasks.loop(hours=24)
async def publicar_resultados():
    canal = bot.get_channel(CHANNEL_ID)
    if canal:
        embed = obtener_resultados()
        if isinstance(embed, discord.Embed):
            await canal.send(embed=embed)
        else:
            await canal.send(embed)

@bot.tree.command(name="resultados", description="Muestra los resultados de los juegos para un equipo en una fecha específica.")
async def resultados(interaction: discord.Interaction, nombre: str, fecha: str):
    url = "https://api-nba-v1.p.rapidapi.com/games"
    params = {"date": fecha}

    try:
        respuesta = requests.get(url, headers=HEADERS, params=params)
        respuesta.raise_for_status()
        data = respuesta.json()

        juegos = data.get("response", [])
        if not juegos:
            await interaction.response.send_message("🏀 No se encontraron juegos para la fecha proporcionada.")
            return

        mensaje = f"**Resultados de la NBA para la fecha {fecha}:**\n"
        for juego in juegos:
            equipo_local = juego["teams"]["home"]["name"]
            equipo_visitante = juego["teams"]["visitors"]["name"]
            puntos_local = juego["scores"]["home"]["points"]
            puntos_visitante = juego["scores"]["visitors"]["points"]

            if nombre and (nombre.lower() not in equipo_local.lower() and nombre.lower() not in equipo_visitante.lower()):
                continue

            mensaje += f"\n🏀 **{equipo_visitante}** ({puntos_visitante}) vs **{equipo_local}** ({puntos_local})\n"

        await interaction.response.send_message(mensaje)
    except requests.exceptions.RequestException as e:
        await interaction.response.send_message(f"Error al obtener los resultados: {str(e)}")

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    try:
        await bot.tree.sync()
        print("Comandos sincronizados correctamente")
    except Exception as e:
        print(f"Error al sincronizar los comandos: {e}")
    publicar_resultados.start()

# Manejo global de errores
@bot.event
async def on_error(event, *args, **kwargs):
    print(f"Error en el evento {event}: {args}")

if __name__ == "__main__":
    try:
        bot.run(TOKEN)
    except Exception as e:
        print(f"Error al iniciar el bot: {e}")
