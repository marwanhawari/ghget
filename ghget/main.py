import sys
import argparse
from typing import Optional, Sequence
import requests
from pathlib import Path
from ghget.gh import GH


def download_file(raw_file_url: str, file_name: str) -> None:
    response = requests.get(raw_file_url)

    file_content = response.content

    with open(file_name, "wb") as f:
        f.write(file_content)


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


def main(argv: Optional[Sequence] = None) -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "url",
        action="store",
        type=str,
        help="The url for the file or directory you want to download.",
    )

    parser.add_argument(
        "-t",
        "--token",
        action="store",
        type=str,
        default="",
        help="Your GitHub token. This is needed for accessing private repos or overcoming the unauthenticated request rate limit for the GitHub API.",
    )

    args = parser.parse_args(argv)

    url = args.url
    github_token = args.token

    gh = GH(url, github_token)

    if gh.type == "file":
        raw_file_url = gh.response_content["download_url"]
        file_name = gh.file_name
        print(f"Downloading {file_name} file...")
        download_file(raw_file_url, file_name)

    elif gh.type == "dir":
        http_response = gh.response
        root_dir = gh.file_name
        headers = gh.headers
        print(f"Downloading {root_dir} directory...")
        download_dir(http_response, root_dir, headers)

    print("Done!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
