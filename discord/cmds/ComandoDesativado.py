# coding=utf-8
# Androxus bot
# ComandoDesativado.py

__author__ = 'Rafael'

from datetime import datetime
from discord.ext import commands
import discord
from discord.Utils import random_color, pegar_o_prefixo
from discord.dao.ComandoDesativadoDao import ComandoDesativadoDao


class ComandoDesativado(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, aliases=['help_disable_command', 'help_dc'])
    async def help_desativar_comando(self, ctx):
        prefixo = pegar_o_prefixo(None, ctx)
        embed = discord.Embed(title=f"``{prefixo}desativar_comando``", colour=discord.Colour(random_color()),
                              description="Desativa um comando!",
                              timestamp=datetime.utcfromtimestamp(datetime.now().timestamp()))
        embed.set_author(name="Androxus", icon_url=f"{self.bot.user.avatar_url}")
        embed.set_footer(text=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        embed.add_field(name="**Como usar?**",
                        value=f"``{prefixo}desativar_comando`` ``\"<comando>\"``",
                        inline=False)
        embed.add_field(
            name="Tudo que estiver entre **<>** são obrigatorio, e tudo que estiver entre **[]** são opcionais.",
            value="<a:jotarodance:754702437901664338>", inline=False)
        embed.add_field(name="Exemplo:",
                        value=f"``{prefixo}desativar_comando`` ``say``\n(Esse comando desativa o comando \"say\" no seu servidor!)",
                        inline=False)
        embed.add_field(name=":twisted_rightwards_arrows: Sinônimos:",
                        value=f"``{prefixo}disable_command``, ``{prefixo}dc``", inline=False)
        embed.add_field(name=":exclamation:Requisitos:",
                        value="Você precisa ter permissão de administrador para usar esse comando!", inline=False)
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(aliases=['disable_command', 'dc'], description='Desativa comandos!')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def desativar_comando(self, ctx, comando=None):
        if (comando is None) or (comando.lower() == 'desativar_comando') or (comando.lower() == 'reativar_comando'):
            await self.help_desativar_comando(ctx)
            return
        if ComandoDesativadoDao().create(ctx.guild.id, comando):
            embed = discord.Embed(title=f'Comando desativado com sucesso!', colour=discord.Colour(random_color()),
                                  description="<a:aeeee:754779905782448258>",
                                  timestamp=datetime.utcfromtimestamp(datetime.now().timestamp()))
            embed.set_author(name="Androxus", icon_url=f"{self.bot.user.avatar_url}")
            embed.set_footer(text=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            embed.add_field(name=f"Comando: {comando}",
                            value="\uFEFF",
                            inline=False)
            await ctx.send(embed=embed)

    @commands.command(hidden=True, aliases=['help_reactivate_command'])
    async def help_reativar_comando(self, ctx):
        prefixo = pegar_o_prefixo(None, ctx)
        embed = discord.Embed(title=f"``{prefixo}reativar_comando``", colour=discord.Colour(random_color()),
                              description="Desativa um comando!",
                              timestamp=datetime.utcfromtimestamp(datetime.now().timestamp()))
        embed.set_author(name="Androxus", icon_url=f"{self.bot.user.avatar_url}")
        embed.set_footer(text=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        embed.add_field(name="**Como usar?**",
                        value=f"``{prefixo}reativar_comando`` ``\"<comando>\"``",
                        inline=False)
        embed.add_field(
            name="Tudo que estiver entre **<>** são obrigatorio, e tudo que estiver entre **[]** são opcionais.",
            value="<a:jotarodance:754702437901664338>", inline=False)
        embed.add_field(name="Exemplo:",
                        value=f"``{prefixo}reativar_comando`` ``\"say\"``\n(Esse comando reativa o comando \"say\" no seu servidor!)",
                        inline=False)
        embed.add_field(name=":twisted_rightwards_arrows: Sinônimos:",
                        value=f"``{prefixo}reactivate_command``", inline=False)
        embed.add_field(name=":exclamation:Requisitos:",
                        value="Você precisa ter permissão de administrador para usar esse comando!", inline=False)
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(aliases=['reactivate_command'], description='Reativa comando!')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def reativar_comando(self, ctx, comando=None):
        if (comando is None):
            await self.help_desativar_comando(ctx)
            return
        if ComandoDesativadoDao().delete(ctx.guild.id, comando):
            embed = discord.Embed(title=f'Comando reativado com sucesso!', colour=discord.Colour(random_color()),
                                  description="<a:aeeee:754779905782448258>",
                                  timestamp=datetime.utcfromtimestamp(datetime.now().timestamp()))
            embed.set_author(name="Androxus", icon_url=f"{self.bot.user.avatar_url}")
            embed.set_footer(text=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ComandoDesativado(bot))
