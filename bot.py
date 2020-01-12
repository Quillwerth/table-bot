import os

from discord.ext import commands
from dotenv import load_dotenv
import tabinst
import tables
import table_globals

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

bot = commands.Bot("/t ")

shared = table_globals.TableGlobals()

shared.tableInstructions = tabinst.load()
shared.tableLibrary = tables.load()


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

	if group in shared.tableInstructions:
		groupInstructions = shared.tableInstructions[group]
		if instruction in groupInstructions.instructions:
			await replaceTokens(ctx, groupInstructions.instructions[instruction].lines)
		else:
			await ctx.send("Couldn't find instruction '" + instruction + "'.")
	else:
		await ctx.send("Couldn't find group '" + group + "'.")

@bot.command()
async def reload(ctx):
	global shared
	shared.tableInstructions = tabinst.load()
	shared.tableLibrary = tables.load()
	await ctx.send("`Table data reloaded.`")

async def replaceTokens(ctx, lines):
	outputLines = []
	# todo: token replacement
	for line in lines:
		outputLine = line
		recurseCount = 0
		while True:
			tokenName = getToken(outputLine)
			recurseCount += 1
			if tokenName == "" or recurseCount > 100:
				break
			tokenValue = shared.tableLibrary.GetValue(tokenName)
			outputLine = replaceToken(outputLine, tokenName, tokenValue)
		outputLines.append(outputLine)

	await outputResult(ctx, outputLines)

def getToken(line):
	startToken = line.find("{")+1
	if startToken == 0 : 
		return ""
	endToken = line.find("}")
	return line[startToken:endToken]

def replaceToken(line, tokenName, newString):
	tokenName = "{"+tokenName+"}"
	return line.replace(tokenName, newString, 1)

async def outputResult(ctx, lines):
	lines[:0]=[ctx.message.author.mention,"```"]
	lines.append("```")
	await ctx.send("\n".join(lines))



bot.run(token)