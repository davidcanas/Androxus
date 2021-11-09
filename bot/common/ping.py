# MIT License

# Copyright(c) 2021 Rafael

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files(the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and / or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import Union

from disnake import ApplicationCommandInteraction as Interaction
from disnake import Embed
from disnake.ext.commands.context import Context
from disnake.utils import utcnow
from language import Translator
from random import randint


async def ping(context: Union[Context, Interaction]):
    send = context.send if isinstance(
        context, Context) else context.response.send_message

    lang = await Translator(context).init()
    embed = Embed(
        title=lang.get('Translation test'),
        description=lang.get('Latency'),
        timestamp=utcnow()
    )

    minutes = randint(2, 50)
    await send(f'{lang.choice("minutes", 1, {"value": 1})}\n'
               f'{lang.choice("minutes", minutes, {"value": minutes})}\n')
