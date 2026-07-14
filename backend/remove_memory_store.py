import re

with open('app/services/data_service.py', 'r') as f:
    content = f.read()

# Remove memory_store init
content = re.sub(r'\s*self\.memory_store = \{\}', '', content)

# Remove memory_store usage in store_dataset
content = re.sub(r'\s*if user_id not in self\.memory_store:\n\s*self\.memory_store\[user_id\] = \{\}\n\s*self\.memory_store\[user_id\]\[name\] = df', '', content)

# Fix get_dataset
def replacement_get_dataset(match):
    return '''    def get_dataset(self, name: str) -> pd.DataFrame:
        user_id = current_user_id.get()
        file_path = os.path.join(self._get_user_dir(), name)
        if os.path.exists(file_path):
            try:
                df = self.load_df_from_disk(file_path)
                return df
            except Exception as e:
                print(f"Failed to load dataset {name} from disk on get: {e}")
        return None'''

content = re.sub(r'    def get_dataset\(self, name: str\) -> pd\.DataFrame:.*?return None', replacement_get_dataset, content, flags=re.DOTALL)

# Fix rollback_dataset
def replacement_rollback(match):
    return '''    def rollback_dataset(self, name: str, version_num: int) -> bool:
        user_id = current_user_id.get()
        versions = self.version_store.get(user_id, {}).get(name, [])
        for v in versions:
            if v["version"] == version_num:
                df = v["df"].copy()
                try:
                    file_path = os.path.join(self._get_user_dir(), name)
                    self.save_df_to_disk(file_path, df)
                except Exception as e:
                    print(f"Failed to overwrite active dataset {name} on rollback: {e}")
                return True
        return False'''

content = re.sub(r'    def rollback_dataset\(self, name: str, version_num: int\) -> bool:.*?return False', replacement_rollback, content, flags=re.DOTALL)

with open('app/services/data_service.py', 'w') as f:
    f.write(content)
