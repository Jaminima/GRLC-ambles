import os ,random,Wallets,Payments,Admin,Giveaway,Jackpot,threading,subprocess,SharedCode,datetime
MainLocation="C:/Users/oscar/Desktop/DiscordGamblingBot/DiscordGamblingBot/"
os.chdir(MainLocation+"discord")
import discord,discord.ext
os.chdir("../")
client = discord.Client()
WalletLocation = MainLocation+"UserInfo/Wallets"
DepositAddresses = MainLocation+"UserInfo/DepositAddresses"
AdminIDs = open(MainLocation+"UserInfo/AdminIDs.bin","r").read()

Participants=[]
Deposited=[]
Colour=[]

import time,asyncio

async def AddParticipant(message,client):
    DiscordId=message.author.id
    Deposit=round(float(message.content.split(" ")[2]),3)
    CurGRLC=float(open(WalletLocation+"/"+DiscordId+".bin","r").read())
    LColour=message.content.split(" ")[3].lower()
    if LColour in "redgreenblack":
        if CurGRLC>=Deposit:
            #SharedCode.AdjustWallet(DiscordId,-Deposit)
            Participants.append(DiscordId)
            Deposited.append(Deposit)
            Colour.append(LColour)
            await client.send_message(message.channel,"<@"+DiscordId+"> You deposited "+str(Deposit)+"GRLC into the roulete game!")
        else:
            await client.send_message(message.channel,"<@"+DiscordId+"> You dont have enough GRLC!")
    else:
        await client.send_message(message.channel,"<@"+DiscordId+"> You chose an invalid colour!\nTry `?roulete join <GRLC> <Red/Green/Black>`")

async def FinishGame(channel,client):
    global Participants,Deposited,Colour
    if datetime.datetime.now().minute%10==0 and len(Participants)>=2:
        WinningColourNum=random.randint(0,37)
        WinningColour=""
        Multiplyer=2
        if WinningColourNum==0:
            WinningColour="green"
            Multiplyer=4
        elif WinningColourNum%2==0:
            WinningColour="red"
        elif WinningColourNum%2==1:
            WinningColour="black"
        await client.send_message(channel,"The Winning Colour Is: "+WinningColour.upper()+"!!!!!")
        for i in range(0,len(Participants)):
            if Colour[i]==WinningColour:
                #SharedCode.AdjustWallet(Participants[i],Deposited[i]*Multiplyer)
                await client.send_message(channel,"<@"+Participants[i]+"> You won "+str(Deposited[i]*Multiplyer)+"GRLC!")
            else:
                await client.send_message(channel,"<@"+Participants[i]+"> You lost! Better luck next time...")
        Participants=[]
        Deposited=[]
        Colour=[]

async def IncreaseFunds(message,client):
    DiscordId=message.author.id
    Out=abs(round(float(message.content.split(" ")[2]),3))
    CurGRLC = float( open(WalletLocation+"/"+DiscordId+".bin","r").read())
    if DiscordId in Participants and CurGRLC>=Out:
        print("Yay")
        for pos in range(0,len(Participants)):
            if Participants[pos]==DiscordId:
                Deposited[pos]+=Out
                await client.send_message(message.channel,"<@"+DiscordId+"> You now have deposited: "+str(Deposited[pos]))
    else:
        print("Nay")
        await client.send_message(message.channel,"<@"+DiscordId+"> You are yet to enter the jackpot or dont have enough GRLC!\nType `?roulette join <grlc>` to participate.")

async def Scheduler(client):
    while True:
        await asyncio.sleep(10)
        await FinishGame(client.get_channel("422829572212523009"),client)
