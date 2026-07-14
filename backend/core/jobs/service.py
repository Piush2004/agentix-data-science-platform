from core.jobs.repository import JobRepository
from core.jobs.manager import job_manager

class JobService:
    def __init__(self):
        self.repo = JobRepository()
        self.manager = job_manager

    def submit(self, task_type: str, func, dataset_name: str = None, parameters: dict = None, *args, **kwargs) -> str:
        """Submits a job to the manager."""
        return self.manager.submit_job(task_type, func, dataset_name, parameters, *args, **kwargs)

    def get_status(self, job_id: str) -> dict:
        """Retrieves job status and result if completed."""
        job = self.repo.get_job(job_id)
        if not job:
            return {"error": "Job not found"}
            
        return {
            "id": job.id,
            "task_type": job.task_type,
            "status": job.status,
            "progress": job.progress,
            "progress_message": job.progress_message,
            "dataset_name": job.dataset_name,
            "result": job.result,
            "error": job.error,
            "created_at": job.created_at.isoformat() if job.created_at else None,
            "completed_at": job.completed_at.isoformat() if job.completed_at else None
        }

job_service = JobService()
