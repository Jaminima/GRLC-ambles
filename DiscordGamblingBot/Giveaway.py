import os ,random,Wallets,Payments,Admin,Giveaway,Jackpot,threading,subprocess,SharedCode
MainLocation="C:/Users/oscar/Desktop/DiscordGamblingBot/DiscordGamblingBot/"
os.chdir(MainLocation+"discord")
import discord,discord.ext
os.chdir("../")
client = discord.Client()
WalletLocation = MainLocation+"UserInfo/Wallets"
DepositAddresses = MainLocation+"UserInfo/DepositAddresses"
AdminIDs = open(MainLocation+"UserInfo/AdminIDs.bin","r").read()

Participants = []

import urllib3

def GetBalance(wallet):
	http = urllib3.PoolManager()
	return http.request('GET',"https://garli.co.in/ext/getbalance/"+wallet).data.decode('utf-8')

def GetTransaction(transid):
	http = urllib3.PoolManager()
	return http.request('GET',"https://garli.co.in/api/getrawtransaction?txid="+transid+"&decrypt=1").data.decode('utf-8')

async def AddParticipant(message,client):
	if open(MainLocation+"UserInfo/GiveAwayValue.bin","r").read() == "0":
		await client.send_message(message.channel,"<@"+message.author.id+"> Giveaway is closed.")
	else:
		if message.author.id not in Participants:
			Participants.append(message.author.id)
			await client.send_message(message.channel,"<@"+message.author.id+"> Has joined the giveaway.")
		else:
			await client.send_message(message.channel,"<@"+message.author.id+"> You are already in this giveaway!")

async def StartGiveaway(message,client):
	giveaway=message.content.split(" ")[2]
	Participants=[]
	CurWallet=float(open(MainLocation+"UserInfo/GiveawayWallet.bin","r").read())
	if CurWallet >=round(float(giveaway),3):
		open(MainLocation+"UserInfo/GiveAwayValue.bin","w").write(giveaway)
		open(MainLocation+"UserInfo/GiveawayWallet.bin","w").write(str(round(CurWallet-float(giveaway),3)))
		await client.send_message(message.channel,"Created Giveaway.\nTo join type `?giveaway join`")
	else:
		await client.send_message(message.channel,"Not Enough GRLC in Bots GiveawayWallet")

def EndGiveaway(client):
	Winner = Participants[random.randint(0,len(Participants)-1)]
	CurBal = float( open(WalletLocation+"/"+Winner+".bin","r").read())
	GiveawayValue = float( open(MainLocation+"UserInfo/GiveAwayValue.bin","r").read())
	SharedCode.AdjustWallet(Winner,round(GiveawayValue,3))
	open(MainLocation+"UserInfo/GiveAwayValue.bin","w").write("0")
	return Winner

def GiveawayCount():
	return len(Participants)

async def ReturnFunds(message,client):
	GiveawayValue = open(MainLocation+"UserInfo/GiveAwayValue.bin","r").read()
	CurWallet = open(MainLocation+"UserInfo/GiveawayWallet.bin","r").read()
	open(MainLocation+"UserInfo/GiveawayWallet.bin","w").write(str(round(float(CurWallet)+float(GiveawayValue))))
	open(MainLocation+"UserInfo/GiveAwayValue.bin","w").write("0")
