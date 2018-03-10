import os ,random,Wallets,Payments,Admin,Giveaway
os.chdir("D:\Programming\DiscordGamblingBot\DiscordGamblingBot\discord")
import discord
os.chdir("../")

WalletPassPhrase = input("WalletPassPhrase (blank for no payouts): ")
WalletLocation = "D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/Wallets"
DepositAddresses = "D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/DepositAddresses"
AdminIDs = open("D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/AdminIDs.bin","r").read()

import subprocess,json

def RunWallet():
    subprocess.Popen("./GarlicoinFiles/garlicoind -datadir=./GarlicoinFiles/AppData -rpcport=52068 -port=52069")

def CreateNewRecivingAddress():
    address=subprocess.check_output("./GarlicoinFiles/garlicoin-cli -datadir=./GarlicoinFiles/AppData -rpcport=52068 -port=52069 getnewaddress").decode("utf-8")
    return address

def Deposit(message,client):
    Target=message.author.id
    Address="ERROR"
    if os.path.exists(DepositAddresses+"/"+Target+".bin"):
        Address=open(DepositAddresses+"/"+Target+".bin","r").read()
    else:
        print("Generating Address")
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
        if (Address == JsonTransaction["vout"][AddressN]["scriptPubKey"]["addresses"][0]) and (TransId not in open("D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/UsedTransIDs.bin","r").read()):
            await client.send_message(message.channel,"Deposit Confirmed <@"+message.author.id+">")
            GRLC = float(JsonTransaction["vout"][AddressN]["value"])
            open("D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/UsedTransIDs.bin","a").write("\n"+TransId)
            CurBal=float(open(WalletLocation+"/"+message.author.id+".bin","r").read())
            open(WalletLocation+"/"+message.author.id+".bin","w").write(str(CurBal+GRLC))
            Confirmed = True
    if Confirmed == False:
        await client.send_message(message.channel,"Invalid TransID <@"+message.author.id+">")

async def PayOut(message,client):
    PayoutsOn=True

    if PayoutsOn:
        GRLCOut=message.content.split(" ")[1]
        Address=message.content.split(" ")[2]
        CurGRLC=open(WalletLocation+"/"+message.author.id+".bin","r").read()
        if GRLCOut<=CurGRLC:
            msg=await client.send_message(message.channel,"Sending Funds!\nExpect delays on commands!")
            open(WalletLocation+"/"+message.author.id+".bin","w").write(str(float(CurGRLC)-float(GRLCOut)))
            subprocess.call("./GarlicoinFiles/garlicoin-cli -rpcport=52068 -port=52069 -datadir=./GarlicoinFiles/AppData walletpassphrase "+WalletPassPhrase+" 60")
            TransId=subprocess.check_output("./GarlicoinFiles/garlicoin-cli -rpcport=52068 -port=52069 -datadir=./GarlicoinFiles/AppData sendtoaddress "+Address+" "+str(round(float(GRLCOut)*0.9,3)),timeout=120).decode("utf-8")
            await client.delete_message(msg)
            await client.send_message(message.channel,"Payment Sent. TransId: `"+TransId+"`\nIt make take around 15mins for the transaction to register!")
        else:
            await client.send_message(message.channel,"Not Enough GRLC")
    else:
        await client.send_message(message.channel,"<@"+message.author.id+"> Payouts are disabled!\nThey should be enabled soon.")
