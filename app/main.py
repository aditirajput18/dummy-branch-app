from fastapi import FastAPI, Request
from prometheus_fastapi_instrumentator import Instrumentator
from app.logger import logger
from app.health import check_db
import uuid


app = FastAPI(title="Loan API")


# Instrumentation: expose /metrics
@app.on_event("startup")
async def startup():
Instrumentator().instrument(app).expose(app, include_in_schema=False)
logger.info("instrumentation_started")


# Middleware: structured logging + request id
@app.middleware("http")
async def add_request_id_and_log(request: Request, call_next):
request_id = str(uuid.uuid4())
# Attach request_id to logger via extra on each log call
logger.info("request_started", extra={"request_id": request_id, "path": request.url.path, "method": request.method})
response = await call_next(request)
logger.info("request_completed", extra={"request_id": request_id, "status_code": response.status_code})
response.headers["X-Request-ID"] = request_id
return response


# Health endpoint uses check_db() which performs a DB ping
@app.get("/health")
async def health():
ok, details = await check_db()
status = "healthy" if ok else "unhealthy"
return {"status": status, **details}


# Example root endpoint
@app.get("/")
async def root():
return {"message": "Loan API running"}
