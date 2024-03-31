import asyncio
from sqlalchemy import Column, Integer, String, BLOB, FLOAT
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.future import select
from schemas import CellDB, CellDBAll

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

async def get_cells_all(dbname:str) -> list[CellDBAll]:
    async for session in get_session(dbname=dbname):
        result = await session.execute(select(Cell))
        cells = result.scalars().all()
    await session.close()
    return [CellDBAll(cell_id=cell.cell_id, label_experiment=cell.label_experiment, manual_label=cell.manual_label, perimeter=round(cell.perimeter,2), area=cell.area, img_ph=cell.img_ph, img_fluo1=cell.img_fluo1, img_fluo2=cell.img_fluo2, contour=cell.contour, center_x=cell.center_x, center_y=cell.center_y) for cell in cells]

async def get_cells(dbname:str) -> list[CellDB]:
    async for session in get_session(dbname=dbname):
        result = await session.execute(select(Cell).where(Cell.manual_label =="1"))
        cells = result.scalars().all()
    await session.close()
    return [CellDB(cell_id=cell.cell_id, label_experiment=cell.label_experiment, manual_label=cell.manual_label, perimeter=round(cell.perimeter,2), area=cell.area) for cell in cells]

async def count_valid_cells(db_name:str) -> int:
    async for session in get_session(db_name):
        result = await session.execute(select(Cell).where(Cell.manual_label =="1"))
        cells = result.scalars().all()
    await session.close()
    return len(cells)

async def get_cell_ph(db_name:str, cell_id:str) -> bytes:
    async for session in get_session(db_name):
        result = await session.execute(select(Cell).where(Cell.cell_id == cell_id))
        cell = result.scalars().first()
    await session.close()
    return cell.img_ph


async def get_cell_fluo(db_name:str, cell_id:str) -> bytes:
    async for session in get_session(db_name):
        result = await session.execute(select(Cell).where(Cell.cell_id == cell_id))
        cell = result.scalars().first()
    await session.close()
    return cell.img_fluo1

async def get_cell_contour(db_name:str, cell_id:str) -> bytes:
    async for session in get_session(db_name):
        result = await session.execute(select(Cell).where(Cell.cell_id == cell_id))
        cell = result.scalars().first()
    await session.close()
    return cell.contour
