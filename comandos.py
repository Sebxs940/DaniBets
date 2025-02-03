import discord 
import requests
import os
from DaniBets import bot  # Importamos el bot desde DaniBets.py

CHANNEL_ID = 1212672913304719370  # Reemplaza con el ID de tu canal

HEADERS = {
    'x-rapidapi-key': "df0f752139msh9ceb95b678f60a7p1d1c78jsnf9140e769870",
    'x-rapidapi-host': "api-nba-v1.p.rapidapi.com"
}

LOGOS_PATH = "Logos NBA"  # Ruta donde están guardados los logos

# Función para obtener los resultados de un juego específico
def obtener_resultados_por_fecha(fecha, equipo_nombre=None):
    url = "https://api-nba-v1.p.rapidapi.com/games"
    params = {"date": fecha}  # Consulta por fecha

    try:
        respuesta = requests.get(url, headers=HEADERS, params=params)
        respuesta.raise_for_status()  # Lanza un error si la respuesta no es exitosa
        data = respuesta.json()

        juegos = data.get("response", [])
        if not juegos:
            return "🏀 No se encontraron juegos para la fecha proporcionada."

        mensaje = f"**Resultados de la NBA para la fecha {fecha}:**\n"
        for juego in juegos:
            equipo_local = juego["teams"]["home"]["name"]
            equipo_visitante = juego["teams"]["visitors"]["name"]
            puntos_local = juego["scores"]["home"]["points"]
            puntos_visitante = juego["scores"]["visitors"]["points"]

            if equipo_nombre and (equipo_nombre.lower() not in equipo_local.lower() and equipo_nombre.lower() not in equipo_visitante.lower()):
                continue  # Si el nombre del equipo no coincide, se salta el juego.

            # Buscar logos en la carpeta local
            logo_local = os.path.join(LOGOS_PATH, f"{equipo_local}.png")
            logo_visitante = os.path.join(LOGOS_PATH, f"{equipo_visitante}.png")

            mensaje += f"\n🏀 **{equipo_visitante}** ({puntos_visitante}) vs **{equipo_local}** ({puntos_local})\n"

        return mensaje
    except requests.exceptions.RequestException as e:
        return f"Error al obtener los resultados: {str(e)}"

# Comando para consultar los resultados de un equipo en una fecha específica
@bot.tree.command(name="resultados", description="Muestra los resultados de los juegos para un equipo en una fecha específica.")
async def resultados(interaction: discord.Interaction, nombre: str, fecha: str):
    """
    /resultados {nombre} {fecha} - Muestra los resultados de los juegos para un equipo en una fecha específica.
    """
    resultado = obtener_resultados_por_fecha(fecha, nombre)
    await interaction.response.send_message(resultado)

# Evento que se ejecuta cuando el bot está listo
@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
