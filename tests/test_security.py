import pytest
import os
import ast

def test_no_eval_exec_in_codebase():
    """Verify that eval and exec are not used in the codebase."""
    project_root = os.path.join(os.path.dirname(__file__), "..")
    for root, _, files in os.walk(project_root):
        if "venv" in root or ".venv" in root:
            continue
        for file in files:
            if file.endswith(".py"):
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    content = f.read()
                    
                # Skip this file since we are testing for it
                if "test_security.py" in file:
                    continue
                    
                try:
                    tree = ast.parse(content)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Call):
                            if isinstance(node.func, ast.Name):
                                assert node.func.id not in ["eval", "exec"], f"Found {node.func.id} in {file}"
                except SyntaxError:
                    pass

def test_no_secrets_in_env_example():
    env_file = os.path.join(os.path.dirname(__file__), "..", ".env.example")
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            content = f.read()
            assert "PASSWORD=" not in content.upper() or "PASSWORD=placeholder" in content.lower()
            assert "API_KEY=" not in content.upper() or "API_KEY=placeholder" in content.lower()
