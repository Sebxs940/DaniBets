import discord
from discord.ext import commands
"""
Este archivo contiene la creación del bot de Discord.
Este archivo define y configura un objeto bot utilizando la librería discord.py y el módulo commands de discord.ext.
El bot se crea con un prefijo de comando "/" y utiliza los intents por defecto de Discord.
El propósito de este archivo es contener únicamente la creación del objeto bot, 
de manera que otros archivos puedan importarlo y utilizarlo.
"""
# Creamos el objeto bot en un archivo independiente
bot = commands.Bot(command_prefix="/", intents=discord.Intents.default())

# Este archivo solo contiene el bot, así otros archivos pueden importarlo y usarlo
