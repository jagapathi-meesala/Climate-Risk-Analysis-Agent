import os

def test_documentation_files_exist():
    docs = ["README.md", "SOUL.md", "RULES.md", "DUTIES.md", "AGENTS.md", "EXPLAINABILITY.md"]
    project_root = os.path.join(os.path.dirname(__file__), "..")
    for doc in docs:
        assert os.path.exists(os.path.join(project_root, doc)), f"Missing {doc}"

def test_agent_yaml_exists():
    assert os.path.exists(os.path.join(os.path.dirname(__file__), "..", "agent.yaml")), "Missing agent.yaml"
