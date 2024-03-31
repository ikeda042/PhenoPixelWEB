from pydantic import BaseModel


class CellDB(BaseModel):
    cell_id: str
    label_experiment: str
    manual_label: int
    perimeter: float
    area: float

class DBInfo(BaseModel):
    file_name: str
    cell_count: int

class CellDBAll(BaseModel):
    cell_id: str
    label_experiment: str
    manual_label: int
    perimeter: float
    area: float
    img_ph: bytes
    img_fluo1: bytes
    img_fluo2: bytes | None
    contour: bytes
    center_x: float
    center_y: float
