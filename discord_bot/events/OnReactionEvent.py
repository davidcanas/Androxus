# coding=utf-8
# Androxus bot
# OnReactionEvent.py

__author__ = 'Rafael'

from discord.ext import commands

from discord_bot.database.Conexao import Conexao
from discord_bot.database.Repositories.BlacklistRepository import BlacklistRepository


class OnReactionEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if (not self.bot.is_ready()) or user.bot:
            return
        if user.id == self.bot.user.id:
            return
        conexao = Conexao()
        banido = BlacklistRepository().get_pessoa(conexao, user.id)
        if banido:
            return conexao.fechar()
        # bandeiras com suas respectivas línguas:
        languages = {
            '🇿🇦': 'af',
            '🇦🇱': 'sq',
            '🇪🇹': 'am',
            '🇸🇦': 'ar',
            '🇧🇭': 'ar',
            '🇶🇦': 'ar',
            '🇹🇩': 'ar',
            '🇰🇲': 'ar',
            '🇩🇯': 'ar',
            '🇰🇲': 'ar',
            '🇦🇪': 'ar',
            '🇪🇷': 'ar',
            '🇪🇬': 'ar',
            '🇾🇪': 'ar',
            '🇮🇶': 'ar',
            '🇯🇴': 'ar',
            '🇱🇾': 'ar',
            '🇱🇧': 'ar',
            '🇰🇼': 'ar',
            '🇲🇦': 'ar',
            '🇲🇷': 'ar',
            '🇴🇲': 'ar',
            '🇸🇾': 'ar',
            '🇸🇴': 'ar',
            '🇹🇳': 'ar',
            '🇸🇩': 'ar',
            '🇦🇲': 'hy',
            '🇦🇿': 'az',
            '🇪🇸': 'eu',
            '🇧🇾': 'be',
            '🇧🇩': 'bn',
            '🇧🇦': 'bs',
            '🇧🇬': 'bg',
            '🇦🇩': 'ca',
            '🇲🇼': 'ny',
            '🇨🇳': 'zh-cn',
            '🇨🇴': 'co',
            '🇭🇷': 'hr',
            '🇨🇿': 'cs',
            '🇩🇰': 'da',
            '🇳🇱': 'nl',
            '🇺🇸': 'en',
            '🇦🇬': 'en',
            '🇧🇸': 'en',
            '🇧🇧': 'en',
            '🇧🇿': 'en',
            '🇧🇼': 'en',
            '🇨🇦': 'en',
            '🇦🇺': 'en',
            '🇩🇲': 'en',
            '🇬🇭': 'en',
            '🇬🇲': 'en',
            '🇬🇩': 'en',
            '🇬🇾': 'en',
            '🇮🇳': 'en',
            '🇸🇧': 'en',
            '🇲🇭': 'en',
            '🇯🇲': 'en',
            '🇱🇷': 'en',
            '🇮🇪': 'en',
            '🇱🇸': 'en',
            '🇲🇼': 'en',
            '🇫🇲': 'en',
            '🇲🇺': 'en',
            '🇳🇦': 'en',
            '🇱🇨': 'en',
            '🇼🇸': 'en',
            '🇬🇧': 'en',
            '🇵🇬': 'en',
            '🇵🇼': 'en',
            '🇳🇿': 'en',
            '🇳🇬': 'en',
            '🇻🇨': 'en',
            '🇰🇳': 'en',
            '🇸🇱': 'en',
            '🇸🇿': 'en',
            '🇹🇻': 'en',
            '🇺🇬': 'en',
            '🇿🇲': 'en',
            '🇿🇼': 'en',
            '🇹🇴': 'en',
            '🇹🇹': 'en',
            '🇪🇪': 'et',
            '🇵🇭': 'tl',
            '🇫🇮': 'fi',
            '🇫🇷': 'fr',
            '🇬🇪': 'ka',
            '🇩🇪': 'de',
            '🇨🇾': 'el',
            '🇬🇷': 'el',
            '🇵🇰': 'gu',
            '🇭🇹': 'ht',
            '🇮🇱': 'he',
            '🇮🇳': 'hi',
            '🇭🇺': 'hu',
            '🇮🇪': 'is',
            '🇮🇩': 'id',
            '🇮🇪': 'ga',
            '🇮🇹': 'it',
            '🇯🇵': 'ja',
            '🇰🇿': 'kk',
            '🇰🇭': 'km',
            '🇰🇷': 'ko',
            '🇹🇷': 'ku',
            '🇰🇬': 'ky',
            '🇱🇦': 'lo',
            '🇻🇦': 'la',
            '🇱🇻': 'lv',
            '🇱🇹': 'lt',
            '🇱🇺': 'lb',
            '🇲🇰': 'mk',
            '🇲🇬': 'mg',
            '🇧🇳': 'ms',
            '🇲🇾': 'ml',
            '🇲🇹': 'mt',
            '🇲🇳': 'mn',
            '🇲🇲': 'my',
            '🇳🇵': 'ne',
            '🇳🇴': 'no',
            '🇦🇫': 'ps',
            '🇮🇷': 'fa',
            '🇵🇱': 'pl',
            '🇧🇷': 'pt',
            '🇦🇴': 'pt',
            '🇲🇿': 'pt',
            '🇵🇹': 'pt',
            '🇬🇼': 'pt',
            '🇹🇱': 'pt',
            '🇲🇴': 'pt',
            '🇨🇻': 'pt',
            '🇸🇹': 'pt',
            '🇲🇩': 'ro',
            '🇷🇴': 'ro',
            '🇧🇾': 'ru',
            '🇷🇺': 'ru',
            '🇼🇸': 'sm',
            '🇷🇸': 'sr',
            '🇱🇰': 'si',
            '🇸🇰': 'sk',
            '🇸🇮': 'sl',
            '🇸🇴': 'so',
            '🇺🇾': 'es',
            '🇧🇴': 'es',
            '🇨🇱': 'es',
            '🇦🇷': 'es',
            '🇨🇴': 'es',
            '🇨🇷': 'es',
            '🇨🇺': 'es',
            '🇸🇻': 'es',
            '🇪🇨': 'es',
            '🇪🇸': 'es',
            '🇬🇹': 'es',
            '🇭🇳': 'es',
            '🇬🇶': 'es',
            '🇳🇮': 'es',
            '🇩🇴': 'es',
            '🇵🇪': 'es',
            '🇵🇾': 'es',
            '🇵🇦': 'es',
            '🇻🇪': 'es',
            '🇹🇿': 'sw',
            '🇸🇪': 'sv',
            '🇹🇭': 'th',
            '🇹🇲': 'tr',
            '🇺🇦': 'uk',
            '🇻🇳': 'vi',
            '🇿🇦': 'xh'
        }
        id_msg = reaction.message.id
        if not (id_msg in self.bot.msg_traduzidas):
            for flag_lang in languages.items():
                if str(reaction) == flag_lang[0]:
                    # evita que a pessoa fique usando o comando na mesma mensagem
                    self.bot.msg_traduzidas.append(id_msg)
                    await self.bot.get_cog('Translator').traduzir(await self.bot.get_context(reaction.message),
                                                                  flag_lang[-1],
                                                                  reaction.message.content)
                    return


def setup(bot):
    bot.add_cog(OnReactionEvent(bot))
