import os ,random,Wallets,Payments,Admin,Giveaway,Jackpot,threading,subprocess
MainLocation="C:/Users/oscar/Desktop/DiscordGamblingBot/DiscordGamblingBot/"
os.chdir(MainLocation+"discord")
import discord,discord.ext
os.chdir("../")
client = discord.Client()
WalletLocation = MainLocation+"UserInfo/Wallets"
DepositAddresses = MainLocation+"UserInfo/DepositAddresses"
AdminIDs = open(MainLocation+"UserInfo/AdminIDs.bin","r").read()

import subprocess,json
WalletPassPhrase=input("Wallet Passphrase: ")

def RunWallet():
    subprocess.Popen("./GarlicoinFiles/garlicoind -datadir=./GarlicoinFiles/AppData -rpcport=52068 -port=52069")

def CreateNewRecivingAddress():
    address=subprocess.check_output("./GarlicoinFiles/garlicoin-cli -datadir=./GarlicoinFiles/AppData -rpcport=52068 -port=52069 getnewaddress").decode("utf-8")
    return address

def BotBal():
    baljson=subprocess.check_output("./GarlicoinFiles/garlicoin-cli -datadir=./GarlicoinFiles/AppData -rpcport=52068 -port=52069 -regtest listunspent").decode("utf-8")
    bal = 0
    for wallet in json.loads(baljson):
        bal += float(wallet["amount"])
    return bal

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
    TransId=message.content.split(" ")[1]
    Address=open(DepositAddresses+"/"+message.author.id+".bin","r").read()
    TransactionContent = Giveaway.GetTransaction(TransId)
    JsonTransaction = json.loads(TransactionContent)
    Confirmed = False
    for AddressN in range(0, len(JsonTransaction["vout"])):
        if (Address == JsonTransaction["vout"][AddressN]["scriptPubKey"]["addresses"][0]) and (TransId not in open(MainLocation+"UserInfo/UsedTransIDs.bin","r").read()):
            await client.send_message(message.channel,"Deposit Confirmed <@"+message.author.id+">")
            GRLC = float(JsonTransaction["vout"][AddressN]["value"])
            open(MainLocation+"UserInfo/UsedTransIDs.bin","a").write("\n"+TransId)
            try:
                CurBal=float(open(WalletLocation+"/"+message.author.id+".bin","r").read())
            except:
                CurBal=0
            open(WalletLocation+"/"+message.author.id+".bin","w").write(str(round(CurBal+GRLC,3)))
            Confirmed = True
    if Confirmed == False:
        await client.send_message(message.channel,"Invalid TransID <@"+message.author.id+">")

async def PayOut(message,client):
    if WalletPassPhrase=="":
        PayoutsOn=False
    else:
        PayoutsOn=True

    if PayoutsOn:
        GRLCOut=message.content.split(" ")[1]
        Address=message.content.split(" ")[2]
        CurGRLC=open(WalletLocation+"/"+message.author.id+".bin","r").read()
        if GRLCOut<=CurGRLC and float(GRLCOut)>=2.0:
            msg=await client.send_message(message.channel,"Sending Funds!\nExpect delays on commands!")
            open(WalletLocation+"/"+message.author.id+".bin","w").write(str(round(float(CurGRLC)-float(GRLCOut),3)))
            subprocess.call("./GarlicoinFiles/garlicoin-cli -rpcport=52068 -port=52069 -datadir=./GarlicoinFiles/AppData walletpassphrase "+WalletPassPhrase+" 60")
            TransId=subprocess.check_output("./GarlicoinFiles/garlicoin-cli -rpcport=52068 -port=52069 -datadir=./GarlicoinFiles/AppData sendtoaddress "+Address+" "+str(abs(round(float(GRLCOut)*0.9,3))),timeout=120).decode("utf-8")
            await client.delete_message(msg)
            await client.send_message(message.channel,"<@"+message.author.id+">Payment Sent. TransId: `"+TransId+"`\nIt may take around 15mins for the transaction to register!")
        else:
            await client.send_message(message.channel,"<@"+message.author.id+"> Not Enough GRLC or You are trying to withdraw >`2.0GRLC`!")
    else:
        await client.send_message(message.channel,"<@"+message.author.id+"> Payouts are disabled!\nThey should be enabled soon.")
