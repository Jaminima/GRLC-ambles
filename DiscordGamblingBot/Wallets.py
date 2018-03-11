import os ,random,Wallets,Payments,Admin,Giveaway,Jackpot,threading,subprocess,SharedCode
MainLocation="C:/Users/oscar/Desktop/DiscordGamblingBot/DiscordGamblingBot/"
os.chdir(MainLocation+"discord")
import discord,discord.ext
os.chdir("../")
client = discord.Client()
WalletLocation = MainLocation+"UserInfo/Wallets"
DepositAddresses = MainLocation+"UserInfo/DepositAddresses"
AdminIDs = open(MainLocation+"UserInfo/AdminIDs.bin","r").read()

async def Bal(message,client):
	if os.path.exists(WalletLocation+"/"+message.author.id+".bin"):
		await client.send_message(message.channel,"{0.author.mention} You Have: ".format(message)+open(WalletLocation+"/"+message.author.id+".bin","r").read()+"GRLC")
	else:
		await client.send_message(message.channel,"{0.author.mention} You dont appear to have a wallet, one has now been created for you.".format(message))
		open(WalletLocation+"/"+message.author.id+".bin","w").write("100")

async def BalOther(message,client):
	Target = SharedCode.DiscordID(message.content.split(" ")[1])
	if os.path.exists(WalletLocation+"/"+Target+".bin"):
		await client.send_message(message.channel,"<@"+Target+"> Has: ".format(message)+open(WalletLocation+"/"+Target+".bin","r").read()+"GRLC")
	else:
		await client.send_message(message.channel,"<@"+Target+"> Does Not Have A Wallet\ntry `?bal <mention>`")

async def Pay(message,client):
	Sender=message.author.id
	Reciver=SharedCode.DiscordID(message.content.split(" ")[1])
	SenderBal = float( open(WalletLocation+"/"+Sender+".bin","r").read())
	ReciverBal = float( open(WalletLocation+"/"+Reciver+".bin","r").read())
	if os.path.exists(WalletLocation+"/"+Sender+".bin") and os.path.exists(WalletLocation+"/"+Reciver+".bin"):
		TransferedAmount = abs(float(message.content.split(" ")[2]))
		if SenderBal-TransferedAmount >= 0:
			SharedCode.AdjustWallet(Sender,round(-TransferedAmount,3))
			SharedCode.AdjustWallet(Reciver,round(TransferedAmount,3))
			await client.send_message(message.channel,("{0.author.mention} Payment Sent Of "+str(TransferedAmount)+"GRLC").format(message))
		else:
			await client.send_message(message.channel,"{0.author.mention} You dont have enough funds".format(message))
	else:
		await client.send_message(message.channel,"You or the Recipiant do not have a wallet!")
