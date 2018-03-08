import os ,random,Wallets,Payments,Admin,Giveaway
os.chdir("./discord")
import discord
os.chdir("../")

WalletLocation = "D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/Wallets"
DepositAddresses = "D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/DepositAddresses"
AdminIDs = {"251754144958906369"}

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