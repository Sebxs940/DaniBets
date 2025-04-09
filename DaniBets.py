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
    'x-rapidapi-host': "api-nba-v1.p.rapidSebxs940"
}

TEAM_LOGOS = {
    "Atlanta Hawks": "https://raw.githubusercontent.com/Sebxs940/DaniBets/main/assets/Atlanta%20Hawks.svg",
    "Boston Celtics": "https://raw.githubusercontent.com/Sebxs940/DaniBets/main/assets/Boston%20Celtics.svg",
    "Brooklyn Nets": "https://raw.githubusercontent.com/Sebxs940/DaniBets/main/assets/Brooklyn%20Nets.svg",
    "Charlotte Hornets": "https://raw.githubusercontent.com/Sebxs940/DaniBets/main/assets/Charlotte%20Hornets.svg",
    "Chicago Bulls": "https://raw.githubusercontent.com/Sebxs940/DaniBets/main/assets/Chicago%20Bulls.svg",
    "Cleveland Cavaliers": "https://raw.githubusercontent.com/Sebxs940/DaniBets/main/assets/Cleveland%20Cavaliers.svg",
    "Dallas Mavericks": "https://raw.githubusercontent.com/Sebxs940/DaniBets/main/assets/Dallas%20Mavericks.svg",
    "Denver Nuggets": "https://raw.githubusercontent.com/Sebxs940/DaniBets/main/assets/Denver%20Nuggets.svg",
    "Detroit Pistons": "https://raw.githubusercontent.com/Sebxs940/DaniBets/main/assets/Detroit%20Pistons.svg",
    "Golden State Warriors": "https://raw.githubusercontent.com/Sebxs940/DaniBets/main/assets/Golden%20State%20Warriors.svg",
    "Houston Rockets": "https://raw.githubusercontent.com/Sebxs940/DaniBets/main/assets/Houston%20Rockets.svg",
    "Indiana Pacers": "https://raw.githubusercontent.com/Sebxs940/DaniBets/main/assets/Indiana%20Pacers.svg",
    "LA Clippers": "https://raw.githubusercontent.com/Sebxs940/DaniBets/main/assets/LA%20Clippers.svg",
    "Los Angeles Lakers": "https://raw.githubusercontent.com/Sebxs940/DaniBets/main/assets/Los%20Angeles%20Lakers.svg",
    "Memphis Grizzlies": "https://raw.githubusercontent.com/Sebxs940/DaniBets/main/assets/Memphis%20Grizzlies.svg",
    "Miami Heat": "https://raw.githubusercontent.com/Sebxs940/DaniBets/main/assets/Miami%20Heat.svg",
    "Milwaukee Bucks": "https://raw.githubusercontent.com/Sebxs940/DaniBets/main/assets/Milwaukee%20Bucks.svg",
    "Minnesota Timberwolves": "https://raw.githubusercontent.com/Sebxs940/DaniBets/main/assets/Minnesota%20Timberwolves.svg",
    "New Orleans Pelicans": "https://raw.githubusercontent.com/Sebxs940/DaniBets/main/assets/New%20Orleans%20Pelicans.svg",
    "New York Knicks": "https://raw.githubusercontent.com/Sebxs940/DaniBets/main/assets/New%20York%20Knicks.svg",
    "Oklahoma City Thunder": "https://raw.githubusercontent.com/Sebxs940/DaniBets/main/assets/Oklahoma%20City%20Thunder.svg",
    "Orlando Magic": "https://raw.githubusercontent.com/Sebxs940/DaniBets/main/assets/Orlando%20Magic.svg",
    "Philadelphia 76ers": "https://raw.githubusercontent.com/Sebxs940/DaniBets/main/assets/Philadelphia%2076ers.svg",
    "Phoenix Suns": "https://raw.githubusercontent.com/Sebxs940/DaniBets/main/assets/Phoenix%20Suns.svg",
    "Portland Trail Blazers": "https://raw.githubusercontent.com/Sebxs940/DaniBets/main/assets/Portland%20Trail%20Blazers.svg",
    "Sacramento Kings": "https://raw.githubusercontent.com/Sebxs940/DaniBets/main/assets/Sacramento%20Kings.svg",
    "San Antonio Spurs": "https://raw.githubusercontent.com/Sebxs940/DaniBets/main/assets/San%20Antonio%20Spurs.svg",
    "Toronto Raptors": "https://raw.githubusercontent.com/Sebxs940/DaniBets/main/assets/Toronto%20Raptors.svg",
    "Utah Jazz": "https://raw.githubusercontent.com/Sebxs940/DaniBets/main/assets/Utah%20Jazz.svg",
    "Washington Wizards": "https://raw.githubusercontent.com/Sebxs940/DaniBets/main/assets/Washington%20Wizards.svg"
}

def obtener_resultados():
    try:
        hoy = datetime.today().strftime('%Y-%m-%d')
        url = "https://api-nba-v1.p.rapidapi.com/games"
        params = {"date": hoy}

        respuesta = requests.get(url, headers=HEADERS, params=params)
        respuesta.raise_for_status()
        
        data = respuesta.json()
        juegos = data.get("response", [])

        # Creamos el embed
        embed = discord.Embed(title="Resultados de la NBA", color=0x1e90ff)

        for juego in juegos:
            equipo_local = juego["teams"]["home"]["name"]
            equipo_visitante = juego["teams"]["visitors"]["name"]
            
            # Obtener logos de los equipos
            logo_local = TEAM_LOGOS.get(equipo_local)
            logo_visitante = TEAM_LOGOS.get(equipo_visitante)
            
            # Verificar si hay puntajes disponibles
            scores = juego.get("scores", {})
            puntos_local = scores.get("home", {}).get("points", "No disponible")
            puntos_visitante = scores.get("visitors", {}).get("points", "No disponible")

            fecha = juego["start"].split("T")[0] if "start" in juego else "Fecha no disponible"
            estado_partido = juego.get("status", {}).get("long", "Estado no disponible")
            
            # Crear campo para el partido
            embed.add_field(
                name="Partido:", 
                value=f"🏀 **{equipo_visitante}** ({puntos_visitante}) vs **{equipo_local}** ({puntos_local})\n📅 {fecha}\n📊 Estado: {estado_partido}",
                inline=False
            )

            # Añadir los logos si están disponibles
            if logo_local:
                embed.set_thumbnail(url=logo_local)
            if logo_visitante:
                embed.set_image(url=logo_visitante)

        embed.set_footer(text="Resultados actualizados")
        return embed
        
    except requests.exceptions.RequestException as e:
        return f"Error al obtener los resultados: {str(e)}"
    except Exception as e:
        return f"Error inesperado: {str(e)}"

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
