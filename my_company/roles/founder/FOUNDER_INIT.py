import os
import yaml
import subprocess

BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INPUT_PATH = os.path.join(BASE_PATH, "inputs", "FOUNDER_EXPANSION_CONFIRMATION.yaml")

def prompt():
    print("\nFOUNDER INITIALIZATION\n")

    mission = input("Company mission: ")
    strategy = input("Company strategy: ")
    functions = input("Required functions (comma separated): ")

    data = {
        "company_mission": mission,
        "company_strategy": strategy,
        "required_functions": [f.strip() for f in functions.split(",") if f.strip()],
        "confirmed_by_founder": True
    }

    return data

def write_yaml(data):
    os.makedirs(os.path.dirname(INPUT_PATH), exist_ok=True)
    with open(INPUT_PATH, "w") as f:
        yaml.dump(data, f)

def expand():
    print("\nRunning expansion...\n")
    subprocess.run(["vc", "expand", BASE_PATH, "--from-founder-init"])

def main():
    data = prompt()
    write_yaml(data)
    expand()

if __name__ == "__main__":
    main()
