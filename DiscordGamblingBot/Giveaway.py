import os ,random,Wallets,Payments,Admin,Giveaway
os.chdir("./discord")
import discord
os.chdir("../")

WalletLocation = "D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/Wallets"
DepositAddresses = "D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/DepositAddresses"
AdminIDs = {"251754144958906369"}

import urllib3

def GetBalance(wallet):
	http = urllib3.PoolManager()
	return http.request('GET',"https://garli.co.in/ext/getbalance/"+wallet).data.decode('utf-8')

def GetTransaction(transid):
	http = urllib3.PoolManager()
	return http.request('GET',"https://garli.co.in/api/getrawtransaction?txid="+transid+"&decrypt=1").data.decode('utf-8')