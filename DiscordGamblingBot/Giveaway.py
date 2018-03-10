import os ,random,Wallets,Payments,Admin,Giveaway
os.chdir("D:\Programming\DiscordGamblingBot\DiscordGamblingBot\discord")
import discord
os.chdir("../")

WalletLocation = "D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/Wallets"
DepositAddresses = "D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/DepositAddresses"
AdminIDs = open("D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/AdminIDs.bin","r").read()

Participants = []

import urllib3

def GetBalance(wallet):
	http = urllib3.PoolManager()
	return http.request('GET',"https://garli.co.in/ext/getbalance/"+wallet).data.decode('utf-8')

def GetTransaction(transid):
	http = urllib3.PoolManager()
	return http.request('GET',"https://garli.co.in/api/getrawtransaction?txid="+transid+"&decrypt=1").data.decode('utf-8')

async def AddParticipant(message,client):
	if open("D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/GiveAwayValue.bin","r").read() == "0":
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
	CurWallet=float(open("D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/GiveawayWallet.bin","r").read())
	if CurWallet >=round(float(giveaway),3):
		open("D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/GiveAwayValue.bin","w").write(giveaway)
		open("D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/GiveawayWallet.bin","w").write(str(round(CurWallet-float(giveaway),3)))
		await client.send_message(message.channel,"Created Giveaway.\nTo join type `?giveaway join`")
	else:
		await client.send_message(message.channel,"Not Enough GRLC in Bots GiveawayWallet")

def EndGiveaway(client):
	Winner = Participants[random.randint(0,len(Participants)-1)]
	CurBal = float( open(WalletLocation+"/"+Winner+".bin","r").read())
	GiveawayValue = float( open("D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/GiveAwayValue.bin","r").read())
	open(WalletLocation+"/"+Winner+".bin","w").write(str(round(CurBal+GiveawayValue,3)))
	open("D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/GiveAwayValue.bin","w").write("0")
	return Winner

def GiveawayCount():
	return len(Participants)

async def ReturnFunds(message,client):
	GiveawayValue = open("D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/GiveAwayValue.bin","r").read()
	CurWallet = open("D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/GiveawayWallet.bin","r").read()
	open("D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/GiveawayWallet.bin","w").write(str(round(float(CurWallet)+float(GiveawayValue))))
	open("D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/GiveAwayValue.bin","w").write("0")
