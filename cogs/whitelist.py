from discord.ext import commands
import discord
from web3 import Web3
import csv
from pathlib import Path
import time
from discord.ext.commands.errors import CommandInvokeError
from dotenv import load_dotenv
import os
load_dotenv()

infura_uri = f'https://mainnet.infura.io/v3/{os.getenv("INFURA_APP_ID")}'
w3 = Web3(Web3.HTTPProvider(infura_uri))
w3.isConnected()
class FivedBot(commands.Cog):
	def __init__(self, bot):
		bot = bot
		self.address = []
		self.whitelisted = []
		self.user = []
	@commands.command()
	async def fivedlist(self, ctx, arg):
		validETHAddress = w3.isAddress(arg)
		if validETHAddress == True and arg not in self.address and str(ctx.author) not in self.user:
			self.whitelisted.append(f'{str(ctx.author.id)},{str(ctx.author)},{arg}')
			self.address.append(arg)
			self.user.append(str(ctx.author))
			reply = await ctx.reply(f'Valid address recorded.')
			msg = await ctx.fetch_message(ctx.message.id)
			reply = await ctx.fetch_message(reply.id)
			time.sleep(3)
			await msg.delete()
			await reply.delete()
		elif validETHAddress == False:
			wrong = await ctx.reply(f'Invalid ETH address')
			msg = await ctx.fetch_message(ctx.message.id)
			wrong = await ctx.fetch_message(wrong.id)
			time.sleep(3)
			await msg.delete()
			await wrong.delete()
		elif arg in self.address:
			w = await ctx.reply(f'This address is whitlisted')
			msg = await ctx.fetch_message(ctx.message.id)
			w = await ctx.fetch_message(w.id)
			time.sleep(10)
			await w.delete()
			await msg.delete()

		elif str(ctx.author) in self.user:
			for i in self.whitelisted:
				u = i.split(',')
				if str(ctx.author) in u:
					user = f'{u[0]},{u[1]},{u[2]}'
					index = self.whitelisted.index(user)
					self.whitelisted[index] = f'{str(ctx.author.id)},{str(ctx.author)},{arg}'
					AddressIndex = self.address.index(u[2])
					self.address[AddressIndex] = arg
					reply = await ctx.reply(f'Valid address resubmitted.')
					msg = await ctx.fetch_message(ctx.message.id)
					reply = await ctx.fetch_message(reply.id)
					time.sleep(3)
					await msg.delete()
					await reply.delete()


	@commands.command()
	async def fivedcheck(self, ctx):
		users = str(ctx.author)
		if users in self.user:
			index = self.user.index(users)
			address = self.address[index]
			checkWhitelist = await ctx.reply(f'Whitlist Confirmed: {address}')
			checkWhitelist = await ctx.fetch_message(checkWhitelist.id)
			msg = await ctx.fetch_message(ctx.message.id)
			time.sleep(3)
			await msg.delete()
			await checkWhitelist.delete()
		else:
			checkWhitelist = await ctx.reply('Not whitelisted')
			checkWhitelist = await ctx.fetch_message(checkWhitelist.id)
			msg = await ctx.fetch_message(ctx.message.id)
			time.sleep(3)
			await msg.delete()
			await checkWhitelist.delete()

	@commands.command()
	@commands.has_permissions(administrator=True)
	async def fivedremove(self, ctx, user:discord.Member):
		for i in self.whitelisted:
			u = i.split(',')
			try:
				if str(user) in u:
					users = f'{u[0]},{u[1]},{u[2]}'
					index = self.whitelisted.index(users)
					ad = self.address.index(u[2])
					us = self.user.index(u[1])
					del self.address[ad]
					del self.user[us]
					del self.whitelisted[index]
					removeUser = await ctx.reply(f"user [{user}] removed")
					removeUser = await ctx.fetch_message(removeUser.id)
					msg = await ctx.fetch_message(ctx.message.id)
					time.sleep(3)
					await msg.delete()
					await removeUser.delete()

			except CommandInvokeError:
				msg = await ctx.fetch_message(ctx.message.id)
				await msg.delete()
				


	@commands.command()
	@commands.has_permissions(administrator=True)
	async def fivedinfo (self, ctx):
		path = Path('./cogs/whitelist.csv')
		f = open(path, 'w')
		writer = csv.writer(f, delimiter=',', lineterminator='\n')
		writer.writerow(['userID','username','walletAddress'])
		for entry in self.whitelisted:
			t = entry.split(',')
			writer.writerow([t[0],t[1],t[2]])
		f.close()
		total = len(self.whitelisted)
		tot = await ctx.send(f'Total Whitelisted Users: {total}')
		msg = await ctx.send(file=discord.File(path))
		time.sleep(30)
		tot = await ctx.fetch_message(tot.id)
		c = await ctx.fetch_message(ctx.message.id)
		msg = await ctx.fetch_message(msg.id)
		await c.delete()
		await msg.delete()
		await tot.delete()
		

def setup(bot):
	bot.add_cog(FivedBot(bot))
