import sys
import argparse
import requests
from typing import Optional, Sequence
from pathlib import Path
from ghget.gh import GH


def generate_raw_url(owner: str, repo: str, branch: str, file_path: str) -> str:
    raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{file_path}"
    return raw_url


def download_file(raw_file_url: str, file_path: Path) -> None:
    response = requests.get(raw_file_url)
    file_content = response.content
    with open(file_path, "wb") as f:
        f.write(file_content)


def download_contents(gh: GH, repo_object: dict, download_path: Path) -> None:
    if repo_object["type"] == "tree":
        if download_path.exists():
            raise SystemExit(f"The directory '{download_path}' already exists!")
        download_path.mkdir(parents=True)
    else:
        raw_file_url = generate_raw_url(
            gh.owner, gh.repo, gh.branch, repo_object["path"]
        )
        download_file(raw_file_url, download_path)


def get_download_paths(gh: GH) -> list[tuple[dict, Path]]:
    prefix_path = Path(gh.file_path).parent
    has_prefix_path = prefix_path != Path(".")
    all_repo_objects = gh.response_content["tree"]

    all_download_paths = []

    if not gh.file_path:
        root_repo = gh.file_name
        all_download_paths.append(
            ({"path": root_repo, "type": "tree"}, Path(root_repo))
        )
    else:
        root_repo = ""

    for repo_object in all_repo_objects:
        full_repo_path = root_repo / Path(repo_object["path"])
        if full_repo_path.is_relative_to(gh.file_path):
            if has_prefix_path:
                download_path = Path(
                    str(full_repo_path).partition(f"{prefix_path}/")[-1]
                )
            else:
                download_path = full_repo_path

            all_download_paths.append((repo_object, download_path))

    return all_download_paths


def main(argv: Optional[Sequence] = None) -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "url",
        action="store",
        type=str,
        help="The url for the file or directory you want to download.",
    )

    args = parser.parse_args(argv)

    url = args.url
    gh = GH(url)

    all_download_paths = get_download_paths(gh)
    if len(all_download_paths) == 0:
        raise SystemExit(f"Could not find any contents at {url}")

    for repo_object, download_path in all_download_paths:
        download_contents(gh, repo_object, download_path)

    print("Done!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
