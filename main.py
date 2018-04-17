import discord
import os
import time
import asyncio

client = discord.Client()

is_prod = os.environ.get('IS_HEROKU', None)
if is_prod:
    token = os.environ.get('TOKEN')
else:
    import secreto
    token = secreto.token

def toint(s):
    try:
        return int(s)
    except ValueError:
        return float(s)

version = "Beta 1.0"
qntdd = int

@client.event
async def on_ready():
    print("=================================")
    print("Bot iniciado com sucesso!")
    print (client.user.name)
    print (client.user.id)
    print(f"Bot Version: {version}")
    print("=================================")
    await client.change_presence(game=discord.Game(name="no Orbit!"))

@client.event
async def on_message(message):
    if message.content.lower().startswith('/ping'):
        timep = time.time()
        emb = discord.Embed(title='Aguarde', color=0x565656)
        pingm0 = await client.send_message(message.channel, embed=emb)
        ping = time.time() - timep
        pingm1 = discord.Embed(title='Pong!', description=':ping_pong: Ping - %.01f segundos' % ping, color=0x15ff00)
        await client.edit_message(pingm0, embed=pingm1)

    if message.channel.id == ("425370391372890113"):
        await client.add_reaction(message, "✔")
        await client.add_reaction(message, "❌")

    elif message.content.lower().startswith('/avatar'):
        try:
            membro = message.mentions[0]
            avatarembed = discord.Embed(
                title="",
                color=0xFF8000,
                description="**[Clique aqui](" + membro.avatar_url + ") para acessar o link do avatar!**"
            )
            avatarembed.set_author(name=membro.name)
            avatarembed.set_image(url=membro.avatar_url)
            await client.send_message(message.channel, embed=avatarembed)
        except:
            avatarembed2 = discord.Embed(
                title="",
                color=0xFF8000,
                description="**[Clique aqui](" + message.author.avatar_url + ") para acessar o link do avatar!**"
            )
            avatarembed2.set_author(name=message.author.name)
            avatarembed2.set_image(url=message.author.avatar_url)
            await client.send_message(message.channel, embed=avatarembed2)

    if message.content.startswith('/jogando'):
        role = discord.utils.get(message.server.roles, name='👑 Dono')
        if not role in message.author.roles:
            return await client.send_message(message.channel, "❌ Você não possui permissão para executar este comando!")
        game = message.content[9:]
        await client.change_presence(game=discord.Game(name=game))
        await client.send_message(message.channel, "Status de jogo alterado para: " + game + " ")

    if message.content.lower().startswith("/say"):
        role = discord.utils.get(message.server.roles, name='🔸 Staff+')
        if not role in message.author.roles:
            return await client.send_message(message.channel, "❌ Você não possui permissão para executar este comando!")
        msg = message.content[5:2000]
        await client.send_message(message.channel, msg)
        await client.delete_message(message)

    if message.content.lower().startswith('/apagar'):
        role = discord.utils.get(message.server.roles, name='🔸 Staff+')
        if not role in message.author.roles:
            return await client.send_message(message.channel, "❌ Você não possui permissão para executar este comando!")
        qntdd = message.content.strip('/apagar ')
        qntdd = toint(qntdd)
        if qntdd <= 999:
            msg_author = message.author.mention
            await client.delete_message(message)
            # await asyncio.sleep(1)
            deleted = await client.purge_from(message.channel, limit=qntdd)
            botmsgdelete = await client.send_message(message.channel,   'Foi apagada {} mensagens com sucesso, {}.'.format(len(deleted), msg_author))
            await asyncio.sleep(5)
            await client.delete_message(botmsgdelete)

        else:
            botmsgdelete = await client.send_message(message.channel,
                                                     'Utilize o comando digitando /apagar <numero de 1 a 999>')
            await asyncio.sleep(5)
            await client.delete_message(message)
            await client.delete_message(botmsgdelete)

    if message.content.startswith('/aviso'):
        role = discord.utils.get(message.server.roles, name='🔸 Staff+')
        if not role in message.author.roles:
            return await client.send_message(message.channel, "❌ Você não possui permissão para executar este comando!")
        await client.delete_message(message)
        try:
            user = message.author
            msg = message.content[7:]

            embed = discord.Embed(
                title=" 📢 AVISO 📢",
                description="{}".format(msg),
                color=0xe67e22
            )
            embed.set_footer(
                text="Enviado por: " + user.name,
                icon_url=user.avatar_url
            )

            await client.send_message(message.channel, "@everyone")
            await client.send_message(message.channel, embed=embed)
        finally:
            pass
 
@client.event
async def on_member_join(member):

    grupo = discord.utils.find(lambda g: g.name == "🌿 Pendentes", member.server.roles)
    await client.add_roles(member, grupo)

    channel = client.get_channel('425368503097229312')
    serverchannel = member.server.default_channel
    msg = "→ {0} entrou no servidor!".format(member.mention, member.server.name)
    await client.send_message(channel, msg)

@client.event
async def on_member_remove(member):

    channel = client.get_channel('425368503097229312')
    serverchannel = member.server.default_channel
    msg = "← {0} saiu do servidor!".format(member.name)
    await client.send_message(channel, msg)

client.run(token)
