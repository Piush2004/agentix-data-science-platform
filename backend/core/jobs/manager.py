from rq import Queue, Retry
from core.jobs.repository import JobRepository
from core.redis_client import get_redis
import logging
import traceback

logger = logging.getLogger(__name__)

# Global wrapper function for RQ to execute
def _execute_job_wrapper(job_id: str, func, *args, **kwargs):
    repo = JobRepository()
    try:
        repo.update_job_status(job_id, status="RUNNING")
        
        # Execute the long-running target function
        result = func(*args, **kwargs)
        
        repo.update_job_status(job_id, status="COMPLETED", result=result)
        logger.info(f"Job {job_id} completed successfully.")
        
    except Exception as e:
        error_trace = traceback.format_exc()
        logger.error(f"Job {job_id} failed: {e}")
        repo.update_job_status(job_id, status="FAILED", error=str(e))
        raise # Re-raise for RQ retry logic to catch

class JobManager:
    """
    Manages the asynchronous execution of background jobs via Redis Queue.
    """
    def __init__(self):
        self.repo = JobRepository()
        self.redis_conn = get_redis()
        # Create a single queue for now, RQ supports multiple easily
        self.queue = Queue('default', connection=self.redis_conn)

    def submit_job(self, task_type: str, func, dataset_name: str = None, parameters: dict = None, *args, **kwargs) -> str:
        """
        Submits a job to the Redis Queue and immediately returns the job_id.
        """
        # Create job record in DB
        job = self.repo.create_job(task_type, dataset_name, parameters)
        
        # Determine specific queue based on task type
        target_queue = Queue(task_type, connection=self.redis_conn)
        
        # Enqueue with RQ, enabling auto-retries for failed jobs
        target_queue.enqueue(
            _execute_job_wrapper, 
            args=(job.id, func) + args,
            kwargs=kwargs,
            job_timeout=3600,  # 1 hour timeout
            retry=Retry(max=3, interval=[10, 30, 60]) # Automatic retry backoff
        )
        
        return job.id

# Global singleton
job_manager = JobManager()
