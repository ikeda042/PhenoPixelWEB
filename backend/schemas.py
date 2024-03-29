from pydantic import BaseModel



class DBInfo(BaseModel):
    file_name: str
    cell_count: int
