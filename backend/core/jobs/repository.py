from core.database import SessionLocal
from core.jobs.models import JobRecord
from datetime import datetime

class JobRepository:
    def create_job(self, task_type: str, dataset_name: str = None, parameters: dict = None) -> JobRecord:
        from core.auth import current_user_id
        
        # Safely extract user context, defaulting to anonymous if outside a web request (e.g. system tasks)
        owner = None
        try:
            owner = current_user_id.get()
        except LookupError:
            pass
            
        with SessionLocal() as db:
            job = JobRecord(
                task_type=task_type,
                dataset_name=dataset_name,
                owner_id=owner,
                parameters=parameters
            )
            db.add(job)
            db.commit()
            db.refresh(job)
            # Create a detached copy to avoid DetachedInstanceError
            db.expunge(job)
            return job
            
    def update_job_status(self, job_id: str, status: str, result: dict = None, error: str = None):
        with SessionLocal() as db:
            job = db.query(JobRecord).filter(JobRecord.id == job_id).first()
            if job:
                job.status = status
                if result is not None:
                    job.result = result
                if error is not None:
                    job.error = error
                if status in ["COMPLETED", "FAILED"]:
                    job.completed_at = datetime.utcnow()
                db.commit()
                db.refresh(job)
                db.expunge(job)
                return job
            return None

    def update_job_progress(self, job_id: str, progress: int, message: str = None):
        with SessionLocal() as db:
            job = db.query(JobRecord).filter(JobRecord.id == job_id).first()
            if job:
                job.progress = progress
                if message is not None:
                    job.progress_message = message
                db.commit()
                db.refresh(job)
                db.expunge(job)
                return job
            return None

    def get_job(self, job_id: str) -> JobRecord:
        from core.auth import current_user_id
        owner = None
        try:
            owner = current_user_id.get()
        except LookupError:
            pass
            
        with SessionLocal() as db:
            query = db.query(JobRecord).filter(JobRecord.id == job_id)
            if owner is not None:
                query = query.filter(JobRecord.owner_id == owner)
                
            job = query.first()
            if job:
                db.expunge(job)
            return job
            
    def list_jobs(self, limit: int = 100) -> list[JobRecord]:
        with SessionLocal() as db:
            jobs = db.query(JobRecord).order_by(JobRecord.created_at.desc()).limit(limit).all()
            for job in jobs:
                db.expunge(job)
            return jobs
