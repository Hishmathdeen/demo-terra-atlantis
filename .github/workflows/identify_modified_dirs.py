import json
import os
import subprocess

def get_modified_dirs(base_branch="main"):
    # Fetch the diff for the current PR against the base branch
    result = subprocess.run(
        ["git", "diff", "--name-only", f"origin/{base_branch}"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise Exception(f"Error running git diff: {result.stderr}")

    # Extract the directories in the 'config/' folder
    modified_files = result.stdout.strip().split("\n")
    modified_dirs = sorted(
        {"/".join(file.split("/")[:2]) for file in modified_files if file.startswith("config/")}
    )
    return modified_dirs

if __name__ == "__main__":
    try:
        modified_dirs = get_modified_dirs()
        print(f"Modified directories: {modified_dirs}")
        
        # Write the modified directories as a JSON array to an output file
        output_file = os.environ.get("GITHUB_WORKSPACE", ".") + "/modified_dirs.json"
        with open(output_file, "w") as f:
            json.dump(modified_dirs, f)

    except Exception as e:
        print(f"Error: {e}")
        exit(1)
