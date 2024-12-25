from discord.ext import commands
import discord, math, json, os, traceback
##################################################################################################
# KEEP AS MANY THINGS OUT OF THIS FILE AS POSSIBLE, SO THEY CAN BE LOADED WITHOUT A FULL RESTART #
##################################################################################################

# Loading extensions
async def load_cogs(unload):
    for extension in os.listdir("cogs"):
        if extension.endswith('.py'):
            try:
                if unload == True:
                    try:
                        await bot.unload_extension("cogs." + extension.rstrip(".py"))
                    except:
                        # Imagine handling your exceptions in the slightest
                        pass
                await bot.load_extension("cogs." + extension.rstrip(".py"))
                print('[INFO] Loaded cog {}'.format(extension))
            except Exception as e:
                print('[ERROR] Failed to load cog {}\n[ERROR] {}: {}'.format(extension, type(e).__name__, e))

# Bot Stuff
intents = discord.Intents(messages=True)
intents.message_content = True
intents.typing = False
intents.presences = False

bot = commands.Bot(["⚙️ ", "⚙️"], case_insensitive=True, intents=intents)
bot.remove_command('help')

footerText = "Gearbot | Contact affected for support"

@bot.event
async def on_ready():
    await load_cogs(False)
    print("[INFO] DM-Handler Online")
    print("[INFO] User/ID: "+bot.user.name+"/"+str(bot.user.id))
    await bot.change_presence(activity=discord.Game(name=('⚙️help')))

@bot.command()
async def reload(ctx):
    try:
        if ctx.author.id == 200631029675982858:
            print('[INFO] Reloading cogs...')
            await load_cogs(True)
            content = discord.Embed()
            content.title = "Reload Complete"
            content.set_footer(text=footerText)
            content.color = 0x00FF00
            await ctx.send(embed=content)
        else:
            content = discord.Embed()
            content.title = "Access Denied"
            content.set_footer(text=footerText)
            content.color = 0xFF0000
            await ctx.send(embed=content)
    except Exception:
        print("[ERROR] Error in reload: "+str(traceback.format_exc()))
        content = discord.Embed()
        content.color = 0xFF0000
        content.title = "ERROR"
        content.description = "An error occured with the `reload` command. **Please try again**. If the problem persists, please inform affected and include the error below."
        content.set_footer(text=footerText)
        content.add_field(name="Error Data", value="```\n"+str(traceback.format_exc())+"\n```", inline=False)
        await ctx.send(embed=content)

#if __name__ == "__main__":
#    load_cogs(False)

tokenFile = open("token", "r")
token = tokenFile.read()
tokenFile.close()
bot.run(token)
