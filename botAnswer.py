import asyncio

import discord


async def on_message(message, bot, creator, color):
    if isinstance(message.channel, discord.DMChannel):
        qt = bot.get_user(creator)
        chunks = [message.content[i:i + 1000] for i in range(0, len(message.content), 1000)]
        embed = discord.Embed(description=f'**Сообщение от {message.author.mention}**', color=color)
        for chunk in chunks:
            embed.add_field(name='', value=f'```fix\n{chunk}\n```', inline=False)
        embed.add_field(name='ID пользователя:', value=f'```fix\n{message.author.id}\n```', inline=True)
        await asyncio.sleep(3)
        await qt.send(embed=embed)

        bot_message = await message.channel.send('Loading…. █[][][][][][][][][] 10%')
        await asyncio.sleep(1)
        await bot_message.edit(content="Loading…. █████[][][][][] 50%")
        await asyncio.sleep(1)
        await bot_message.edit(content="Loading…. ████████[][] 80%")
        await asyncio.sleep(1)
        await bot_message.edit(content="Loading… ██████████████] 99%")
        await asyncio.sleep(1)
        await bot_message.edit(content="*•.¸♡ meow! ♡¸.•*")
        embed = discord.Embed(
            description=f'```fix\n Ваше сообщение отправлено, ожидайте, скоро на него ответит модератор\n```',
            color=color)
        await bot_message.edit(embed=embed)


async def msg(user, ctx, text, color):
    if user:
        embed = discord.Embed(description=f'**Сообщение от <@{ctx.message.author.id}>**', color=color)
        embed.add_field(name='', value=f'```fix\n{text}\n```', inline=False)
        await user.send(embed=embed)
        await ctx.message.author.send(f'**Отправлено {user}**')
