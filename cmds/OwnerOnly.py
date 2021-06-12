# -*- coding: utf-8 -*-
# Androxus bot
# OwnerOnly.py

__author__ = 'Rafael'

import ast
import asyncio
from datetime import datetime
from inspect import getmodule
from io import BytesIO
from traceback import format_exc

import asyncpg
import discord
from discord.ext import commands
from stopwatch import Stopwatch

from EmbedGenerators.HelpGroup import embed_help_group
from database.Models.ComandoDesativado import ComandoDesativado
from database.Models.ComandoPersonalizado import ComandoPersonalizado
from database.Models.Servidor import Servidor
from database.Repositories.BlacklistRepository import BlacklistRepository
from database.Repositories.ComandoDesativadoRepository import ComandoDesativadoRepository
from database.Repositories.ComandoPersonalizadoRepository import ComandoPersonalizadoRepository
from database.Repositories.InformacoesRepository import InformacoesRepository
from database.Repositories.ServidorRepository import ServidorRepository
from utils import permissions
from utils.Utils import get_emoji_dance, datetime_format, get_emojis_json, is_number, prettify_number, pretty_i


class OwnerOnly(commands.Cog):
    # algumas outras funções que só o dono do bot pode usar
    def __init__(self, bot):
        """

        Args:
            bot (Classes.Androxus.Androxus): Instância do bot

        """
        self.bot = bot

    @commands.group(name='owner', case_insensitive=True, invoke_without_command=True, ignore_extra=False,
                    aliases=['dev_only', 'owner_only', 'dono'])
    @commands.check(permissions.is_owner)
    async def owner_gp(self, ctx):
        await ctx.reply(embed=await embed_help_group(ctx), mention_author=False)

    @owner_gp.command(name='desativar_erros', aliases=['desativar_tratamento_de_erro', 'erros_off'])
    @commands.check(permissions.is_owner)
    async def _desativar_erros(self, ctx):
        self.bot.unload_extension('events.ErrorCommands')
        await ctx.reply('Tratamento de erro desativado!', mention_author=False)

    @owner_gp.command(name='ativar_erros', aliases=['ativar_tratamento_de_erro', 'erros_on'])
    @commands.check(permissions.is_owner)
    async def _ativar_erros(self, ctx):
        self.bot.load_extension('events.ErrorCommands')
        await ctx.reply('Tratamento de erro ativado!', mention_author=False)

    @owner_gp.command(name='game', aliases=['jogar', 'status'])
    @commands.check(permissions.is_owner)
    async def _game(self, ctx, *, name=None):
        if name is None:
            self.bot.mudar_status = True
            embed = discord.Embed(title=f'Agora meus status vão ficar alterado!',
                                  colour=discord.Colour.random(),
                                  description=get_emoji_dance(),
                                  timestamp=datetime.utcnow())
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            embed.set_footer(text=f'{ctx.author}', icon_url=ctx.author.avatar.url)
        else:
            self.bot.mudar_status = False
            await self.bot.change_presence(activity=discord.Game(name=name))
            embed = discord.Embed(title=f'Status alterado!',
                                  colour=discord.Colour.random(),
                                  description=f'Agora eu estou jogando ``{name}``',
                                  timestamp=datetime.utcnow())
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            embed.set_footer(text=f'{ctx.author}', icon_url=ctx.author.avatar.url)
        await ctx.reply(embed=embed, mention_author=False)

    @owner_gp.command(name='kill', aliases=['reboot', 'reiniciar', 'shutdown', 'poweroff'])
    @commands.check(permissions.is_owner)
    async def _kill(self, ctx):
        await ctx.reply(f'Reiniciando {self.bot.get_emoji("loading")}', mention_author=False)
        await self.bot.close()
        raise SystemExit('Rebooting...')

    @owner_gp.command(name='sql', aliases=['query', 'query_sql', 'dbeval'])
    @commands.check(permissions.is_owner)
    async def _sql(self, ctx, *, query=None):
        if query is not None:
            send_file = False
            msg_file = None
            mode = 'insertion'
            emojis = {
                'ids': get_emojis_json()['ids'],
                'check_verde': self.bot.get_emoji('check_verde'),
                'atencao': self.bot.get_emoji('atencao'),
                'warning_flag': self.bot.get_emoji('warning_flag')
            }
            emojis['cadeado'] = self.bot.get_emoji(emojis['ids']['cadeado'])
            emojis['desativado'] = self.bot.get_emoji(emojis['ids']['desativado'])
            emojis['ativado'] = self.bot.get_emoji(emojis['ids']['ativado'])

            def check(reaction_, user_):
                author = user_.id == ctx.author.id
                reactions = (str(reaction_.emoji) == str(emojis['cadeado'])) or (
                        str(reaction_.emoji) == str(emojis['desativado'])) or (
                                    str(reaction_.emoji) == str(emojis['ativado']))
                message_check = reaction_.message == msg_bot
                return author and reactions and message_check

            if not query.endswith(';'):
                query += ';'
            closed_embed = discord.Embed(title=f'Query fechada {emojis["check_verde"]}',
                                         colour=discord.Colour(0xff6961),
                                         timestamp=datetime.utcnow())
            closed_embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar.url}')
            try:
                async with self.bot.db_connection.acquire() as conn:
                    await conn.execute(query)
            except:
                erro_embed = discord.Embed(title=f'{emojis["atencao"]} Erro ao executar query',
                                           colour=discord.Colour(0xff6961),
                                           timestamp=datetime.utcnow())
                erro_embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar.url}')
                erro_embed.add_field(name='📥 Input',
                                     value=f'```sql\n{query}```',
                                     inline=False)

                msg_erro = '\n'.join(f'- {c}' for c in format_exc().splitlines())
                if len(msg_erro) <= 1_000:
                    erro_embed.add_field(name=f'{self.bot.get_emoji("warning_flag")} Erro',
                                         value=f'```diff\n{msg_erro}```',
                                         inline=False)
                else:
                    send_file = True
                    erro_embed.add_field(name='😅 infelizmente o erro foi muito grande, então enviei '
                                              'o erro completo num arquivo.',
                                         value='** **',
                                         inline=False)
                msg_bot = await ctx.send(embed=erro_embed)
                if send_file:
                    msg_file = await ctx.send(file=discord.File(
                        filename='erro.log',
                        fp=BytesIO(format_exc().encode('utf-8'))
                    ))
                await msg_bot.add_reaction(emojis['ativado'])
                try:
                    await self.bot.wait_for('reaction_add', timeout=120.0, check=check)
                except asyncio.TimeoutError:
                    pass
                await msg_bot.remove_reaction(emojis['ativado'], ctx.me)
                await msg_bot.edit(embed=closed_embed, allowed_mentions=discord.AllowedMentions(replied_user=False))
                if send_file and msg_file is not None:
                    await msg_file.delete()
            else:
                embed = discord.Embed(title=f'{emojis["check_verde"]} Query executada com sucesso!',
                                      colour=discord.Colour(0xbdecb6),
                                      timestamp=datetime.utcnow())
                embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar.url}')
                embed.add_field(name='📥 Input',
                                value=f'```sql\n{query}```',
                                inline=False)
                if 'select' in query.lower():
                    mode = 'selection'
                if mode == 'selection':
                    async with self.bot.db_connection.acquire() as conn:
                        select_result = []
                        for record in await conn.fetch(query):
                            try:
                                select_result.append(dict(record))
                            except ValueError:
                                select_result.append(tuple(record))
                        select_result = tuple(select_result)
                        if len(select_result) == 1:
                            select_result_str = str(pretty_i(select_result[0]))
                        elif len(select_result) > 1:
                            select_result_str = str(pretty_i(select_result))
                        else:
                            select_result_str = '()'
                        if len(select_result_str) <= 1_000:
                            embed.add_field(name='📤 Output',
                                            value=f'```py\n{select_result_str}```',
                                            inline=False)
                        else:
                            send_file = True
                            embed.add_field(name='😅 infelizmente o resultado ficou muito grande, então '
                                                 'enviei o erro completo num arquivo.',
                                            value='** **',
                                            inline=False)
                embed.add_field(name='** **',
                                value=f'Essa mensagem será fechada em 2 minutos 🙂',
                                inline=False)
                msg_bot = await ctx.send(embed=embed)
                if send_file:
                    msg_file = await ctx.send(file=discord.File(
                        filename='result.py',
                        fp=BytesIO(select_result_str.encode('utf-8'))
                    ))
                await msg_bot.add_reaction(emojis['desativado'])
                await msg_bot.add_reaction(emojis['cadeado'])
                try:
                    reaction, _ = await self.bot.wait_for('reaction_add', timeout=120.0, check=check)
                    if str(reaction.emoji) == str(emojis['desativado']):
                        await msg_bot.edit(embed=closed_embed,
                                           allowed_mentions=discord.AllowedMentions(replied_user=False))
                        if send_file and msg_file is not None:
                            await msg_file.delete()
                    elif str(reaction.emoji) == str(emojis['cadeado']):
                        embed.remove_field(-1)
                        await msg_bot.edit(embed=embed, allowed_mentions=discord.AllowedMentions(replied_user=False))
                except asyncio.TimeoutError:
                    await msg_bot.edit(embed=closed_embed, allowed_mentions=discord.AllowedMentions(replied_user=False))
                    if send_file and msg_file is not None:
                        await msg_file.delete()
                await msg_bot.remove_reaction(emojis['desativado'], ctx.me)
                await msg_bot.remove_reaction(emojis['cadeado'], ctx.me)

        else:
            return await self.bot.send_help(ctx)

    # base: https://gist.github.com/nitros12/2c3c265813121492655bc95aa54da6b9
    def __insert_returns(self, body):
        if isinstance(body[-1], ast.Expr):
            body[-1] = ast.Return(body[-1].value)
            ast.fix_missing_locations(body[-1])
        if isinstance(body[-1], ast.If):
            self.__insert_returns(body[-1].body)
            self.__insert_returns(body[-1].orelse)
        if isinstance(body[-1], ast.With):
            self.__insert_returns(body[-1].body)

    @owner_gp.command(name='eval', aliases=['ev', 'e'])
    @commands.check(permissions.is_owner)
    async def _eval(self, ctx, *, cmd):
        emojis = {
            'ids': get_emojis_json()['ids'],
            'check_verde': self.bot.get_emoji('check_verde'),
            'atencao': self.bot.get_emoji('atencao'),
            'warning_flag': self.bot.get_emoji('warning_flag')
        }
        emojis['cadeado'] = self.bot.get_emoji(emojis['ids']['cadeado'])
        emojis['desativado'] = self.bot.get_emoji(emojis['ids']['desativado'])
        emojis['ativado'] = self.bot.get_emoji(emojis['ids']['ativado'])
        send_file = False
        msg_file = None

        def check(reaction_, user_):
            author = user_.id == ctx.author.id
            reactions = (str(reaction_.emoji) == str(emojis['cadeado'])) or (
                    str(reaction_.emoji) == str(emojis['desativado'])) or (
                                str(reaction_.emoji) == str(emojis['ativado']))
            message_check = reaction_.message == msg_bot
            return author and reactions and message_check

        closed = discord.Embed(title=f'Eval fechada {emojis["check_verde"]}',
                               colour=discord.Colour(0xff6961),
                               timestamp=datetime.utcnow())
        closed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar.url}')
        execute_cmd = ''
        try:
            fn_name = '_eval_function'
            if cmd.startswith('```py'):
                cmd = cmd[5:]
            elif cmd.startswith('```'):
                cmd = cmd[3:]
            if cmd.endswith('```'):
                cmd = cmd[:-3]
            if cmd.startswith('\n'):
                cmd = cmd[1:]
            # add a layer of indentation
            cmd = '\n'.join(f'    {i}' for i in cmd.splitlines())
            # wrap in async def body
            body = f'async def {fn_name}():\n{cmd}'
            # se o comando começar com #s, vai emitir a mensagem do retorno do comando
            retornar_algo = not cmd.splitlines()[0].replace(' ', '').startswith('#s')
            execute_cmd = body
            if len(execute_cmd) > 1000:
                execute_cmd = f'{execute_cmd[:1000]}\n...'
            parsed = ast.parse(body)
            body = parsed.body[0].body

            self.__insert_returns(body)

            env = {
                'self': self,
                'discord': discord,
                'asyncpg': asyncpg,
                'asyncio': asyncio,
                'commands': commands,
                'datetime': datetime,
                'BlacklistRepository': BlacklistRepository,
                'ComandoDesativadoRepository': ComandoDesativadoRepository,
                'ComandoPersonalizadoRepository': ComandoPersonalizadoRepository,
                'InformacoesRepository': InformacoesRepository,
                'ServidorRepository': ServidorRepository,
                'ComandoDesativado': ComandoDesativado,
                'ComandoPersonalizado': ComandoPersonalizado,
                'Servidor': Servidor,
                'permissions': permissions,
                'Stopwatch': Stopwatch,
                'ctx': ctx,
                'bot': self.bot,
                'author': ctx.author,
                'message': ctx.message,
                'msg': ctx.message,
                'channel': ctx.channel,
                'guild': ctx.guild,
                '_find': discord.utils.find,
                '_get': discord.utils.get,
                '__import__': __import__
            }
            utils_module = getmodule(get_emoji_dance)
            for attr_name in dir(utils_module):
                try:
                    attr = getattr(utils_module, attr_name)
                except AttributeError:
                    continue
                if getmodule(attr) == utils_module:
                    env[attr_name] = attr
            exec(compile(parsed, filename='<ast>', mode='exec'), env)
            execution_time = Stopwatch()
            result = await eval(f'{fn_name}()', env)
            execution_time.stop()
        except:
            erro_embed = discord.Embed(title=f'{emojis["atencao"]} Erro no comando eval',
                                       colour=discord.Colour(0xff6961),
                                       timestamp=datetime.utcnow())
            erro_embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar.url}')
            erro_embed.add_field(name='📥 Input',
                                 value=f'```py\n{execute_cmd}```',
                                 inline=False)
            erro_msg = '\n'.join(f'- {line}' for line in format_exc().splitlines())
            if len(erro_msg) <= 1500:
                erro_embed.add_field(name=f'{emojis["warning_flag"]} Erro',
                                     value=f'```diff\n{erro_msg}```',
                                     inline=False)
            else:
                send_file = True
                erro_embed.add_field(name='** **',
                                     value='😅 infelizmente o erro foi muito grande, então enviei '
                                           'o erro completo num arquivo.',
                                     inline=False)
            msg_bot = await ctx.send(embed=erro_embed)
            if send_file:
                msg_file = await ctx.send(file=discord.File(
                    filename='erro.log',
                    fp=BytesIO(format_exc().encode('utf-8'))
                ))
            await msg_bot.add_reaction(emojis['ativado'])
            try:
                await self.bot.wait_for('reaction_add', timeout=120.0, check=check)
            except asyncio.TimeoutError:
                pass
            await msg_bot.remove_reaction(emojis['ativado'], ctx.me)
            await msg_bot.edit(embed=closed, allowed_mentions=discord.AllowedMentions(replied_user=False))
            if send_file and msg_file is not None:
                await msg_file.delete()
        else:
            if retornar_algo:
                e = discord.Embed(title=f'Comando eval executado com sucesso!',
                                  colour=discord.Colour(0xbdecb6),
                                  timestamp=datetime.utcnow())
                e.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar.url}')
                e.add_field(name='📥 Input',
                            value=f'```py\n{execute_cmd}```',
                            inline=False)
                result_type = type(result)
                if is_number(str(result)):
                    result_str = prettify_number(str(result))
                else:
                    result_str = str(pretty_i(result))
                if len(result_str) <= 1_000:
                    e.add_field(name='📤 Output',
                                value=f'```py\n{result_str}```',
                                inline=False)
                else:
                    send_file = True
                    e.add_field(name='** **',
                                value='😅 infelizmente o resultado ficou muito grande, então '
                                      'enviei o erro completo num arquivo.',
                                inline=False)
                e.add_field(name='🤔 Tipo do return',
                            value=f'```py\n{result_type}```',
                            inline=False)
                e.add_field(name='⌚ Tempo de execução',
                            value=f'```md\n{str(execution_time)}\n====```',
                            inline=False)
                e.add_field(name='** **',
                            value=f'Essa mensagem será fechada em 2 minutos 🙂',
                            inline=False)
                msg_bot = await ctx.send(embed=e)
                if send_file:
                    msg_file = await ctx.send(file=discord.File(
                        filename='result.py',
                        fp=BytesIO(result_str.encode('utf-8'))
                    ))
                await msg_bot.add_reaction(emojis['desativado'])
                await msg_bot.add_reaction(emojis['cadeado'])
                try:
                    reaction, _ = await self.bot.wait_for('reaction_add', timeout=120.0, check=check)
                    if str(reaction.emoji) == str(emojis['desativado']):
                        await msg_bot.edit(embed=closed, allowed_mentions=discord.AllowedMentions(replied_user=False))
                        if send_file and msg_file is not None:
                            await msg_file.delete()
                    elif str(reaction.emoji) == str(emojis['cadeado']):
                        e.remove_field(-1)
                        await msg_bot.edit(embed=e, allowed_mentions=discord.AllowedMentions(replied_user=False))
                except asyncio.TimeoutError:
                    await msg_bot.edit(embed=closed, allowed_mentions=discord.AllowedMentions(replied_user=False))
                    if send_file and msg_file is not None:
                        await msg_file.delete()
                await msg_bot.remove_reaction(emojis['desativado'], ctx.me)
                await msg_bot.remove_reaction(emojis['cadeado'], ctx.me)
            else:
                await ctx.message.add_reaction(emojis['ativado'])

    @owner_gp.command(name='blacklist', aliases=['blacklisted', 'banido'])
    @commands.check(permissions.is_owner)
    async def _blacklist(self, ctx, *args):
        if ctx.prefix.replace('!', '').replace(' ', '') == self.bot.user.mention:
            # se a pessoa marcou o bot apenas 1 vez
            if ctx.message.content.replace('!', '').count(self.bot.user.mention) == 1:
                # vai tirar a menção da mensagem
                ctx.message.mentions.pop(0)
        if ctx.message.mentions:
            user_id = ctx.message.mentions[-1].id
        else:
            user_id = int(args[0])
        blacklisted = await BlacklistRepository().get_pessoa(self.bot.db_connection, user_id)
        if not blacklisted[0]:
            msg = f'O usuário <@!{user_id}> pode usar meus comandos! {get_emoji_dance()}'
        else:
            msg = f'{self.bot.get_emoji("no_no")} O usuário <@!{user_id}> foi banido de me usar!' + \
                  f'\nMotivo: `{blacklisted[1]}`\nQuando: `{datetime_format(blacklisted[-1], lang="pt_br")}`'
        return await ctx.reply(msg, mention_author=False)

    @owner_gp.command(name='add_blacklist', aliases=['ab'])
    @commands.check(permissions.is_owner)
    async def _add_blacklist(self, ctx, *args):
        if ctx.prefix.replace('!', '').replace(' ', '') == self.bot.user.mention:
            # se a pessoa marcou o bot apenas 1 vez
            if ctx.message.content.replace('!', '').count(self.bot.user.mention) == 1:
                # vai tirar a menção da mensagem
                ctx.message.mentions.pop(0)
        if ctx.message.mentions:
            user_id = ctx.message.mentions[-1].id
            args = ctx.message.content.split(' ')
            args.pop(0)
        else:
            user_id = int(args[0])
            args = list(args)
        args.pop(0)
        arg = args
        if args:
            motivo = ' '.join(arg)
        else:
            motivo = 'nulo'
        await BlacklistRepository().create(self.bot.db_connection, user_id, motivo)
        return await ctx.reply(
            f'O usuário <@!{user_id}> não vai poder usar meus comandos! {self.bot.get_emoji("banido")}'
            f'\nCom o motivo: {motivo}', mention_author=False)

    @owner_gp.command(name='remove_blacklist', aliases=['rb', 'whitelist'])
    @commands.check(permissions.is_owner)
    async def _remove_blacklist(self, ctx, *args):
        if ctx.prefix.replace('!', '').replace(' ', '') == self.bot.user.mention:
            # se a pessoa marcou o bot apenas 1 vez
            if ctx.message.content.replace('!', '').count(self.bot.user.mention) == 1:
                # vai tirar a menção da mensagem
                ctx.message.mentions.pop(0)
        if ctx.message.mentions:
            user_id = ctx.message.mentions[-1].id
        else:
            user_id = int(args[0])
        await BlacklistRepository().delete(self.bot.db_connection, user_id)
        return await ctx.reply(f'Usuário <@!{user_id}> perdoado! {get_emoji_dance()}', mention_author=False)

    @owner_gp.command(name='manutenção_on', aliases=['ativar_manutenção', 'man_on'])
    @commands.check(permissions.is_owner)
    async def _manutencao_on(self, ctx):
        if not self.bot.maintenance_mode:
            self.bot.maintenance_mode = True
            self.bot.mudar_status = False
            await self.bot.change_presence(activity=discord.Game(name='Em manutenção!'))
            self.bot.unload_extension('events.ErrorCommands')
        await ctx.reply(f'Modo manutenção:\n{self.bot.get_emoji("on")}', mention_author=False)

    @owner_gp.command(name='manutenção_off', aliases=['desativar_manutenção', 'man_off'])
    @commands.check(permissions.is_owner)
    async def _manutencao_off(self, ctx):
        if self.bot.maintenance_mode:
            self.bot.maintenance_mode = False
            self.bot.mudar_status = True
            self.bot.load_extension('events.ErrorCommands')
        await ctx.reply(f'Modo manutenção:\n{self.bot.get_emoji("off")}', mention_author=False)

    @owner_gp.command(name='jsk_docs', aliases=['docs_jsk', 'help_jsk', 'jsk_help', 'jh', 'jd'])
    @commands.check(permissions.is_owner)
    async def _jsk_docs(self, ctx):
        await ctx.reply('Docs do jsk:\nhttps://jishaku.readthedocs.io/en/latest/cog.html#commands',
                        mention_author=False)


def setup(bot):
    bot.add_cog(OwnerOnly(bot))
