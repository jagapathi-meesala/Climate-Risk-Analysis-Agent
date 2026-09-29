import os
import sys

def audit():
    print("Starting Readiness Audit...")
    project_root = os.path.join(os.path.dirname(__file__), "..")
    
    required_files = [
        "agent.yaml", "README.md", "SOUL.md", "RULES.md",
        "DUTIES.md", "AGENTS.md", "EXPLAINABILITY.md",
        ".env.example", ".gitignore", "requirements.txt",
        "pytest.ini"
    ]
    
    missing = []
    for f in required_files:
        if not os.path.exists(os.path.join(project_root, f)):
            missing.append(f)
            
    if missing:
        print(f"FAILED: Missing required files: {missing}")
        return False
        
    required_tools = [
        "analyze-climate-exposure.py",
        "analyze-temperature-risk.py",
        "analyze-precipitation-risk.py",
        "calculate-drought-risk.py",
        "calculate-flood-risk.py",
        "calculate-climate-vulnerability.py",
        "calculate-climate-priority.py"
    ]
    
    missing_tools = []
    for t in required_tools:
        if not os.path.exists(os.path.join(project_root, "tools", t)):
            missing_tools.append(t)
            
    if missing_tools:
        print(f"FAILED: Missing required tools: {missing_tools}")
        return False
        
    print("PASSED: All required files and tools are present.")
    return True

if __name__ == "__main__":
    success = audit()
    sys.exit(0 if success else 1)
