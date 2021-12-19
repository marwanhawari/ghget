import os
import sys
import requests
from pathlib import Path
from ghget.gh import GH

gh = GH(
    "https://github.com/marwanhawari/pyinterview/tree/main/docs/",
    os.getenv("GITHUB_TOKEN"),
)

all_paths = gh.response_content["tree"]
print(gh.file_path)
print(gh.file_name)
prefix_path = Path(gh.file_path).parent
is_root = prefix_path == Path(".")
print(prefix_path, is_root)
print("----------------")


def generate_raw_url(owner, repo, branch, file_path):
    raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{file_path}"
    return raw_url


def download_file(raw_file_url: str, file_name: str) -> None:
    response = requests.get(raw_file_url)
    file_content = response.content
    with open(file_name, "wb") as f:
        f.write(file_content)


def download_contents(path, gh, partition_path):
    if path["type"] == "tree":
        partition_path.mkdir(parents=True)
    else:
        raw_file_url = generate_raw_url(gh.owner, gh.repo, gh.branch, path["path"])
        download_file(raw_file_url, partition_path)


def main() -> int:
    for path in all_paths:
        tree_path = Path(path["path"])
        if tree_path.is_relative_to(gh.file_path):
            if is_root:
                partition_path = tree_path
                download_contents(path, gh, partition_path)
            else:
                partition_path = Path(str(tree_path).partition(f"{prefix_path}/")[-1])
                download_contents(path, gh, partition_path)

    return 0


if __name__ == "__main__":
    sys.exit(main())
