from fastapi import FastAPI, APIRouter
import uvicorn

app = FastAPI(docs_url="/cellAPI")
router_cell = APIRouter(prefix="/cellAPI")


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(router_cell)

if __name__ == "__main__":
    uvicorn.run("router:app", host="0.0.0.0", port=8000, reload=True)
