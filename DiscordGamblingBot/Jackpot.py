import os ,random,Wallets,Payments,Admin,Giveaway,Jackpot,threading,subprocess
MainLocation="C:/Users/oscar/Desktop/DiscordGamblingBot/DiscordGamblingBot/"
os.chdir(MainLocation+"discord")
import discord,discord.ext
os.chdir("../")
client = discord.Client()
WalletLocation = MainLocation+"UserInfo/Wallets"
DepositAddresses = MainLocation+"UserInfo/DepositAddresses"
AdminIDs = open(MainLocation+"UserInfo/AdminIDs.bin","r").read()

Participants = []
Deposited = []
Finishing = False

async def AddParticipant(message,client):
    if os.path.exists(WalletLocation+"/"+message.author.id+".bin"):
        CurBal = float( open(WalletLocation+"/"+message.author.id+".bin","r").read())
        GRLC = abs(float( message.content.split(" ")[2]))
        if CurBal>=GRLC and message.author.id not in Participants and GRLC>=0.1:
            NewBal = round(CurBal-GRLC,3)
            open(WalletLocation+"/"+message.author.id+".bin","w").write(str(NewBal))
            Participants.append(message.author.id)
            Deposited.append(GRLC)
            await client.send_message(message.channel,"<@"+message.author.id+"> You deposited "+str(GRLC)+"GRLC into the pot!")

        else:
            await client.send_message(message.channel,"<@"+message.author.id+"> You dont have enough GRLC or are already participating!\nOr you put < `0.1` GRLC")
    else:
        await client.send_message(message.channel,"<@"+message.author.id+"> You dont have a wallet, type `?bal`")
    await FinishCheck(message,client)

async def FinishCheck(message,client):
    global Participants,Deposited,Finishing
    TotalGRLC = 0
    for GRLC in Deposited:
        TotalGRLC+=float(GRLC)
    if len(Participants)>=5 and Finishing==False:
        Finishing=True
        WinnerAtGRLC=random.randint(0,int(round(TotalGRLC,0)))
        WinnerTotalGRLC = 0
        WinnerFound = False
        for i in range(0,len(Participants)):
            WinnerTotalGRLC+=float(Deposited[i])
            if WinnerTotalGRLC>=WinnerAtGRLC and WinnerFound==False:
                WinnerFound=True
                WinnerID=Participants[i]
        msg = await client.send_message(message.channel,"The winner is:")
        for i in range(0,10):
            CurUSR = Participants[random.randint(0,len(Participants)-1)]
            await client.edit_message(msg,"The winner is: <@"+CurUSR+">")
        await client.delete_message(msg)

        await client.send_message(message.channel,"<@"+WinnerID+"> Won "+str(TotalGRLC)+"GRLC!")
        CurGLRC=float( open(WalletLocation+"/"+WinnerID+".bin","r").read())
        open(WalletLocation+"/"+WinnerID+".bin","w").write(str(round(TotalGRLC+CurGLRC,3)))
        Participants=[]
        Deposited=[]
        Finishing=False

async def Balance(message,client):
    TotalGRLC = 0
    for GRLC in Deposited:
        TotalGRLC+=float(GRLC)
    await client.send_message(message.channel,"The Jackpot Balance is: "+str(TotalGRLC)+"GRLC")

async def CountParticipants(message,client):
    await client.send_message(message.channel,"<@"+message.author.id+"> There are: "+str(len(Participants))+"/5 Participants.\nType `?jackpot join <GRLC>` to participate.")

async def ReturnFunds(message,client):
    AtWho = ""
    for Pos in range(0,len(Participants)):
        AtWho+="<@"+Participants[Pos]+"> "
        CurBal =float( open(WalletLocation+"/"+Participants[Pos]+".bin","r").read())
        open(WalletLocation+"/"+Participants[Pos]+".bin","w").write(str(round(CurBal+Deposited[Pos],3)))
    await client.send_message(message.channel,AtWho+"The Jackpot has terminated. Your GRLC has been returned!")
