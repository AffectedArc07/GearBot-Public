import struct, discord, sys, json, random, traceback, subprocess
from discord.ext import commands
import __main__
# Any commands that dont have a specific home go here
class Misc(commands.Cog):
    @commands.command()
    async def help(self, ctx):
        try:
            content = discord.Embed()
            content.title = "Help"
            content.color = 0x00FF00
            content.description = "**This bot will be phased out before long. Web-based DM compiler may arrive eventually.**"
            _commands = """
            **⚙️dm** - Allows for in-chat DM compilation and testing
            **⚙️dmi** - Converts a DMI state to a full-size PNG in discord. Supply a DMI file as attachment and the name of the state as the second word. Does not work with gifs.
            **⚙️helpers** - Link to helpers for use within the DM compilation module
            **⚙️pr** - Lookup PR info in detail
            **⚙️testserver** - Get a link to the test server
            """
            content.add_field(name="Bot Commands", value=_commands, inline=False)
            content.set_footer(text=__main__.footerText)
            await ctx.send(embed=content)
        except Exception:
            print("[ERROR] Error in help: "+str(traceback.format_exc()))
            content = discord.Embed()
            content.color = 0xFF0000
            content.title = "ERROR"
            content.description = "An error occured with the `help` command. **Please try again**. If the problem persists, please inform affected and include the error below."
            content.set_footer(text=__main__.footerText)
            content.add_field(name="Error Data", value="```\n"+str(traceback.format_exc())+"\n```", inline=False)
            await ctx.send(embed=content)

    @commands.command()
    async def testserver(self, ctx):
        #return
        try:
            content = discord.Embed()
            content.title = "Test Server URL"
            content.color = 0x00FF00
            content.description = "`byond://multiss13.com:6666`\nHosted by Denghis. Ping him if you require ingame permissions."
            content.set_footer(text=__main__.footerText)
            await ctx.send(embed=content)
        except Exception:
            print("[ERROR] Error in help: "+str(traceback.format_exc()))
            content = discord.Embed()
            content.color = 0xFF0000
            content.title = "ERROR"
            content.description = "An error occured with the `testserver` command. **Please try again**. If the problem persists, please inform affected and include the error below."
            content.set_footer(text=__main__.footerText)
            content.add_field(name="Error Data", value="```\n"+str(traceback.format_exc())+"\n```", inline=False)
            await ctx.send(embed=content)


async def setup(bot):
    await bot.add_cog(Misc(bot))
