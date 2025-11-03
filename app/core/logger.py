import logging

# For Docker: log to stdout/stderr (Docker captures these)
# No file handler needed - view logs with: docker logs <container>
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler()  # Console output only
    ]
)

logger = logging.getLogger("job_assistant")
