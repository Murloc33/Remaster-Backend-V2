import os
import signal
import sys
import threading

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from general.routers import main_router

# app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
app = FastAPI()

# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(main_router)


def stdin_loop():
    print("[sidecar] Waiting for commands...", flush=True)
    while True:
        user_input = sys.stdin.readline().strip()

        if user_input == "sidecar shutdown":
            print("[sidecar] Received 'sidecar shutdown' command.", flush=True)
            os.kill(os.getpid(), signal.SIGINT)
        else:
            print(f"[sidecar] Invalid command [{user_input}]. Try again.", flush=True)


if __name__ == "__main__":
    input_thread = threading.Thread(target=stdin_loop, daemon=True)
    input_thread.start()

    uvicorn.run(app, port=1010, workers=1)
