import re

with open('app/services/platform_services.py', 'r') as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    if "data_service.models = {}" in line:
        continue
    if "if current_user_id.get() not in data_service.models" in line:
        continue
    
    # In predict, we replace the model storing with joblib dumping
    if "data_service.models[current_user_id.get()][dataset_name] =" in line:
        new_lines.append('''        import joblib
        import os
        model_dir = os.path.join(os.path.dirname(__file__), "../../data", current_user_id.get(), "models")
        os.makedirs(model_dir, exist_ok=True)
        model_path = os.path.join(model_dir, f"{dataset_name}.joblib")
        # Save model and necessary data
        joblib.dump({"model": best_model_obj, "features": list(X.columns)}, model_path)
        try:
            db = SessionLocal()
            from app.models.models import ModelRecord, Dataset
            ds = db.query(Dataset).filter(Dataset.name == dataset_name, Dataset.owner_id == current_user_id.get()).first()
            if ds:
                db_model = ModelRecord(
                    algorithm=best_model_name,
                    accuracy=str(best_r2),
                    dataset_id=ds.id,
                    owner_id=current_user_id.get(),
                    filepath=model_path
                )
                db.add(db_model)
                db.commit()
            db.close()
        except Exception as db_e:
            print(f'Failed to save model to DB: {db_e}')\n''')
        # Skip the original db saving code block if it was already added earlier
        continue

    # Clean up the old db saving block in predict if it exists
    if "db_model = ModelRecord(" in line and "data_service.models[current_user_id.get()][dataset_name]" not in line:
        # We handle this manually below
        pass
        
    # In xai
    if "if not True or dataset_name not in data_service.models:" in line:
        new_lines.append('''        import joblib
        import os
        model_path = os.path.join(os.path.dirname(__file__), "../../data", current_user_id.get(), "models", f"{dataset_name}.joblib")
        if not os.path.exists(model_path):
            return {"top_drivers": [], "bias_detected": False, "importances": {}, "waterfall": []}
''')
        continue
        
    if "model_info = data_service.models.get(current_user_id.get(), {}).get(dataset_name, {})" in line:
        new_lines.append('''        model_info = joblib.load(model_path)
        # Note: X_train, X_test, y_train are missing for XAI if not saved, so XAI might need to fetch Dataset and recreate or handle missing safely.
        X_train = None
        X_test = None
        y_train = None
''')
        continue

    # In chat
    if "if True and dataset_name in data_service.models.get(current_user_id.get(), {}):" in line:
        new_lines.append('''            import os, joblib
            model_path = os.path.join(os.path.dirname(__file__), "../../data", current_user_id.get(), "models", f"{dataset_name}.joblib")
            if os.path.exists(model_path):
''')
        continue
    if "pred_res = {\"model\": \"Random Forest\", \"features\": data_service.models.get(current_user_id.get(), {}).get(dataset_name, {})[\"features\"]}" in line:
        new_lines.append('''                model_info = joblib.load(model_path)
                pred_res = {"model": model_info["model"].__class__.__name__, "features": model_info["features"]}
''')
        continue
        
    # In dashboard_metrics
    if "if True and active_dataset in data_service.models.get(current_user_id.get(), {}):" in line:
        new_lines.append('''        import os, joblib
        model_path = os.path.join(os.path.dirname(__file__), "../../data", current_user_id.get(), "models", f"{active_dataset}.joblib")
        if os.path.exists(model_path):
''')
        continue
        
    if "model_info = data_service.models.get(current_user_id.get(), {}).get(active_dataset, {})" in line:
        new_lines.append('''            model_info = joblib.load(model_path)
''')
        continue

    # In mlops (trained_datasets)
    if "trained_datasets = list(getattr(data_service, \"models\", {}).keys())" in line:
        new_lines.append('''        try:
            db = SessionLocal()
            from app.models.models import ModelRecord
            models_count = db.query(ModelRecord).filter(ModelRecord.owner_id == current_user_id.get()).count()
            db.close()
        except:
            models_count = 0
        trained_datasets = [1] * models_count # mock list length for num_deployments
''')
        continue

    # In model_registry
    if "model_info = data_service.models.get(current_user_id.get(), {}).get(ds_name, {})" in line:
        new_lines.append('''            import os, joblib
            model_path = os.path.join(os.path.dirname(__file__), "../../data", current_user_id.get(), "models", f"{ds_name}.joblib")
            if os.path.exists(model_path):
                model_info = joblib.load(model_path)
            else:
                model_info = {"model": "Unknown", "best_r2": 0.0}
''')
        continue

    new_lines.append(line)

with open('app/services/platform_services.py', 'w') as f:
    f.writelines(new_lines)
