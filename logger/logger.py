import logging
import sys
from datetime import datetime
from pathlib import Path

# Create logs directory if it doesn't exist
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Configure logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create formatters
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Create handlers
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

# Create file handler with current date
current_date = datetime.now().strftime("%Y-%m-%d")
file_handler = logging.FileHandler(
    f"logs/stockmanager_{current_date}.log", encoding="utf-8"
)
file_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)


async def logging_middleware(request, call_next):
    """
    Middleware for logging incoming requests and their responses.

    Args:
        request: The incoming request
        call_next: The next middleware in the chain

    Returns:
        response: The response from the next middleware
    """
    start_time = datetime.now()

    # Log request details
    logger.info(
        f"Request: {request.method}: {request.url.path} "
        f"Client: {request.client.host}"
    )

    response = await call_next(request)

    # Calculate request processing time
    process_time = (datetime.now() - start_time).total_seconds()

    # Log response details
    logger.info(
        f"Request: {request.method}: {request.url.path} "
        f"Response: Status {response.status_code} "
        f"Process Time: {process_time:.3f}s"
    )

    return response


"""alternative logging middleware
async def log_middleware(request: Request, call_next):
    log_dict = {
        "url": request.url.path,
        "method": request.method,
    }
    logger.info(log_dict)

    response = await call_next(request)
    return response
"""
