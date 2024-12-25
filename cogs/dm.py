import struct, discord, sys, json, random, traceback, subprocess, asyncio
from discord.ext import commands
import __main__
# Any commands that dont have a specific home go here - WHY CANT I STOP COPYPASTING THIS TEXT
class DM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.executing = False

    # Command to echo list of helpers
    @commands.command()
    async def helpers(self, ctx):
        try:
            content = discord.Embed()
            content.title = "Helpers"
            content.color = 0x00FF00
            content.description = ""
            content.title = "Helpers"
            content.add_field(name="**DM Defines**", value="[Click Here](https://gist.github.com/AffectedArc07/ba9eaf1c522f804a12ee6915f901af58)")
            content.set_footer(text=__main__.footerText)
            await ctx.send(embed=content)
        except Exception:
            print("[ERROR] Error in helpers: "+str(traceback.format_exc()))
            content = discord.Embed()
            content.color = 0xFF0000
            content.title = "ERROR"
            content.description = "An error occured with the `helpers` command. **Please try again**. If the problem persists, please inform affected and include the error below."
            content.set_footer(text=__main__.footerText)
            content.add_field(name="Error Data", value="```\n"+str(traceback.format_exc())+"\n```", inline=False)
            await ctx.send(embed=content)

    # Actual command to take DM input
    @commands.command()
    async def dm(self, ctx, *, lines=None):
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
                # Prepare the file
                fileLines = "#include \"helpers.dm\"\n"
                # Check if they defined proc/main
                if cleanLines.find("proc/main") == -1:
                    # If they didnt define it, lets force-define it
                    fileLines += "/proc/main()\n"
                    # Indent each line by one so we can put it as a datum's New().s
                    for index, line in enumerate(listLines):
                        if not line.strip():
                            continue

                        listLines[index] = "\t" + line

                    fileLines += "\n".join(listLines)
                else:
                    # If they did define it, lets just insert their code
                    fileLines += cleanLines
                
                fileLines += "\nvar/datum/runner/R=new\n/datum/runner/New()\n\tAASTART\n\tmain()\n\tAAEND\n\teval(\"\")\n\tshutdown()"

                # Now write the file
                outputFile = open("./dm_env/code.dm", "w")
                outputFile.write(fileLines)
                outputFile.close()

                # COMPILE
                DMproc = await asyncio.create_subprocess_exec("./dm_build.sh", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
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
                DDproc = await asyncio.create_subprocess_exec("./dm_run.sh", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
                DDfailReason = None
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
                content.add_field(name="DM Output", value="```" + str(DMlog) + "```", inline=False)
                content.add_field(name="DD Output", value="```" + str(DDlog) + "```", inline=False)
                if DDfailReason:
                    content.color = 0xFF0000
                    content.description = DDfailReason
                else:
                    content.color = 0x00FF00
                await ctx.send(embed=content)
                self.executing = False
                return
            else:
                content.title = "Error"
                content.description = "Only GitHub Contributors may use this command."
                content.color = 0xFF0000
                await ctx.send(embed=content)
                return
        except Exception:
            print("[ERROR] Error in dm: "+str(traceback.format_exc()))
            self.executing = False
            content = discord.Embed()
            content.color = 0xFF0000
            content.title = "ERROR"
            content.description = "An error occured with the `dm` command. **Please try again**. If the problem persists, please inform affected and include the error below."
            content.set_footer(text=__main__.footerText)
            content.add_field(name="Error Data", value="```\n"+str(traceback.format_exc())+"\n```", inline=False)
            await ctx.send(embed=content)

async def setup(bot):
    await bot.add_cog(DM(bot))
