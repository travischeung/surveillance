        
from asyncio.constants import DEBUG_STACK_DEPTH
import RPi.GPIO as GPIO
import time
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix="!")

async def on_ready():  # when the bot is ready
    print("on ready running")
    guild = discord.utils.get(bot.guilds, name=936704754275483738)
    print('{bot.user} has joined this cringe discord.')
    channel2 = bot.get_channel(936704754275483742)
    await channel2.send("quiet bot")

@bot.event  # idk what this means but you have to do it
async def detected():
    print('message')
    channel2 = bot.get_channel(936704754275483742)
    await channel2.send("alert")


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.IN)         #Read output from PIR motion sensor
GPIO.setup(3, GPIO.OUT)         #LED output pin

async def run():
    print("now running")
    while True:
        i=GPIO.input(8)
        if i==0:                 #When output from motion sensor is LOW
            print ("No intruders"),i
            GPIO.output(3, 0)  #Turn OFF LED
            time.sleep(0.1)
        elif i==1:               #When output from motion sensor is HIGH
            print ("Intruder detected"),i
            await detected()
            GPIO.output(3, 1)  #Turn ON LED
            time.sleep(0.1)

bot.run(TOKEN)