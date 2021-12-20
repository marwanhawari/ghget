import os
import pytest
from ghget.gh import GH
from ghget.main import main


@pytest.mark.parametrize(
    "url",
    [
        ("https://github.com/marwanhawari/pyinterview/tree/main/docs/algorithms"),
        ("http://github.com/marwanhawari/pyinterview/tree/main/docs/algorithms"),
        ("github.com/marwanhawari/pyinterview/tree/main/docs/algorithms"),
    ],
)
def test_GH(url):
    gh = GH(url)
    assert len(gh.headers) == 2
    assert gh.owner == "marwanhawari"
    assert gh.repo == "pyinterview"
    assert gh.file_name == "algorithms"
    assert gh.file_path == "docs/algorithms"
    assert (
        gh.trimmed_url
        == "github.com/marwanhawari/pyinterview/tree/main/docs/algorithms"
    )
    assert len(gh.response_content["tree"]) == 58


@pytest.mark.parametrize(
    "url, root_download, contents_size",
    [
        ("https://github.com/marwanhawari/pyinterview", "pyinterview", 59),
        (
            "https://github.com/marwanhawari/pyinterview/tree/gh-pages",
            "pyinterview",
            73,
        ),
        (
            "https://github.com/marwanhawari/pyinterview/tree/gh-pages/search",
            "search",
            2,
        ),
        (
            "https://github.com/marwanhawari/pyinterview/tree/gh-pages/404.html",
            "404.html",
            1,
        ),
        (
            "https://github.com/marwanhawari/pyinterview/tree/main/README.md",
            "README.md",
            1,
        ),
        ("https://github.com/marwanhawari/pyinterview/tree/main/docs", "docs", 16),
        (
            "https://github.com/marwanhawari/pyinterview/tree/main/docs/index.md",
            "index.md",
            1,
        ),
        (
            "https://github.com/marwanhawari/pyinterview/tree/main/docs/algorithms",
            "algorithms",
            3,
        ),
        (
            "https://github.com/marwanhawari/pyinterview/tree/main/docs/algorithms/searching.md",
            "searching.md",
            1,
        ),
        (
            "https://github.com/numpy/numpy/blob/maintenance/1.0.3.x/COMPATIBILITY",
            "COMPATIBILITY",
            1,
        ),
        (
            "https://github.com/numpy/numpy/blob/maintenance/1.0.3.x/benchmarks",
            "benchmarks",
            6,
        ),
    ],
)
def test_root_repo(tmp_path, url, root_download, contents_size):
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()
    os.chdir(test_dir)

    returncode = main([url])
    assert returncode == 0

    test_dir_contents = set(test_dir.rglob("**/*"))
    assert len(test_dir_contents) == contents_size

    root_dir = test_dir / root_download
    assert root_dir in test_dir_contents
