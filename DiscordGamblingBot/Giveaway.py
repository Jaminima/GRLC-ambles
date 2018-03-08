import os ,random,Wallets,Payments,Admin,Giveaway
os.chdir("D:\Programming\DiscordGamblingBot\DiscordGamblingBot\discord")
import discord
os.chdir("../")

WalletLocation = "D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/Wallets"
DepositAddresses = "D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/DepositAddresses"
AdminIDs = {"251754144958906369","421228709425446912"}

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

def StartGiveaway(giveaway):
	Participants=[]
	open("D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/GiveAwayValue.bin","w").write(giveaway)

def EndGiveaway(client):
	Winner = Participants[random.randint(0,len(Participants)-1)]
	CurBal = float( open(WalletLocation+"/"+Winner+".bin","r").read())
	GiveawayValue = int( open("D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/GiveAwayValue.bin","r").read())
	open(WalletLocation+"/"+Winner+".bin","w").write(str(CurBal+GiveawayValue))
	open("D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/GiveAwayValue.bin","w").write("0")
	return Winner