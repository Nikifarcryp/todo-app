from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from config import ASYNC_SQLALCHEMY_DATABASE_URL

# ------------------------------------------------------------- #
# from databases import Database                                #
#                                                               #
# DATABASE_URL = "postgresql://user:password@localhost/dbname"  #
#                                                               #
# database = Database(DATABASE_URL)                             #
# ------------------------------------------------------------- #

engine = create_async_engine(ASYNC_SQLALCHEMY_DATABASE_URL, echo=True)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
