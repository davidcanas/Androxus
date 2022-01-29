# MIT License

# Copyright(c) 2021-2022 Rafael

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

from typing import (
    Any,
    Optional
)

from sqlalchemy import String  # type: ignore
from sqlalchemy import (
    BigInteger,
    Column
)
from sqlalchemy.ext.asyncio.engine import AsyncEngine  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore

from configs import Configs

from .model import Model


Base = declarative_base()  # type: ignore


class Guild(Model, Base):  # type: ignore
    """
    Represents a guild in the database.

    Args:
        id (int): The guild id
        prefix (str, optional): The guild prefix.
        language (str, optional): The guild language.

    Attributes:
        id (int): The guild's ID.
        prefix (str): The guild's prefix.
        language (str): The guild's language.

    """
    __tablename__ = 'guilds'
    id = Column(
        BigInteger, primary_key=True, autoincrement=False, nullable=False
    )  # type: ignore
    prefix = Column(String(10), nullable=False)
    language = Column(String(255), nullable=False)

    def __init__(
        self,
        id_: int,
        prefix: Optional[str] = None,
        language: Optional[str] = None
    ) -> None:
        super().__init__(id_)
        self.prefix = prefix or Configs.default_prefix
        self.language = language or Configs.default_language

    @staticmethod
    async def create_table(engine: AsyncEngine):
        """
        Creates the "guilds" table.

        Args:
            engine (sqlalchemy.ext.asyncio.engine.AsyncEngine): The database engine.

        """
        async with engine.begin() as conn:  # type: ignore
            await conn.run_sync(Base.metadata.create_all)  # type: ignore

    @staticmethod
    async def drop_table(engine: AsyncEngine):
        """
        Drops the "guilds" table.

        Args:
            engine (sqlalchemy.ext.asyncio.engine.AsyncEngine): The database engine.

        """
        async with engine.begin() as conn:  # type: ignore
            await conn.run_sync(Base.metadata.drop_all)  # type: ignore

    def to_dict(self) -> dict[str, Any]:
        """
        Returns a dictionary representation of the guild.

        Returns:
            dict[str, Any]: The guild's dictionary representation.

        """
        return {'id': self.id, 'prefix': self.prefix, 'language': self.language}
