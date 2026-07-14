from rq import get_current_job
from core.jobs.repository import JobRepository
import logging

logger = logging.getLogger(__name__)

def update_job_progress(progress: int, message: str = None):
    """
    Called from inside the executing ML workflows to update their progress (0-100%).
    If the code is executing inside RQ, it extracts the job context and updates PostgreSQL.
    """
    job = get_current_job()
    if job:
        try:
            repo = JobRepository()
            repo.update_job_progress(job.id, progress, message)
        except Exception as e:
            logger.error(f"Failed to update job progress for {job.id}: {e}")
    else:
        # Not running in RQ context (synchronous fallback)
        logger.debug(f"[Progress: {progress}%] {message}")
