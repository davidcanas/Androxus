# -*- coding: utf-8 -*-
# Androxus bot
# embedHelpCategory.py

__author__ = 'Rafael'

from datetime import datetime
from random import randint

import discord

from utils.Utils import capitalize
from utils.Utils import pegar_o_prefixo


async def embed_help_category(bot, ctx, category, color=None):
    """

    Args:
        bot (Classes.Androxus.Androxus): A instância do bot
        ctx (discord.ext.commands.context.Context): O contexto que vai ser usado para pegar o prefixo
        category (str): Categoria em que ser criado o embed
        color(hex): A cor que vai ser usada nos embeds (Default value = None)

    Returns:
        discord.Embed: O embed com todos os comandos da categoria passada

    """
    # se a pessoa usou o comando, mencionando o bot:
    if ctx.prefix.replace("!", "").replace(" ", "") == bot.user.mention:
        # vai pegar o prefixo que está no banco
        prefixo = await pegar_o_prefixo(bot, ctx)
    else:
        # se a pessoa não marcou o bot:
        prefixo = ctx.prefix
    if color is None:
        color = int(f'0x{randint(0, 255):02x}{randint(0, 255):02x}{randint(0, 255):02x}', 16)
    e = discord.Embed(title=f'Categoria: {bot.get_emoji_from_category(category)} {capitalize(category)}',
                      colour=discord.Colour(color),
                      description='Todos os comandos que estão nesta categoria!\nPara obter mais detalhes sobre '
                                  f'um comando, digite `{prefixo}help comando`!',
                      timestamp=datetime.utcnow())
    e.set_author(name=bot.user.name,
                 icon_url=bot.user.avatar_url)
    e.set_footer(text=f'{ctx.author}',
                 icon_url=ctx.author.avatar_url)
    comandos = [f'``{c.name}``' for c in bot.get_commands_from_category(category)]
    comandos = ', '.join(comandos)
    e.add_field(name='📖 Comandos:',
                value=comandos,
                inline=False)
    return e
