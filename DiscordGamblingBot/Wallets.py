import os ,random,Wallets,Payments,Admin,Giveaway
os.chdir("./discord")
import discord
os.chdir("../")

WalletLocation = "D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/Wallets"
DepositAddresses = "D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/DepositAddresses"
AdminIDs = {"251754144958906369"}

async def Bal(message,client):
	if os.path.exists(WalletLocation+"/"+message.author.id+".bin"):
		await client.send_message(message.channel,"{0.author.mention} You Have: ".format(message)+open(WalletLocation+"/"+message.author.id+".bin","r").read()+"GRLC")
	else:
		await client.send_message(message.channel,"{0.author.mention} You dont appear to have a wallet, one has now been created for you.".format(message))
		open(WalletLocation+"/"+message.author.id+".bin","w").write("0")

async def BalOther(message,client):
	Target = message.content.split(" ")[1]
	if os.path.exists(WalletLocation+"/"+Target+".bin"):
		await client.send_message(message.channel,"<@"+Target+"> Has: ".format(message)+open(WalletLocation+"/"+Target+".bin","r").read())
	else:
		await client.send_message(message.channel,Target+" Does Not Have A Wallet")

async def Pay(message,client):
	Sender=message.author.id
	Reciver=message.content.split(" ")[1]
	SenderBal = float( open(WalletLocation+"/"+Sender+".bin","r").read())
	ReciverBal = float( open(WalletLocation+"/"+Reciver+".bin","r").read())
	if os.path.exists(WalletLocation+"/"+Sender+".bin") and os.path.exists(WalletLocation+"/"+Reciver+".bin"):
		TransferedAmount = float(message.content.split(" ")[2])
		if SenderBal-TransferedAmount >= 0:
			open(WalletLocation+"/"+Sender+".bin","w").write(str(SenderBal-TransferedAmount))
			open(WalletLocation+"/"+Reciver+".bin","w").write(str(ReciverBal+TransferedAmount))
			await client.send_message(message.channel,("{0.author.mention} Payment Sent Of "+str(TransferedAmount)+"GRLC").format(message))
		else:
			await client.send_message(message.channel,"{0.author.mention} You dont have enough funds".format(message))
	else:
		await client.send_message(message.channel,"You or the Recipiant do not have a wallet!")
		
