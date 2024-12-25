import struct, discord, sys, json, random, traceback, subprocess, asyncio, requests
from discord.ext import commands
from github import Github
from datetime import datetime
import __main__
# All GitHub related commands
class GH(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.executing = False

    @commands.command()
    async def pr(self, ctx, *args):
        try:
            content = discord.Embed()
            content.set_footer(text=__main__.footerText)
            if not len(args):
                content.title = "Error"
                content.description = "Please supply a PR number"
                content.color = 0xFF0000
                await ctx.send(embed=content)
                return
            prnum = int(args[0])

            if prnum in [3333, 7572, 7000, 7579]:
                content.title = "Error"
                content.description = f"<@{ctx.author.id}> This PR cant be posted for a good reason.\nDont post the link to it either please."
                content.color = 0xFF0000
                await ctx.send(embed=content)
                return

            git = Github("lol no") # totally not a hardcoded secret
            repo = git.get_repo(27286452)
            pr = repo.get_pull(prnum)
            data = pr.raw_data
            state = pr.state
            if state == "open":
                content.color = 0x00FF00
            else:
                if pr.is_merged():
                    content.color = 0x6F42C1
                    state = "merged"
                else:
                    content.color = 0xFF0000
            labelList = []
            if pr.labels:
                for label in pr.labels:
                    labelList.append("`{}`".format(label.name))
            else:
                labelList.append("*None*")
            content.title = "PR #" + str(prnum)
            content.description = "**" + data["user"]["login"] + "** - " + data["title"]
            content.add_field(name="Opened At:", value=pr.created_at, inline=False)
            content.add_field(name="Link", value="https://github.com/ParadiseSS13/Paradise/pull/" + str(prnum), inline=False)
            content.add_field(name="Labels", value=", ".join(labelList), inline=False)
            content.add_field(name="Status", value=state.title(), inline=False)
            if pr.merged:
                content.add_field(name="Merged By: " + str(pr.merged_by.login), value="Merged At: " + str(pr.merged_at), inline=False)
            if pr.state.title() == "Closed":
                content.add_field(name="Closed At:", value=str(pr.closed_at), inline=False)
            await ctx.send(embed=content)
        except Exception:
            print("[ERROR] Error in pr: "+str(traceback.format_exc()))
            content = discord.Embed()
            content.color = 0xFF0000
            content.title = "ERROR"
            content.description = "An error occured with the `pr` command. **Please try again**. If the problem persists, please inform affected and include the error below."
            content.set_footer(text=__main__.footerText)
            content.add_field(name="Error Data", value="```\n"+str(traceback.format_exc())+"\n```", inline=False)
            await ctx.send(embed=content)

    @commands.command()
    async def ghapirls(self, ctx, *args):
        try:
            content = discord.Embed()
            content.set_footer(text=__main__.footerText)
            if ctx.author.id != 200631029675982858:
                content.title = "Error"
                content.description = "This command is AA only"
                content.color = 0xFF0000
                await ctx.send(embed=content)
                return
            header_list = {"Authorization": "Bearer lol no"} # totally not a hardcoded secret
            data = requests.get("https://api.github.com/rate_limit", headers=header_list).json()
            content.title = "GitHub API Rate Limits Status"
            content.color = 0x12A5F4
            content.add_field(name="Limit", value=data["rate"]["limit"], inline=False)
            content.add_field(name="Used", value=data["rate"]["used"], inline=False)
            content.add_field(name="Remaining", value=data["rate"]["remaining"], inline=False)
            content.add_field(name="Reset", value="{} UTC".format(datetime.utcfromtimestamp(data["rate"]["reset"]).strftime('%Y-%m-%d %H:%M:%S')), inline=False)
            await ctx.send(embed=content)
        except Exception:
            print("[ERROR] Error in ghapirls: "+str(traceback.format_exc()))
            content = discord.Embed()
            content.color = 0xFF0000
            content.title = "ERROR"
            content.description = "An error occured with the `ghapirls` command. **Please try again**. If the problem persists, please inform affected and include the error below."
            content.set_footer(text=__main__.footerText)
            content.add_field(name="Error Data", value="```\n"+str(traceback.format_exc())+"\n```", inline=False)
            await ctx.send(embed=content)

async def setup(bot):
    await bot.add_cog(GH(bot))
