import discord
from discord.ext import commands, tasks
import requests
import os
from datetime import datetime
from bot import bot  # Importamos el bot desde bot.py

TOKEN = "os.getenv("DISCORD_TOKEN")"  # Coloca aquí tu token de forma segura
CHANNEL_ID = 1212672913304719370  # Reemplaza con el ID de tu canal

HEADERS = {
    'x-rapidapi-key': "os.getenv("RAPIDAPI_KEY0"),
    'x-rapidapi-host': "api-nba-v1.p.rapidapi.com"
}

LOGOS_PATH = "Logos NBA"  # Ruta donde están guardados los logos

# Función para obtener los resultados de los juegos recientes
def obtener_resultados():
    hoy = datetime.today().strftime('%Y-%m-%d')  # Obtiene la fecha de hoy
    url = "https://api-nba-v1.p.rapidapi.com/games"
    params = {"date": hoy}  # Pasamos la fecha dinámica
    try:
        respuesta = requests.get(url, headers=HEADERS, params=params)
        respuesta.raise_for_status()  # Lanza un error si la respuesta no es exitosa
        data = respuesta.json()

        juegos = data.get("response", [])

        # Creamos el embed
        embed = discord.Embed(title="Resultados de la NBA", color=0x1e90ff)

        for juego in juegos:
            equipo_local = juego["teams"]["home"]["name"]
            equipo_visitante = juego["teams"]["visitors"]["name"]
            puntos_local = juego["scores"]["home"]["points"]
            puntos_visitante = juego["scores"]["visitors"]["points"]

            # Verificar si 'start' existe en los datos del juego
            if "start" in juego:
                fecha = juego["start"].split("T")[0]  # Extraemos solo la fecha (YYYY-MM-DD)
            else:
                fecha = "Fecha no disponible"  # Si no hay fecha, mostramos un mensaje alternativo

            # Obtener las rutas de los logos (ahora con extensión .svg)
            logo_local = os.path.join(LOGOS_PATH, f"{equipo_local}.svg")
            logo_visitante = os.path.join(LOGOS_PATH, f"{equipo_visitante}.svg")

            # Añadir los logos en el embed si existen
            if os.path.exists(logo_local) and os.path.exists(logo_visitante):
                embed.add_field(
                    name="Partido:", 
                    value=f"🏀 **{equipo_visitante}** ({puntos_visitante}) vs **{equipo_local}** ({puntos_local}) - {fecha}",
                    inline=False
                )
                # Solo se puede establecer un thumbnail por embed, así que lo omitimos aquí
                embed.set_footer(text="Resultados actualizados")
            else:
                embed.add_field(
                    name="Partido:", 
                    value=f"🏀 **{equipo_visitante}** ({puntos_visitante}) vs **{equipo_local}** ({puntos_local}) - {fecha}\n(Logo no encontrado para uno o más equipos)",
                    inline=False
                )

        return embed
    except requests.exceptions.RequestException as e:
        return f"Error al obtener los resultados: {str(e)}"

# Tarea programada para enviar los resultados automáticamente
@tasks.loop(hours=24)
async def publicar_resultados():
    canal = bot.get_channel(CHANNEL_ID)
    if canal:
        embed = obtener_resultados()
        if isinstance(embed, discord.Embed):
            await canal.send(embed=embed)
        else:
            await canal.send(embed)

# Comando para consultar los resultados de un equipo en una fecha específica
@bot.tree.command(name="resultados", description="Muestra los resultados de los juegos para un equipo en una fecha específica.")
async def resultados(interaction: discord.Interaction, nombre: str, fecha: str):
    """
    /resultados {nombre} {fecha} - Muestra los resultados de los juegos para un equipo en una fecha específica.
    """
    url = "https://api-nba-v1.p.rapidapi.com/games"
    params = {"date": fecha}  # Consulta por fecha

    try:
        respuesta = requests.get(url, headers=HEADERS, params=params)
        respuesta.raise_for_status()  # Lanza un error si la respuesta no es exitosa
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
                continue  # Si el nombre del equipo no coincide, se salta el juego.

            mensaje += f"\n🏀 **{equipo_visitante}** ({puntos_visitante}) vs **{equipo_local}** ({puntos_local})\n"

        await interaction.response.send_message(mensaje)
    except requests.exceptions.RequestException as e:
        await interaction.response.send_message(f"Error al obtener los resultados: {str(e)}")

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    try:
        # Sincronizamos los comandos explícitamente
        await bot.tree.sync()
        print("Comandos sincronizados correctamente")
    except Exception as e:
        print(f"Error al sincronizar los comandos: {e}")
    publicar_resultados.start()

bot.run(TOKEN)
