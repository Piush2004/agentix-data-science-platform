import pandas as pd
from typing import Dict, List, Any
import os
import json
import sys
from core.context import current_user_id

class DataService:
    def __init__(self):
        # Multi-tenant memory structures: keyed by user_id
        self.version_store = {}
        self.models = {}
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.abspath(os.path.join(base_dir, "../../data"))
        self.versions_dir = os.path.join(self.data_dir, "versions")
        
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.versions_dir, exist_ok=True)
        
    def _get_user_dir(self):
        user_id = current_user_id.get()
        path = os.path.join(self.data_dir, user_id)
        os.makedirs(path, exist_ok=True)
        return path

    def _get_user_version_dir(self):
        user_id = current_user_id.get()
        path = os.path.join(self.versions_dir, user_id)
        os.makedirs(path, exist_ok=True)
        return path

    def save_df_to_disk(self, file_path: str, df: pd.DataFrame):
        if file_path.endswith('.csv'):
            df.to_csv(file_path, index=False)
        elif file_path.endswith('.parquet'):
            df.to_parquet(file_path, index=False)
        elif file_path.endswith('.json'):
            df.to_json(file_path, orient='records')
        elif file_path.endswith(('.xlsx', '.xls')):
            df.to_excel(file_path, index=False)
        else:
            df.to_csv(file_path, index=False)
            
    def load_df_from_disk(self, file_path: str) -> pd.DataFrame:
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path)
        elif file_path.endswith('.parquet'):
            return pd.read_parquet(file_path)
        elif file_path.endswith('.json'):
            return pd.read_json(file_path)
        elif file_path.endswith(('.xlsx', '.xls')):
            return pd.read_excel(file_path)
        else:
            return pd.read_csv(file_path)
            
    def store_dataset(self, name: str, df: pd.DataFrame, change_summary: str = "Initial Upload"):
        user_id = current_user_id.get()
        
        size_bytes = int(sys.getsizeof(df))
        row_count = int(len(df))
        col_count = int(len(df.columns))
        
        if user_id not in self.version_store:
            self.version_store[user_id] = {}
        if name not in self.version_store[user_id]:
            self.version_store[user_id][name] = []
            
        next_version = len(self.version_store[user_id][name]) + 1
        
        version_entry = {
            "version": next_version,
            "df": df.copy(),
            "sizeBytes": size_bytes,
            "rowCount": row_count,
            "colCount": col_count,
            "changeSummary": change_summary,
            "timestamp": pd.Timestamp.now().isoformat()
        }
        self.version_store[user_id][name].append(version_entry)
        
        try:
            user_dir = self._get_user_dir()
            file_path = os.path.join(user_dir, name)
            self.save_df_to_disk(file_path, df)
            
            user_ver_dir = os.path.join(self._get_user_version_dir(), name)
            os.makedirs(user_ver_dir, exist_ok=True)
            _, ext = os.path.splitext(name)
            if not ext:
                ext = ".csv"
            ver_file_path = os.path.join(user_ver_dir, f"v{next_version}{ext}")
            self.save_df_to_disk(ver_file_path, df)
            
            self.save_versions_metadata_to_disk(name)
        except Exception as e:
            print(f"Failed to persist dataset {name} locally: {e}")
            
        try:
            from core.repositories.database import SessionLocal
            from core.models.models import Dataset as DBDataset
            db = SessionLocal()
            dataset = db.query(DBDataset).filter(DBDataset.name == name, DBDataset.owner_id == user_id).first()
            if dataset:
                dataset.rows = row_count
                dataset.columns = col_count
                dataset.size_bytes = size_bytes
                db.commit()
            db.close()
        except Exception as db_e:
            print(f"Failed to sync dataset {name} to DB on store: {db_e}")
            
    def save_versions_metadata_to_disk(self, name: str):
        user_id = current_user_id.get()
        versions = self.version_store.get(user_id, {}).get(name, [])
        meta_list = []
        for v in versions:
            meta_list.append({
                "version": v["version"],
                "sizeBytes": v["sizeBytes"],
                "rowCount": v["rowCount"],
                "colCount": v["colCount"],
                "changeSummary": v["changeSummary"],
                "timestamp": v["timestamp"]
            })
        ds_ver_dir = os.path.join(self._get_user_version_dir(), name)
        os.makedirs(ds_ver_dir, exist_ok=True)
        meta_path = os.path.join(ds_ver_dir, "versions.json")
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta_list, f, indent=2)
            
    def get_dataset(self, name: str) -> pd.DataFrame:
        user_id = current_user_id.get()
        file_path = os.path.join(self._get_user_dir(), name)
        if os.path.exists(file_path):
            try:
                df = self.load_df_from_disk(file_path)
                return df
            except Exception as e:
                print(f"Failed to load dataset {name} from disk on get: {e}")
        return None
        
    def get_versions(self, name: str) -> List[Dict[str, Any]]:
        user_id = current_user_id.get()
        versions = self.version_store.get(user_id, {}).get(name, [])
        return [
            {
                "version": v["version"],
                "sizeBytes": v["sizeBytes"],
                "rowCount": v["rowCount"],
                "colCount": v["colCount"],
                "changeSummary": v["changeSummary"],
                "timestamp": v["timestamp"]
            }
            for v in versions
        ]
        
    def rollback_dataset(self, name: str, version_num: int) -> bool:
        user_id = current_user_id.get()
        versions = self.version_store.get(user_id, {}).get(name, [])
        for v in versions:
            if v["version"] == version_num:
                df = v["df"].copy()
                try:
                    file_path = os.path.join(self._get_user_dir(), name)
                    self.save_df_to_disk(file_path, df)
                    
                    # Sync rollback to DB
                    from core.repositories.database import SessionLocal
                    from core.models.models import Dataset as DBDataset
                    import sys
                    db = SessionLocal()
                    dataset = db.query(DBDataset).filter(DBDataset.name == name, DBDataset.owner_id == user_id).first()
                    if dataset:
                        dataset.rows = int(len(df))
                        dataset.columns = int(len(df.columns))
                        dataset.size_bytes = int(sys.getsizeof(df))
                        db.commit()
                    db.close()
                    
                except Exception as e:
                    print(f"Failed to overwrite active dataset {name} on rollback: {e}")
                return True
        return False

data_service = DataService()
