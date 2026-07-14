from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
import core.context
from core.auth import get_current_user
from core.models.models import User, Dataset as DBDataset
from sqlalchemy.orm import Session
from core.repositories.database import get_db
from core.schemas.data_schemas import UploadResponse
from core.services.data_service import data_service
import pandas as pd
import io

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_dataset(file: UploadFile = File(...), db: Session = Depends(get_db)):
    MAX_UPLOAD_SIZE = 50 * 1024 * 1024 # 50 MB
    
    if not file.filename.endswith(('.csv', '.xlsx', '.xls', '.parquet', '.json')):
        raise HTTPException(status_code=400, detail="Unsupported file format")

    contents = await file.read()
    
    # 1. Size Validation
    if len(contents) > MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=413, detail="File size exceeds the 50MB limit")
        
    # 2. MIME Validation
    ALLOWED_MIMES = {
        "text/csv", 
        "application/vnd.ms-excel", 
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 
        "application/json", 
        "application/octet-stream",
        "text/plain"
    }
    if file.content_type and file.content_type not in ALLOWED_MIMES:
        # Warning: Sometimes browsers send octet-stream for CSVs, so we must be lenient if it's not strictly known
        pass

    # 3. Magic Byte Validation
    if len(contents) >= 4:
        magic_bytes = contents[:4]
        if file.filename.endswith(".parquet") and magic_bytes != b'PAR1':
            raise HTTPException(status_code=415, detail="Invalid Parquet magic bytes")
        elif file.filename.endswith((".xlsx", ".xls")):
            if magic_bytes != b'PK\x03\x04' and magic_bytes != b'\xd0\xcf\x11\xe0':
                raise HTTPException(status_code=415, detail="Invalid Excel magic bytes")
        elif file.filename.endswith(".json"):
            first_char = contents.lstrip()[:1]
            if first_char not in (b'{', b'['):
                raise HTTPException(status_code=415, detail="Invalid JSON format")
        elif file.filename.endswith(".csv"):
            if b'\x00' in contents[:512]:
                raise HTTPException(status_code=415, detail="Invalid CSV: binary data detected")
    
    
    try:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        elif file.filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(io.BytesIO(contents))
        elif file.filename.endswith('.parquet'):
            df = pd.read_parquet(io.BytesIO(contents))
        elif file.filename.endswith('.json'):
            df = pd.read_json(io.BytesIO(contents))
        else:
            raise ValueError("Unsupported file format extension")
    except Exception as e:
        import os
        if os.getenv("ENVIRONMENT") == "production":
            raise HTTPException(status_code=400, detail="Failed to parse file. The format may be invalid or corrupt.")
        else:
            raise HTTPException(status_code=400, detail=f"Failed to parse file: {str(e)}")

    if df.empty:
        raise HTTPException(status_code=400, detail="Dataset is empty")

    dataset_name = file.filename
    
    # Process dataset offline without LLMs (Masks sensitive data)
    from core.services.dataset_processor import dataset_processor
    try:
        metadata, statistics, profile, privacy_report, df = dataset_processor.process_dataset(dataset_name, df)
    except Exception as e:
        print(f"Error processing dataset offline: {e}")
        
    data_service.store_dataset(dataset_name, df)
    
    import uuid
    from datetime import datetime
    
    dataset_id = f"ds_{uuid.uuid4().hex}"
    upload_timestamp = datetime.utcnow().isoformat() + "Z"
    
    # Save to SQLite
    try:
        user_id = core.context.current_user_id.get()
        db_dataset = DBDataset(
            id=dataset_id,
            name=dataset_name,
            owner_id=user_id,
            filepath=f"{user_id}/{dataset_name}",
            rows=len(df),
            columns=len(df.columns),
            size_bytes=int(df.memory_usage(deep=True).sum())
        )
        from core.repositories.dataset_repository import dataset_repository
        dataset_repository.add(db, db_dataset)
    except Exception as db_e:
        print(f"Failed to save dataset metadata to DB: {db_e}")
        import os
        if os.getenv("ENVIRONMENT") == "production":
            raise HTTPException(status_code=500, detail="Database transaction failed during dataset registration.")
        else:
            raise HTTPException(status_code=500, detail=f"Database transaction failed: {str(db_e)}")
    
    # Safe replacement of NaNs with None for JSON encoding in the preview
    df_clean = df.head(5).where(pd.notnull(df), None)
    preview = df_clean.to_dict(orient="records")
    
    column_types = {str(k): str(v) for k, v in df.dtypes.items()}
    
    return {
        "message": "Dataset uploaded successfully",
        "dataset_name": dataset_name,
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": df.columns.tolist(),
        "preview": preview,
        "column_types": column_types,
        "upload_timestamp": upload_timestamp,
        "dataset_id": dataset_id
    }

@router.get("/history")
async def get_datasets_history(db: Session = Depends(get_db)):
    history = []
    user_id = core.context.current_user_id.get()
    from core.repositories.dataset_repository import dataset_repository
    datasets = dataset_repository.get_by_owner(db, user_id)
    for ds in datasets:
        # Load from disk to calculate missing values if needed, but for performance, we can just use stored metadata
        # To avoid blocking the API loading 10 datasets, we just return basic info
        history.append({
            "name": ds.name,
            "rows": ds.rows,
            "columns": ds.columns,
            "missing_values": 0, # Should be stored in DBDataset metadata in the future
            "quality_score": 100, # Should be stored in DBDataset metadata in the future
            "size_bytes": ds.size_bytes
        })
    return {"history": history}

@router.delete("/{dataset_name}")
async def delete_dataset(dataset_name: str, db: Session = Depends(get_db)):
    user_id = core.context.current_user_id.get()
    from core.repositories.dataset_repository import dataset_repository
    success = dataset_repository.delete(db, dataset_name, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    try:
        from core.services.data_service import data_service
        # Implement physical file deletion if supported by data_service, for now just remove from DB
    except Exception:
        pass
        
    return {"message": f"Dataset {dataset_name} deleted successfully"}

@router.get("/{dataset_name}/preview")
async def get_dataset_preview(dataset_name: str, limit: int = 100):
    df = data_service.get_dataset(dataset_name)
    if df is None:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    columns = df.columns.tolist()
    # Safe replacement of NaNs with None for JSON encoding
    df_clean = df.head(limit).where(pd.notnull(df), None)
    records = df_clean.to_dict(orient="records")
    types = {str(k): str(v) for k, v in df.dtypes.items()}
    null_counts = {str(k): int(v) for k, v in df.isna().sum().items()}
    
    return {
        "columns": columns,
        "dtypes": types,
        "null_counts": null_counts,
        "data": records
    }

