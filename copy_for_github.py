import os
import shutil
import fnmatch

source_dir = r"D:\Projects\Agentic Data Intelligence Platform"
dest_dir = r"D:\Projects\Agentix-AI-Public"

# Patterns to ignore
exclude_dirs = {
    '.git', 'node_modules', '.next', '__pycache__', 'venv', '.venv', 'env', 
    '.pytest_cache', 'build', 'dist', '.idea', '.vscode'
}

exclude_files = {
    '.env', '.env.local', '.env.production', 'agentix.db', '*.db', '*.csv', 
    '*.log', '*_logs.json', '.DS_Store'
}

def should_exclude(name, is_dir):
    if is_dir and name in exclude_dirs:
        return True
    
    for pattern in exclude_files:
        if fnmatch.fnmatch(name, pattern):
            return True
            
    return False

if os.path.exists(dest_dir):
    shutil.rmtree(dest_dir)

os.makedirs(dest_dir)

for root, dirs, files in os.walk(source_dir):
    # Filter directories in-place
    dirs[:] = [d for d in dirs if not should_exclude(d, True)]
    
    for file in files:
        if not should_exclude(file, False):
            src_file = os.path.join(root, file)
            rel_path = os.path.relpath(src_file, source_dir)
            dest_file = os.path.join(dest_dir, rel_path)
            
            os.makedirs(os.path.dirname(dest_file), exist_ok=True)
            shutil.copy2(src_file, dest_file)

print(f"Successfully copied clean repository to {dest_dir}")
