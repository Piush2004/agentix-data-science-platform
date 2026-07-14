from sqlalchemy.orm import Session
from core.models.models import Dataset as DBDataset

class DatasetRepository:
    def get_by_owner(self, db: Session, user_id: str):
        return db.query(DBDataset).filter(DBDataset.owner_id == user_id).order_by(DBDataset.created_at.desc()).all()
        
    def add(self, db: Session, dataset: DBDataset):
        db.add(dataset)
        db.commit()
        db.refresh(dataset)
        return dataset
        
    def delete(self, db: Session, dataset_name: str, user_id: str):
        dataset = db.query(DBDataset).filter(DBDataset.name == dataset_name, DBDataset.owner_id == user_id).first()
        if dataset:
            db.delete(dataset)
            db.commit()
            return True
        return False
        
dataset_repository = DatasetRepository()
