import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from routers import items, checkout

load_dotenv()
app = FastAPI()

app.include_router(items.router)
app.include_router(checkout.router)

@app.get("/healthcheck")
async def root():
    return {"message": "API is live!!"}

if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)