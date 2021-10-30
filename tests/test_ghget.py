import os
from ghget.gh import GH

file_url = "https://github.com/marwanhawari/pyinterview/blob/main/docs/index.md"
file_gh = GH(file_url)

dir_url = "https://github.com/marwanhawari/pyinterview/tree/main/tests"
dir_gh = GH(dir_url, os.environ.get("GITHUB_TOKEN"))

recursive_dir_url = "https://github.com/marwanhawari/pyinterview/tree/main/docs/"
recursive_dir_gh = GH(recursive_dir_url, os.environ.get("GITHUB_TOKEN"))


def test_download_file():
    assert len(file_gh.headers) == 1
    assert file_gh.response_content["name"] == "index.md"
    assert file_gh.type == "file"


def test_download_dir():
    assert len(dir_gh.headers) == 2
    assert len(dir_gh.response_content) == 8
    assert dir_gh.type == "dir"


def test_download_recursive_dir():
    assert len(recursive_dir_gh.headers) == 2
    assert len(recursive_dir_gh.response_content) == 7
    assert recursive_dir_gh.type == "dir"
