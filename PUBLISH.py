"""
cd ~/Developer/addon-ha-fusion
python3 PUBLISH.py
"""

import urllib.request
import json
import subprocess


def get_latest_release():
    url = "https://api.github.com/repos/matt8707/ha-fusion/releases/latest"
    with urllib.request.urlopen(urllib.request.Request(url)) as response:
        return json.loads(response.read().decode())


def update_config_yaml(version):
    file_path = "config.yaml"
    with open(file_path, "r") as file:
        lines = file.readlines()

    with open(file_path, "w") as file:
        for line in lines:
            if line.strip().startswith("version:"):
                file.write(f"version: {version}\n")
            else:
                file.write(line)


def update_changelog_md(release_notes):
    file_path = "CHANGELOG.md"
    with open(file_path, "w") as file:
        file.write(release_notes)


def git_commit(version):
    subprocess.run(["git", "add", "config.yaml", "CHANGELOG.md"], check=True)
    subprocess.run(["git", "commit", "-m", version], check=True)


try:
    # get ha-fusion release data
    data = get_latest_release()

    # update version in config.yaml
    version = data.get("tag_name")
    if not version:
        raise ValueError("missing version")
    update_config_yaml(version)
    print(f"INFO: config.yaml updated to {version}")

    # update release notes in CHANGELOG.md
    release_notes = data.get("body")
    if not release_notes:
        raise ValueError("missing release_notes")
    update_changelog_md(release_notes)
    print("INFO: CHANGELOG.md updated\n")
    print(release_notes)

    # git commit changes
    prompt = input("\nPROMPT: commit changes to git? (y/n): ").strip().lower()
    if prompt == "y":
        git_commit(version)
        print("INFO: changes committed to git")
    else:
        print("INFO: git commit skipped")

except Exception as error:
    print(f"An error occurred: {error}")
