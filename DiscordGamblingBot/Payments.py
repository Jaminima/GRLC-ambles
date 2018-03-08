import os ,random,Wallets,Payments,Admin,Giveaway
os.chdir("./discord")
import discord
os.chdir("../")

WalletPassPhrase = input("WalletPassPhrase (blank for no payouts): ")
WalletLocation = "D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/Wallets"
DepositAddresses = "D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/DepositAddresses"
AdminIDs = {"251754144958906369","421228709425446912"}

import subprocess,json

def RunWallet():
	subprocess.Popen("./GarlicoinFiles/garlicoind")

def UpdateWallet():
	subprocess.call("./GarlicoinFiles/garlicoin-cli getblockchaininfo")

def CreateNewRecivingAddress():
	address=subprocess.check_output("./GarlicoinFiles/garlicoin-cli getnewaddress").decode("utf-8")
	return address

def Deposit(message,client):
	Target=message.author.id
	Address="ERROR"
	if os.path.exists(DepositAddresses+"/"+Target+".bin"):
		Address=open(DepositAddresses+"/"+Target+".bin","r").read()
	else:
		Address=CreateNewRecivingAddress()
		open(DepositAddresses+"/"+Target+".bin","w").write(Address.splitlines()[0])
	return Address

async def Confirm(message,client):
	UpdateWallet()
	TransId=message.content.split(" ")[1]
	Address=open(DepositAddresses+"/"+message.author.id+".bin","r").read()
	TransactionContent = Giveaway.GetTransaction(TransId)
	JsonTransaction = json.loads(TransactionContent)
	if (Address == JsonTransaction["vout"][0]["scriptPubKey"]["addresses"][0]) and (TransId not in open("D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/UsedTransIDs.bin","r").read()):
		await client.send_message(message.channel,"Deposit Confirmed <@"+message.author.id+">")
		GRLC = float(JsonTransaction["vout"][0]["value"])
		open("D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/UsedTransIDs.bin","a").write("\n"+TransId)
		CurBal=float(open(WalletLocation+"/"+message.author.id+".bin","r").read())
		open(WalletLocation+"/"+message.author.id+".bin","w").write(str(CurBal+GRLC))
		await Wallets.Bal(message,client)
	else:
		await client.send_message(message.channel,"Invalid TransID <@"+message.author.id+">")

async def PayOut(message,client):
    PayoutsOn=False

    if PayoutsOn:
        GRLCOut=message.content.split(" ")[1]
        Address=message.content.split(" ")[2]
        CurGRLC=open(WalletLocation+"/"+message.author.id+".bin","r").read()
        if GRLCOut<=CurGRLC:
            open(WalletLocation+"/"+message.author.id+".bin","w").write(str(float(CurGRLC)-float(GRLCOut)))
            subprocess.call("./GarlicoinFiles/garlicoin-cli walletpassphrase "+DiscordGamblingBot+" 10")
            TransId=subprocess.check_output("./GarlicoinFiles/garlicoin-cli sendtoaddress "+Address+" "+str(round(float(GRLCOut)*0.9,3))).decode("utf-8")
            await client.send_message(message.channel,"Payment Sent. TransId: "+TransId)
        else:
            await client.send_message(message.channel,"Not Enough GRLC")
    else:
        await client.send_message(message.channel,"<@"+message.author.id+"> Payouts are disabled!\nThey should be enabled soon.")
