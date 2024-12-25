import struct, discord, sys, json, random, traceback, subprocess, asyncio
from discord.ext import commands
import __main__
# Any commands that dont have a specific home go here - this is also copypaste
class Dis(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.executing = False

    # Actual command to take DM input - this is also copypaste
    @commands.command()
    async def dis(self, ctx, *, lines=None):
        content = discord.Embed()
        content.set_footer(text=__main__.footerText)
        content.title = "Error"
        content.description = "This thing broke when I upated BYOND. It might get fixed some day. Maybe."
        content.color = 0xFF0000
        await ctx.send(embed=content)
        return
        
        # Broken till I fix it 
        try:
            content = discord.Embed()
            content.set_footer(text=__main__.footerText)
            # Check permissions
            contributorRole = discord.utils.get(ctx.guild.roles, id=275977432144674818)
            if contributorRole in ctx.author.roles:
                if not lines:
                    content.title = "Error"
                    content.description = "Please supply DM code, inside a code block for this command to function"
                    content.color = 0xFF0000
                    await ctx.send(embed=content)
                    return
                if self.executing:
                    content.title = "Error"
                    content.description = "The bot is currently executing someone else's DM code. Please wait."
                    content.color = 0xFF0000
                    await ctx.send(embed=content)
                    return
                # Check for exploitation
                if lines.find("include") != -1:
                    content.title = "Error"
                    content.description = "`#include` was supplied. This operation is disabled for security reasons."
                    content.color = 0xFF0000
                    await ctx.send(embed=content)
                    return
                if lines.find("Export") != -1:
                    content.title = "Error"
                    content.description = "`world.Export` was supplied. This operation is disabled for security reasons."
                    content.color = 0xFF0000
                    await ctx.send(embed=content)
                    return
                # Sanity checks over. LETS BEGIN. So lets parse these lines
                # FROM THIS POINT ON, WE LOSE OUR ASYNCABILITY
                self.executing = True
                cleanLines = lines.lstrip("```\n")
                cleanLines = cleanLines.rstrip("\n```")
                cleanLines = cleanLines.replace("\r", "\n").replace("    ", "\t") # Tabs > Spaces
                listLines = cleanLines.split("\n")

                fileLines = "#define DEBUG\n/proc/main()\n"
                # Indent each line by one so we can put it as a datum's New().s
                for index, line in enumerate(listLines):
                    if not line.strip():
                        continue

                    listLines[index] = "\t" + line

                fileLines += "\n".join(listLines)

                # Now write the file
                outputFile = open("./src/code.dm", "w")
                outputFile.write(fileLines)
                outputFile.close()

                # COMPILE
                DMproc = await asyncio.create_subprocess_exec("./dis_build.sh", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
                DMfailReason = None
                try:
                    await asyncio.wait_for(DMproc.wait(), timeout=30)
                except asyncio.TimeoutError:
                    DMproc.kill()
                    self.executing = False
                    content.title = "DM Error"
                    content.description = "Compiler timed out after 30 seconds"
                    content.color = 0xFF0000
                    await ctx.send(embed=content)
                    return

                assert DMproc.stdout is not None
                DMdata = await DMproc.stdout.read()
                DMlog = DMdata.decode("UTF-8", "replace")

                # Discord max size of field is 1024 chars. Lets cap at 512
                if len(DMlog) > 512:
                    DMlog = DMlog[:512] + "\n<Truncated>"

                if DMfailReason or DMproc.returncode:
                    self.executing = False
                    content.title = "DM Error"
                    if DMfailReason:
                        content.description = DMfailReason
                    content.add_field(name="DM Output", value="```" + str(DMlog) + "```", inline=False)
                    content.color = 0xFF0000
                    await ctx.send(embed=content)
                    return


                # If we are here, we successfully compiled. SO LETS RUN
                DDproc = await asyncio.create_subprocess_exec("./dis_run.sh", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
                DDfailReason = None
                try:
                    await asyncio.wait_for(DDproc.wait(), timeout=30)
                except asyncio.TimeoutError:
                    DDproc.kill()
                    self.executing = False
                    content.title = "Dis Error"
                    content.description = "Dissassembler timed out after 30 seconds"
                    content.color = 0xFF0000
                    await ctx.send(embed=content)
                    return

                assert DDproc.stdout is not None
                DDdata = await DDproc.stderr.read() + await DDproc.stdout.read()
                DDlog = DDdata.decode("UTF-8", "replace")
                raw_log = DDlog
                post_raw = False

                # Discord max size of field is 1024 chars. Lets cap at 512
                if len(DDlog) > 512:
                    DDlog = DDlog[:512] + "\n<Truncated>"
                    post_raw = True

                # Send the log
                content.title = "Success"
                content.add_field(name="DM Output", value="```" + str(DMlog) + "```", inline=False)
                content.add_field(name="Dis Output", value="**`DbgLine` instructions have a line offset of 2 (Line 2 becomes 4, etc)**\n```" + str(DDlog) + "```", inline=False)
                if DDfailReason:
                    content.color = 0xFF0000
                    content.description = DDfailReason
                else:
                    content.color = 0x00FF00
                await ctx.send(embed=content)

                if post_raw:
                    rf = open("raw.log", "w")
                    rf.write(raw_log)
                    rf.close()

                    await ctx.send(file=discord.File("raw.log"))

                self.executing = False
                return
            else:
                content.title = "Error"
                content.description = "Only GitHub Contributors may use this command."
                content.color = 0xFF0000
                await ctx.send(embed=content)
                return
        except Exception:
            print("[ERROR] Error in dis: "+str(traceback.format_exc()))
            self.executing = False
            content = discord.Embed()
            content.color = 0xFF0000
            content.title = "ERROR"
            content.description = "An error occured with the `dis` command. **Please try again**. If the problem persists, please inform affected and include the error below."
            content.set_footer(text=__main__.footerText)
            content.add_field(name="Error Data", value="```\n"+str(traceback.format_exc())+"\n```", inline=False)
            await ctx.send(embed=content)

async def setup(bot):
    await bot.add_cog(Dis(bot))
