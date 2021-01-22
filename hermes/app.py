from time import time
from pprint import pprint

import uvicorn

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from .logs import get_logger
from .resources import messages_router


logger = get_logger(__name__)


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

app.include_router(messages_router)


@app.middleware("http")
async def log_request_and_response_and_timeit(request: Request, call_next):
    logger.info("Request -> %s", pprint(request.__dict__))
    start_time = time()

    response = await call_next(request)

    process_time = time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    logger.info("Response -> %s", pprint(response.__dict__))
    logger.info("Executed in %s", process_time)

    return response


@app.get("/healthcheck")
async def healthcheck():
    return {"health": True}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
