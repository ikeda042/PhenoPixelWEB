import asyncio
from sqlalchemy import Column, Integer, String, BLOB, FLOAT
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.future import select
from schemas import CellDB

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
    img_fluo2 = Column(BLOB,nullable=True) | None
    contour = Column(BLOB)
    center_x = Column(FLOAT)
    center_y = Column(FLOAT)



async def get_session(dbname:str):
    engine = create_async_engine(f'sqlite+aiosqlite:///{dbname}', echo=False)
    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        yield session


async def get_cells(dbname:str) -> list[CellDB]:
    async for session in get_session(dbname=dbname):
        result = await session.execute(select(Cell).where(Cell.manual_label =="1"))
        cells = result.scalars().all()
    await session.close()
    return [CellDB(cell_id=cell.cell_id, label_experiment=cell.label_experiment, manual_label=cell.manual_label, perimeter=cell.perimeter, area=cell.area) for cell in cells]

async def count_valid_cells(db_name:str) -> int:
    async for session in get_session(db_name):
        result = await session.execute(select(Cell).where(Cell.manual_label =="1"))
        cells = result.scalars().all()
        return len(cells)
