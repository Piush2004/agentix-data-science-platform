import os
import ast

def analyze_dependencies(root_dir):
    dependencies = {}
    for subdir, _, files in os.walk(root_dir):
        if 'venv' in subdir or '__pycache__' in subdir: continue
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(subdir, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        node = ast.parse(f.read(), filename=filepath)
                    imports = []
                    for n in ast.walk(node):
                        if isinstance(n, ast.Import):
                            for alias in n.names:
                                imports.append(alias.name)
                        elif isinstance(n, ast.ImportFrom):
                            if n.module:
                                imports.append(n.module)
                    # Use relative path as key
                    rel_path = os.path.relpath(filepath, root_dir)
                    dependencies[rel_path] = imports
                except Exception as e:
                    print(f"Error parsing {filepath}: {e}")
    return dependencies

if __name__ == "__main__":
    deps = analyze_dependencies("backend")
    with open("DEPENDENCY_ANALYSIS.md", "w") as f:
        f.write("# Dependency Analysis\n\n")
        f.write("## Module Imports\n")
        for module, imports in deps.items():
            f.write(f"- **{module}**\n")
            for imp in set(imports):
                f.write(f"  - `{imp}`\n")
