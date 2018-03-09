import os ,random,Wallets,Payments,Admin,Giveaway
os.chdir("D:\Programming\DiscordGamblingBot\DiscordGamblingBot\discord")
import discord
os.chdir("../")

WalletLocation = "D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/Wallets"
DepositAddresses = "D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/DepositAddresses"
AdminIDs = open("D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/AdminIDs.bin","r").read()

async def CreateFunds(message,client):
	Reciver=message.content.split(" ")[1]
	TransferedAmount = float(message.content.split(" ")[2])
	ReciverBal = float( open(WalletLocation+"/"+Reciver+".bin","r").read())
	if message.author.id in AdminIDs:
		try:
			open(WalletLocation+"/"+Reciver+".bin","w").write(str(ReciverBal+TransferedAmount))
			await client.send_message(message.channel,("<@"+Reciver+"> Has been awarded: "+str(TransferedAmount)+"GRLC"))
		except:
			await client.send_message(message.channel,"Recipiant Does not have a wallet")
	else:
		await client.send_message(message.channel,"You do not have required perms")

async def StartGiveaway(message,client):
    if message.author.id in AdminIDs:
        Giveaway.StartGiveaway(message.content.split(" ")[2])
        await client.send_message(message.channel,"Created Giveaway")
    else:
        await client.send_message(message.channel,"You do not have required perms")

async def EndGiveaway(message,client):
    if message.author.id in AdminIDs:
        Winner = Giveaway.EndGiveaway(client)
        await client.send_message(message.channel,"<@"+Winner+"> Won The Giveaway\nGiveaway is now Closed.")
    else:
        await client.send_message(message.channel,"You do not have required perms")