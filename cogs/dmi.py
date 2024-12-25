import struct, discord, sys, json, random, traceback, subprocess, asyncio, urllib.request
from discord.ext import commands
import __main__
# Any commands that dont have a specific home go here - this is a copypasted comment
class DMI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.executing = False

    # Actual command to take DM input - so is this lol
    @commands.command()
    async def dmi(self, ctx, state=None):
        try:
            content = discord.Embed()
            content.set_footer(text=__main__.footerText)
            # Check permissions
            contributorRole = discord.utils.get(ctx.guild.roles, id=275977432144674818)
            spriterRole = discord.utils.get(ctx.guild.roles, id=489070019087433738)
            if (contributorRole in ctx.author.roles) or (spriterRole in ctx.author.roles):
                if not state:
                    content.title = "Error"
                    content.description = "Please supply a state for the bot to read from"
                    content.color = 0xFF0000
                    await ctx.send(embed=content)
                    return
                if len(ctx.message.attachments) == 0:
                    content.title = "Error"
                    content.description = "Please attach a DMI file for the bot to read from"
                    content.color = 0xFF0000
                    await ctx.send(embed=content)
                    return
                if self.executing:
                    content.title = "Error"
                    content.description = "The bot is currently executing someone else's DMI operation. Please wait."
                    content.color = 0xFF0000
                    await ctx.send(embed=content)
                    return

                # From here, we block
                self.executing = True

                # We have an attachment, assume index 0 is the DMI
                attachment = ctx.message.attachments[0]
                opener = urllib.request.build_opener()
                opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                urllib.request.install_opener(opener)
                urllib.request.urlretrieve(attachment.url, './dmi_env/input.dmi')
                
                # Handle saving the state file
                stateFile = open("./dmi_env/state.txt", "w")
                stateFile.write(state)
                stateFile.close()

                # Now we do the scary part. Start up DD
                DDproc = await asyncio.create_subprocess_exec("./dmi_run.sh", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
                try:
                    await asyncio.wait_for(DDproc.wait(), timeout=30)
                except asyncio.TimeoutError:
                    DDproc.kill()
                    self.executing = False
                    content.title = "DD Error"
                    content.description = "DreamDaemon timed out after 30 seconds"
                    content.color = 0xFF0000
                    await ctx.send(embed=content)
                    return

                assert DDproc.stdout is not None
                DDdata = await DDproc.stderr.read() + await DDproc.stdout.read()
                DDlog = DDdata.decode("UTF-8", "replace")

                # Discord max size of field is 1024 chars. Lets cap at 512
                if len(DDlog) > 512:
                    DDlog = DDlog[:512] + "\n<Truncated>"
                
                # Send the log
                content.title = "Success"
                content.add_field(name="DD Output", value="```" + str(DDlog) + "```", inline=False)
                content.color = 0x00FF00
                await ctx.send(embed=content, file=discord.File("./dmi_env/out.png"))
                self.executing = False
                return
            else:
                content.title = "Error"
                content.description = "Only GitHub Contributors or Sprite Contributors may use this command."
                content.color = 0xFF0000
                await ctx.send(embed=content)
                return
        except Exception:
            print("[ERROR] Error in dmi: "+str(traceback.format_exc()))
            self.executing = False
            content = discord.Embed()
            content.color = 0xFF0000
            content.title = "ERROR"
            content.description = "An error occured with the `dmi` command. **Please try again**. If the problem persists, please inform affected and include the error below."
            content.set_footer(text=__main__.footerText)
            content.add_field(name="Error Data", value="```\n"+str(traceback.format_exc())+"\n```", inline=False)
            await ctx.send(embed=content)

async def setup(bot):
    await bot.add_cog(DMI(bot))
