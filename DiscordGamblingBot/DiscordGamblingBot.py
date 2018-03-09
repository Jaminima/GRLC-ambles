import os ,random,Wallets,Payments,Admin,Giveaway,Jackpot
os.chdir("D:\Programming\DiscordGamblingBot\DiscordGamblingBot\discord")
import discord,threading,subprocess
os.chdir("../")
from _thread import *
from discord.ext import commands

client = discord.Client()
WalletLocation = "D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/Wallets"
DepositAddresses = "D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/DepositAddresses"
AdminIDs = open("D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/AdminIDs.bin","r").read()
Payments.RunWallet()

@client.event
async def on_message(message):
    await messagehandler(message)

async def messagehandler(message):
    if message.author.id == "421228709425446912":
        null=1
    elif message.content.lower().startswith("?bal") and not "?balother" in message.content:
        await Wallets.Bal(message,client)
        await client.delete_message(message)

    elif message.content.lower().startswith("?balother"):
        await Wallets.BalOther(message,client)
        await client.delete_message(message)

    elif message.content.lower().startswith("?pay"):
        await Wallets.Pay(message,client)
        await client.delete_message(message)

    elif message.content.lower().startswith("?createfunds"):
        await Admin.CreateFunds(message,client)
        await client.delete_message(message)

    elif message.content.lower().startswith("?deposit"):
        await client.send_message(message.channel,"Deposit into: "+Payments.Deposit(message,client)+"Then type ?confirm <transid>")
        await client.delete_message(message)

    elif message.content.lower().startswith("?confirm"):
        await Payments.Confirm(message,client)
        await client.delete_message(message)

    elif message.content.lower().startswith("?withdraw"):
        await Payments.PayOut(message,client)
        await client.delete_message(message)

    elif message.content.lower().startswith("?help"):
        Help="<@"+message.author.id+">\n-------GRLC-ambles-------\nFeel free to donate GRLC using `?donate`\n"
        THelp="?help giveaway -- Show help for giveaways\n?help wallet -- Show help for wallets\n?help admin -- Show help for admin commands\n?help jackpot -- Show help for jackpot"
        try:
            if message.content.split(" ")[1].lower()=="giveaway":
                THelp="\n?giveaway join -- Join the giveaway (make sure you have done `?bal` to create your wallet!)\n?giveaway balance -- Gives giveaway value"
            elif message.content.split(" ")[1].lower()=="wallet":
                THelp="\n?bal -- View you balance\n?balother <userid> -- View balance of someone else\n?pay <userid> <amount>\n?deposit -- Gives an address for you to pay into\n?confirm <transid> -- Confirm payment\n?withdraw <amount> <address>"
            elif message.content.split(" ")[1].lower()=="admin":
                THelp="\n?giveaway start <GRLC> -- Start a giveaway\n?giveaway end -- End the giveaway\n?createfunds <userid> <GRLC> -- Its obvious\n?shutdown -- What do you think?"
            elif message.content.split(" ")[1].lower()=="jackpot":
                THelp="\n?jackpot join <GRLC> -- Join the Jackpot with <GRLC>\n?jackpot bal -- Return current Jackpot Balance\n?jackpot count -- Participants in the jackpot"
        except:
            null=0
        await client.send_message(message.channel,Help+THelp)
        await client.delete_message(message)

    elif message.content.lower().startswith("?giveaway bal"):
        bal = open("D:/Programming/DiscordGamblingBot/DiscordGamblingBot/UserInfo/GiveAwayValue.bin","r").read()
        if bal != 0:
            await client.send_message(message.channel,"Giveaway value is: "+bal+"GRLC")
        else:
            await client.send_message(message.channel,"Giveaway value is offline!")
        await client.delete_message(message)

    elif message.content.lower().startswith("?giveaway join"):
        await Giveaway.AddParticipant(message,client)
        await client.delete_message(message)

    elif message.content.lower().startswith("?giveaway start"):
        await Admin.StartGiveaway(message,client)
        await client.delete_message(message)

    elif message.content.lower().startswith("?giveaway end"):
        await Admin.EndGiveaway(message,client)
        await client.delete_message(message)

    elif message.content.lower().startswith("?donate"):
        await client.send_message(message.channel,"Feel free to donate GRLC to `GbWPXrJw2zN6wCu7bFSuGFBXaW4njEdBQV`")
        await client.delete_message(message)

    elif message.content.lower().startswith("?jackpot join"):
        await Jackpot.AddParticipant(message,client)
        await client.delete_message(message)

    elif message.content.lower().startswith("?jackpot bal"):
        await Jackpot.Balance(message,client)
        await client.delete_message(message)

    elif message.content.lower().startswith("?jackpot count"):
        await Jackpot.CountParticipants(message,client)
        await client.delete_message(message)

    elif message.content.lower().startswith("?shutdown"):
        await client.delete_message(message)
        if message.author.id in AdminIDs:
            await client.send_message(message.channel,"Bot Shutting Down")
            subprocess.Popen("./GarlicoinFiles/garlicoin-cli stop")
            exit()
        else:
            await client.send_message(message.channel,"You do not have required perms")

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
client.run('NDIxMjI4NzA5NDI1NDQ2OTEy.DYKLeA.cQqjgdyV6PaoPxV-Lf78ZA8X8Mo')
