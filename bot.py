import os

from discord.ext import commands
from dotenv import load_dotenv
import tabinst

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

bot = commands.Bot("/t ")
tableInstructions = tabinst.load()


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name="hi", help="Say hello!")
async def hello(ctx):
	await ctx.send("Hello!")

@bot.command()
async def gen(ctx, group: str, instruction: str):
	group = group.lower()
	instruction = instruction.lower()

	if group in tableInstructions:
		groupInstructions = tableInstructions[group]
		if instruction in groupInstructions.instructions:
			await replaceTokens(ctx, groupInstructions.instructions[instruction].lines)
		else:
			await ctx.send("Couldn't find instruction '" + instruction + "'.")
	else:
		await ctx.send("Couldn't find group '" + group + "'.")

async def replaceTokens(ctx, lines):
	# todo: token replacement
	await outputResult(ctx, lines)

async def outputResult(ctx, lines):
	lines[:0]=[ctx.message.author.mention,"```"]
	lines.append("```")
	await ctx.send("\n".join(lines))



bot.run(token)