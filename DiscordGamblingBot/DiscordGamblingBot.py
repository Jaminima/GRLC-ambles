import os ,random,Wallets,Payments,Admin,Giveaway,Jackpot,threading,subprocess,SharedCode,Roulette
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

    elif message.content.lower().startswith("?bal bot"):
        await client.send_message(message.channel,"The bot has a total of: "+str(round(Payments.BotBal(),3))+"GRLC")

    elif message.content.lower().startswith("?bal") and not "?balother" in message.content:
        try :
            target = message.content.split(" ")[1]#forces error if operand not provided
            await Wallets.BalOther(message,client)
        except:
            await Wallets.Bal(message,client)
        await client.delete_message(message)

    elif message.content.lower().startswith("?pay"):
        try: await Wallets.Pay(message,client)
        except: await client.send_message(message.channel,"?pay <mention> <amount>")
        await client.delete_message(message)

#    elif message.content.lower().startswith("?createfunds"):
#        try: await Admin.CreateFunds(message,client)
#        except: await client.send_message(message.channel,"?createfunds <discordid> <amount>")
#        await client.delete_message(message)

    elif message.content.lower().startswith("?deposit"):
        mes = await client.send_message(message.channel,"Generating Address!\nExpect delays on commands!")
        try:
            await client.send_message(message.channel,"<@"+message.author.id+"> Deposit into: `"+Payments.Deposit(message,client)+"` Then type `?confirm <transid>`")
        except:
            await client.send_message(message.channel,"<@"+message.author.id+"> Failed to load/make deposit address!\nWait a min and type `?deposit` again.")
        await client.delete_message(message)
        await client.delete_message(mes)

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
        THelp="?help notification\n?help giveaway\n?help wallet\n?help roulette\n?help admin\n?help jackpot\n?help memes"
        try:
            if message.content.split(" ")[1].lower()=="giveaway":
                THelp="?giveaway join -- Join the giveaway (make sure you have done `?bal` to create your wallet!)\n?giveaway balance -- Gives giveaway value\n?giveaway count -- Participants in giveaway"
            elif message.content.split(" ")[1].lower()=="wallet":
                THelp="?bal <mention> -- View your/someone else balance\n?bal bot -- View bots balance\n?pay <mention> <amount>\n?deposit -- Gives an address for you to pay into\n?confirm <transid> -- Confirm payment\n?withdraw <amount> <address> -- must be minimum of 2GRLC"
            elif message.content.split(" ")[1].lower()=="admin":
                THelp="?giveaway start <GRLC> -- Start a giveaway\n?giveaway end -- End the giveaway\n?createfunds <mention> <GRLC> -- DISABLED\n?shutdown -- What do you think?"
            elif message.content.split(" ")[1].lower()=="jackpot":
                THelp="?jackpot join <GRLC> -- Join the Jackpot with <GRLC>\n?jackpot bal -- Return current Jackpot Balance\n?jackpot count -- Participants in the jackpot"
            elif message.content.split(" ")[1].lower()=="memes":
                THelp="?bad <mention> -- Tell someone they are bad!\n?good <mention> -- Tell someone they are good"
            elif message.content.split(" ")[1].lower()=="roulette":
                THelp="?roulette about -- Some information about the function of the game.\n?roulette join <GRLC> <Red/Green/Black> -- Join Roulette with bet on colour.\n?roulette increase <GRLC> -- Increase your bet by the value."
            elif message.content.split(" ")[1].lower()=="notification":
                THelp="?notification <enable/disbale> -- With this on we will notify you via a mention when a update/event occurs.\nIf it is disabled you wont get these as we wont mention everyone!"
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

    elif message.content.lower().startswith("?jackpot increase"):
        await Jackpot.IncreaseFunds(message,client)

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

    elif message.content.lower().startswith("?bad"):
        try: await client.send_message(message.channel,"<@"+SharedCode.DiscordID(message.content.split(" ")[1])+"> Is Bad!")
        except: await client.send_message(message.channel,"try `?bad <mention>`")

    elif message.content.lower().startswith("?good"):
        try: await client.send_message(message.channel,"<@"+SharedCode.DiscordID(message.content.split(" ")[1])+"> Is Good!")
        except: await client.send_message(message.channel,"try `?good <mention>`")

    elif message.content.lower().startswith("?roulette join"):
        try: await Roulette.AddParticipant(message,client)
        except: await client.send_message(message.channel,"try `?roulette join <GRLC> <Red/Green/Black>`")

    elif message.content.lower().startswith("?roulette increase"):
        try: await Roulette.IncreaseFunds(message,client)
        except: await client.send_message(message.channel,"try `?roulette increase <GRLC>`")

    elif message.content.lower().startswith("?roulette about"):
        await client.send_message(message.channel,"<@"+message.author.id+"> Roulette works by the user choosing a colour,\nA virtual bal (Random Number) is rolled.\nIf it lands on 0 the multiplyer is 4x.\nOtherwise it is 2x\n\nTo participate type `?roulette join <GRLC> <Red/Green/Black>`.\nThe wheel will be spun every ten minutes.")

    elif message.content.lower().startswith("?notification enable"):
        Role=discord.utils.get(message.server.roles, name="NotificationSquad")
        await client.add_roles(message.author,Role)
        await client.send_message(message.channel,"<@"+message.author.id+"> Welcome to the NotificationSquad!")

    elif message.content.lower().startswith("?notification disable"):
        Role=discord.utils.get(message.server.roles, name="NotificationSquad")
        await client.remove_roles(message.author,Role)
        await client.send_message(message.channel,"<@"+message.author.id+"> You have left the NotificationSquad!")

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await Roulette.Scheduler(client)
client.run('NDIxMjI4NzA5NDI1NDQ2OTEy.DYKLeA.cQqjgdyV6PaoPxV-Lf78ZA8X8Mo')
