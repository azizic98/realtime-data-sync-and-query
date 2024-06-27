from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import (consumer,routes,startup)

app = FastAPI()

# Include your API routes
app.include_router(routes.router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, startup.setup_index)
    loop.run_in_executor(None, consumer.start_consumers)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)