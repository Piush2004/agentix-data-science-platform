import re

with open('app/services/platform_services.py', 'r') as f:
    content = f.read()

if 'current_user_id' not in content:
    content = content.replace('from app.services.data_service import data_service', 'from app.services.data_service import data_service\nfrom app.core.context import current_user_id')

content = content.replace('data_service.memory_store.keys()', 'data_service.memory_store.get(current_user_id.get(), {}).keys()')
content = content.replace('data_service.memory_store.items()', 'data_service.memory_store.get(current_user_id.get(), {}).items()')
content = content.replace('hasattr(data_service, "memory_store") and data_service.memory_store', 'data_service.memory_store.get(current_user_id.get(), {})')
content = content.replace('data_service.memory_store', 'data_service.memory_store.get(current_user_id.get(), {})')

content = content.replace('data_service.models[dataset_name] = ', 'if current_user_id.get() not in data_service.models: data_service.models[current_user_id.get()] = {}\n        data_service.models[current_user_id.get()][dataset_name] = ')
content = content.replace('data_service.models[dataset_name]', 'data_service.models.get(current_user_id.get(), {}).get(dataset_name, {})')
content = content.replace('data_service.models[active_dataset]', 'data_service.models.get(current_user_id.get(), {}).get(active_dataset, {})')
content = content.replace('data_service.models[ds_name]', 'data_service.models.get(current_user_id.get(), {}).get(ds_name, {})')
content = content.replace('dataset_name in data_service.models', 'dataset_name in data_service.models.get(current_user_id.get(), {})')
content = content.replace('active_dataset in data_service.models', 'active_dataset in data_service.models.get(current_user_id.get(), {})')
content = content.replace('hasattr(data_service, "models")', 'True')

with open('app/services/platform_services.py', 'w') as f:
    f.write(content)
