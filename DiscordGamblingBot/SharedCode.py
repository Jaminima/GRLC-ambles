MainLocation="C:/Users/oscar/Desktop/DiscordGamblingBot/DiscordGamblingBot/"
WalletLocation = MainLocation+"UserInfo/Wallets"
DepositAddresses = MainLocation+"/UserInfo/DepositAddresses"

import os
os.chdir(MainLocation+"discord")
import discord,discord.ext
os.chdir("../")
client = discord.Client()

def AdjustWallet(DiscordID,Change):
    try:
        CurBal = float(open(WalletLocation+"/"+DiscordID+".bin","r").read())
    except:
        CurBal = 0
    NewBal =round(CurBal+float(Change),3)
    open(WalletLocation+"/"+DiscordID+".bin","w").write(str(NewBal))

def DiscordID(IDorName):
    if "@" in IDorName.lower():
        if "!" in IDorName: return IDorName[3:len(IDorName)-1]
        else: return (IDorName[2:len(IDorName)-1])
    else:
        return IDorName
