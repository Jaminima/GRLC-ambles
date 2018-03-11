import os ,random,Wallets,Payments,Admin,Giveaway,Jackpot,threading,subprocess
MainLocation="C:/Users/oscar/Desktop/DiscordGamblingBot/DiscordGamblingBot/"
os.chdir(MainLocation+"discord")
import discord,discord.ext
os.chdir("../")
client = discord.Client()
WalletLocation = MainLocation+"UserInfo/Wallets"
DepositAddresses = MainLocation+"/UserInfo/DepositAddresses"
AdminIDs = open(MainLocation+"/UserInfo/AdminIDs.bin","r").read()
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
        try: await Wallets.BalOther(message,client)
        except: await client.send_message(message.channel,"?balother <discordid>")
        await client.delete_message(message)

    elif message.content.lower().startswith("?pay"):
        try: await Wallets.Pay(message,client)
        except: await client.send_message(message.channel,"?pay <discordid> <amount>")
        await client.delete_message(message)

#    elif message.content.lower().startswith("?createfunds"):
#        try: await Admin.CreateFunds(message,client)
#        except: await client.send_message(message.channel,"?createfunds <discordid> <amount>")
#        await client.delete_message(message)

    elif message.content.lower().startswith("?deposit"):
        try:
            await client.send_message(message.channel,"<@"+message.author.id+"> Deposit into: `"+Payments.Deposit(message,client)+"` Then type `?confirm <transid>`")
        except:
            await client.send_message(message.channel,"<@"+message.author.id+"> Failed to load/make deposit address!\nWait a min and type `?deposit` again.")
        await client.delete_message(message)

    elif message.content.lower().startswith("?confirm"):
        try: await Payments.Confirm(message,client)
        except: await client.send_message(message.channel,"?confirm <transactionid>")
        await client.delete_message(message)

    elif message.content.lower().startswith("?withdraw"):
        try: await Payments.PayOut(message,client)
        except: await client.send_message(message.channel,"?withdraw <amount> <address>")
        await client.delete_message(message)

    elif message.content.lower().startswith("?help"):
        Help="<@"+message.author.id+">\n-------GRLC-ambles-------\nFeel free to donate GRLC using `?donate`\nTo setup your wallet type `?bal` and you can now enter a giveaway or `?deposit`.\nFor more help contact an @Admin or type `?help <option>`\n\n"
        THelp="?help giveaway -- Show help for giveaways\n?help wallet -- Show help for wallets\n?help admin -- Show help for admin commands\n?help jackpot -- Show help for jackpot"
        try:
            if message.content.split(" ")[1].lower()=="giveaway":
                THelp="\n?giveaway join -- Join the giveaway (make sure you have done `?bal` to create your wallet!)\n?giveaway balance -- Gives giveaway value\n?giveaway count -- Participants in giveaway"
            elif message.content.split(" ")[1].lower()=="wallet":
                THelp="\n?bal -- View you balance\n?balother <userid> -- View balance of someone else\n?pay <userid> <amount>\n?deposit -- Gives an address for you to pay into\n?confirm <transid> -- Confirm payment\n?withdraw <amount> <address> -- must be minimum of 2GRLC"
            elif message.content.split(" ")[1].lower()=="admin":
                THelp="\n?giveaway start <GRLC> -- Start a giveaway\n?giveaway end -- End the giveaway\n?createfunds <userid> <GRLC> -- DISABLED\n?shutdown -- What do you think?"
            elif message.content.split(" ")[1].lower()=="jackpot":
                THelp="\n?jackpot join <GRLC> -- Join the Jackpot with <GRLC>\n?jackpot bal -- Return current Jackpot Balance\n?jackpot count -- Participants in the jackpot"
        except:
            null=0
        await client.send_message(message.channel,Help+THelp)
        await client.delete_message(message)

    elif message.content.lower().startswith("?giveaway bal"):
        bal = open(MainLocation+"UserInfo/GiveAwayValue.bin","r").read()
        if bal != 0:
            await client.send_message(message.channel,"Giveaway value is: "+bal+"GRLC")
        else:
            await client.send_message(message.channel,"Giveaway value is offline!")
        await client.delete_message(message)

    elif message.content.lower().startswith("?giveaway join"):
        await Giveaway.AddParticipant(message,client)
        await client.delete_message(message)

    elif message.content.lower().startswith("?giveaway start"):
        try: await Admin.StartGiveaway(message,client)
        except: await client.send_message(message.channel,"?giveaway start <amount>")
        await client.delete_message(message)

    elif message.content.lower().startswith("?giveaway end"):
        await Admin.EndGiveaway(message,client)
        await client.delete_message(message)

    elif message.content.lower().startswith("?giveaway count"):
        await client.send_message(message.channel,"Giveaway Participants: "+str(Giveaway.GiveawayCount()))

    elif message.content.lower().startswith("?giveaway"):
        await client.send_message(message.channel,"try `?giveaway join`")

    elif message.content.lower().startswith("?donate"):
        await client.send_message(message.channel,"Feel free to donate GRLC to `GbWPXrJw2zN6wCu7bFSuGFBXaW4njEdBQV`")
        await client.delete_message(message)

    elif message.content.lower().startswith("?jackpot join"):
        try: await Jackpot.AddParticipant(message,client)
        except: await client.send_message(message.channel,"?jackpot join <amount>")
        await client.delete_message(message)

    elif message.content.lower().startswith("?jackpot bal"):
        await Jackpot.Balance(message,client)
        await client.delete_message(message)

    elif message.content.lower().startswith("?jackpot count"):
        await Jackpot.CountParticipants(message,client)
        await client.delete_message(message)

    elif message.content.lower().startswith("?jackpot"):
        await client.send_message(message.channel,"try `?giveaway join/bal/count`")

    elif message.content.lower().startswith("?shutdown"):
        await client.delete_message(message)
        if message.author.id in AdminIDs:
            await client.send_message(message.channel,"Bot Shutting Down")
            await Jackpot.ReturnFunds(message,client)
            await Giveaway.ReturnFunds(message,client)
            subprocess.Popen("./GarlicoinFiles/garlicoin-cli -rpcport=52068 -port=52069 stop")
            exit()
        else:
            await client.send_message(message.channel,"You do not have required perms")

    elif message.content.lower().startswith("?about"):
        await client.send_message(message.channel,"<@"+message.author.id+"> This is a Disocrd Bot aimed at gambling GRLC\nCreated by <@251754144958906369>\nFor help type `?help`")

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
client.run('NDIxMjI4NzA5NDI1NDQ2OTEy.DYKLeA.cQqjgdyV6PaoPxV-Lf78ZA8X8Mo')
