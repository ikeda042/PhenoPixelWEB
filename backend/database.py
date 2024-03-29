import asyncio
from sqlalchemy import Column, Integer, String, BLOB, FLOAT
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.future import select

Base = declarative_base()

class Cell(Base):
    __tablename__ = 'cells'
    id = Column(Integer, primary_key=True)
    cell_id = Column(String)
    label_experiment = Column(String)
    manual_label  = Column(Integer)
    perimeter = Column(FLOAT)
    area = Column(FLOAT)
    img_ph = Column(BLOB) 
    img_fluo1 = Column(BLOB)
    img_fluo2 = Column(BLOB) | None
    contour = Column(BLOB)
    center_x = Column(FLOAT)
    center_y = Column(FLOAT)


engine = create_async_engine(f'sqlite+aiosqlite:///sk326tri120min.db', echo=False)

async def get_session():
    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        yield session

# async def create_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

# async def main():

#     await create_tables()

#     async_session = sessionmaker(
#         engine, expire_on_commit=False, class_=AsyncSession
#     )

#     async with async_session() as session:
#         result = await session.execute(select(Cell))
#         cells = result.scalars().all()

#         for cell in cells:
#             print(cell.manual_label, cell.perimeter, cell.area, cell.center_x, cell.center_y)  



