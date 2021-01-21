import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Hermes Messaging API",
    description="Luiza Labs Code Challenge",
    docs_url=None,
    redoc_url="/",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthcheck")
async def healthcheck():
    return {"healthcheck": True}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
