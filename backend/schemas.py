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
