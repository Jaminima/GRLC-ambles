import os ,random,Wallets,Payments,Admin,Giveaway
os.chdir("D:\Programming\DiscordGamblingBot\DiscordGamblingBot\discord")
import discord
os.chdir("../")

WalletLocation = "D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/Wallets"
DepositAddresses = "D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/DepositAddresses"
AdminIDs = open("D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/AdminIDs.bin","r").read()

Participants = []
Deposited = []

async def AddParticipant(message,client):
    if os.path.exists(WalletLocation+"/"+message.author.id+".bin"):
        CurBal = float( open(WalletLocation+"/"+message.author.id+".bin","r").read())
        GRLC = float( message.content.split(" ")[2])
        if CurBal>=GRLC and message.author.id not in Participants:
            NewBal = CurBal-GRLC
            open(WalletLocation+"/"+message.author.id+".bin","w").write(str(NewBal))
            Participants.append(message.author.id)
            Deposited.append(GRLC)
            await client.send_message(message.channel,"<@"+message.author.id+"> You deposited "+str(GRLC)+"GRLC into the pot!")

        else:
            await client.send_message(message.channel,"<@"+message.author.id+"> You dont have enough GRLC or are already participating!")
    else:
        await client.send_message(message.channel,"<@"+message.author.id+"> You dont have a wallet, type `?bal`")
    await FinishCheck(message,client)

async def FinishCheck(message,client):
    global Participants,Deposited
    TotalGRLC = 0
    for GRLC in Deposited:
        TotalGRLC+=float(GRLC)
    if len(Participants)>=5:
        WinnerAtGRLC=random.randint(0,TotalGRLC)
        WinnerTotalGRLC = 0
        WinnerFound = False
        for i in range(0,len(Participants)):
            WinnerTotalGRLC+=float(Deposited[i])
            if WinnerTotalGRLC>=WinnerAtGRLC and WinnerFound==False:
                WinnerFound=True
                WinnerID=Participants[i]

        await client.send_message(message.channel,"<@"+WinnerID+"> Won "+str(TotalGRLC)+"GRLC!")
        CurGLRC=float( open(WalletLocation+"/"+WinnerID+".bin","r").read())
        open(WalletLocation+"/"+WinnerID+".bin","w").write(str(TotalGRLC+CurGLRC))
        Participants=[]
        Deposited=[]

async def Balance(message,client):
    TotalGRLC = 0
    for GRLC in Deposited:
        TotalGRLC+=float(GRLC)
    await client.send_message(message.channel,"The Jackpot Balance is: "+str(TotalGRLC)+"GRLC")

async def CountParticipants(message,client):
    await client.send_message(message.channel,"<@"+message.author.id+"> There are: "+str(len(Participants))+"/5 Participants.\nType `?jackpot join <GRLC>` to participate.") 