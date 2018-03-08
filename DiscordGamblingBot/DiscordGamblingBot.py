import os ,random,Wallets,Payments,Admin,Giveaway
os.chdir("./discord")
import discord,threading
os.chdir("../")
from _thread import *
from discord.ext import commands

client = discord.Client()
WalletLocation = "D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/Wallets"
DepositAddresses = "D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/DepositAddresses"
AdminIDs = {"251754144958906369"}
Payments.RunWallet()

@client.event
async def on_message(message):
	await messagehandler(message)

async def messagehandler(message):
	if message.content.lower().startswith("?bal") and not "?balother" in message.content:
		await Wallets.Bal(message,client)

	elif message.content.lower().startswith("?balother"):
		await Wallets.BalOther(message,client)

	elif message.content.lower().startswith("?pay"):
		await Wallets.Pay(message,client)

	elif message.content.lower().startswith("?createfunds"):
		await Admin.CreateFunds(message,client)

	elif message.content.lower().startswith("?deposit"):
		await client.send_message(message.channel,"Deposit into: "+Payments.Deposit(message,client)+"Then type ?confirm <transid>")

	elif message.content.lower().startswith("?confirm"):
		await Payments.Confirm(message,client)

	elif message.content.lower().startswith("?withdraw"):
		await Payments.PayOut(message,client)

	elif message.content.lower().startswith("?help"):
		Help="-------GRLC-ambles-------\n?bal -- View you balance\n?balother <userid> -- View balance of someone else\n?pay <reciveraddress> <amount>\n?deposit -- Gives an address for you to pay into\n?confirm <transid> -- Confirm payment\n?withdraw <amount> <address>"
		await client.send_message(message.channel,Help)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
client.run('NDIxMjI4NzA5NDI1NDQ2OTEy.DYKLeA.cQqjgdyV6PaoPxV-Lf78ZA8X8Mo')