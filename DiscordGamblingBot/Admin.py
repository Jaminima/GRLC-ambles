import os ,random,Wallets,Payments,Admin,Giveaway,Jackpot,threading,subprocess,SharedCode
MainLocation="C:/Users/oscar/Desktop/DiscordGamblingBot/DiscordGamblingBot/"
os.chdir(MainLocation+"discord")
import discord,discord.ext
os.chdir("../")
client = discord.Client()
WalletLocation = MainLocation+"UserInfo/Wallets"
DepositAddresses = MainLocation+"/UserInfo/DepositAddresses"
AdminIDs = open(MainLocation+"/UserInfo/AdminIDs.bin","r").read()

async def CreateFunds(message,client):
	Reciver=SharedCode.DiscordID(message.content.split(" ")[1])
	TransferedAmount = float(message.content.split(" ")[2])
	ReciverBal = float( open(WalletLocation+"/"+Reciver+".bin","r").read())
	if message.author.id in AdminIDs:
		try:
			SharedCode.AdjustWallet(Reciver,TransferedAmount)
			await client.send_message(message.channel,("<@"+Reciver+"> Has been awarded: "+str(TransferedAmount)+"GRLC"))
		except:
			await client.send_message(message.channel,"Recipiant Does not have a wallet")
	else:
		await client.send_message(message.channel,"You do not have required perms")

async def StartGiveaway(message,client):
    if message.author.id in AdminIDs:
        await Giveaway.StartGiveaway(message,client)
    else:
        await client.send_message(message.channel,"You do not have required perms")

async def EndGiveaway(message,client):
    if message.author.id in AdminIDs:
        Winner = Giveaway.EndGiveaway(client)
        await client.send_message(message.channel,"<@"+Winner+"> Won The Giveaway\nGiveaway is now Closed.")
    else:
        await client.send_message(message.channel,"You do not have required perms")
