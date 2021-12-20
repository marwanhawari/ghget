import os
import requests
from requests_html import HTMLSession


class GH:
    def __init__(self, url: str) -> None:
        self.url = url
        self.token = os.getenv("GITHUB_TOKEN")
        self.headers = self.generate_headers(self.token)

        self.trimmed_url = self.trim_url(self.url)
        self.components = self.trimmed_url.split("/")
        self.owner = self.components[1]
        self.repo = self.components[2]
        self.branch = self.get_branch(self.trimmed_url, self.owner, self.repo)

        (
            self.file_path,
            self.file_name,
            self.api_url,
        ) = self.generate_api_url(self.components, self.owner, self.repo, self.branch)

        self.response = self.get_http_reponse(self.api_url, self.headers)
        self.response_content = self.response.json()

    def trim_url(self, url: str) -> str:
        if url.startswith("https://"):
            url = url.partition("https://")[-1]
        elif url.startswith("http://"):
            url = url.partition("http://")[-1]

        return url.rstrip("/")

    def generate_headers(self, token: str) -> dict:
        headers = {"Accept": "application/vnd.github.v3+json"}
        if token:
            headers["Authorization"] = f"token {token}"
        return headers

    def get_http_reponse(self, url: str, headers: dict) -> requests.models.Response:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response
        elif response.status_code == 403:
            raise SystemExit("Error: GitHub API rate limit exceeded.")
        else:
            error_message = response.json()["message"]
            raise SystemExit(f"Error: {error_message}")

    def get_branch(self, url, owner, repo):
        session = HTMLSession()
        html_url = f"https://{url}"
        response = session.get(html_url)
        if response.status_code == 200:
            branch_components = (
                response.html.find("#code-tab", first=True).attrs["href"].split("/")
            )
            if len(branch_components) > 3:
                # If more than 3 components, then you're on a non-default branch
                branch = "/".join(branch_components[4:])
                return branch

        # Otherwise get the default branch
        repo_api_url = f"https://api.github.com/repos/{owner}/{repo}"
        branch = self.get_http_reponse(repo_api_url, self.headers).json()[
            "default_branch"
        ]

        return branch

    def generate_api_url(
        self, components: list, owner: str, repo: str, branch: str
    ) -> tuple:

        branch_len = len(branch.split("/"))

        # Repo homepage, default branch
        if len(components) == 3:
            file_path = ""
            file_name = repo
        # Repo homepage, on a tag or non-default branch
        elif len(components) == 4 + branch_len:
            file_path = ""
            file_name = repo
        # File or folder within the repo
        elif len(components) > 4 + branch_len:
            file_path = "/".join(components[4 + branch_len :])
            file_name = components[-1]

        api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=true"

        return file_path, file_name, api_url
