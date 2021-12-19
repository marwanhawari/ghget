import requests
from pathlib import Path
from ghget.gh import GH
import os

gh = GH(
    "https://github.com/marwanhawari/pyinterview/tree/main/docs/algorithms",
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


for path in all_paths:
    tree_path = Path(path["path"])
    if tree_path.is_relative_to(gh.file_path):
        if is_root:
            print(str(tree_path), path["type"])
        else:
            partition_path = Path(str(tree_path).partition(f"{prefix_path}/")[-1])
            if path["type"] == "tree":
                # print(partition_path)
                partition_path.mkdir(exist_ok=True, parents=True)
            else:
                raw_file_url = generate_raw_url(
                    gh.owner, gh.repo, gh.branch, path["path"]
                )
                # print(partition_path)
                download_file(raw_file_url, partition_path)


def download_dir(
    http_response: requests.models.Response, file_path: str, headers: dict
) -> None:
    response_content = http_response.json()

    Path(file_path).mkdir(exist_ok=True, parents=True)

    for obj in response_content:

        current_path = f'{file_path}/{obj["name"]}'

        if obj["type"] == "file":
            download_file(obj["download_url"], current_path)

        elif obj["type"] == "dir":
            response = requests.get(obj["url"], headers=headers)
            download_dir(response, current_path, headers)
