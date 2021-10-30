import requests
from typing import Optional, Union


class GH:
    def __init__(self, url: str, token: str = "") -> None:
        self.url = url
        self.token = token

        self.trimmed_url = self.trim_url(self.url)
        self.components = self.trimmed_url.split("/")
        self.owner = self.components[1]
        self.repo = self.components[2]

        (
            self.branch,
            self.file_path,
            self.file_name,
            self.api_url,
        ) = self.generate_api_url(self.components, self.owner, self.repo)

        self.headers = self.get_headers(self.token)

        self.response = self.get_http_reponse(self.api_url, self.headers)
        self.response_content = self.response.json()
        self.type = self.get_type(self.response_content)

    def trim_url(self, url: str) -> str:
        return url.lstrip("https://").rstrip("/")

    def get_headers(self, token: str) -> dict:
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

    def get_type(self, response_content: Union[dict, list]) -> Optional[str]:
        if type(response_content) == dict:
            return "file"
        elif type(response_content) == list:
            return "dir"

    def generate_api_url(self, components: list, owner: str, repo: str) -> tuple:
        # Repo homepage, default branch
        if len(components) == 3:
            branch = None
            file_path = None
            file_name = repo
            api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/"
        # Repo homepage, on a tag or non-default branch
        elif len(components) == 5:
            branch = components[4]
            file_path = None
            file_name = repo
            api_url = (
                f"https://api.github.com/repos/{owner}/{repo}/contents/?ref={branch}"
            )
        # File or folder within the repo
        elif len(components) > 5:
            branch = components[4]
            file_path = "/".join(components[5:])
            file_name = components[-1]
            api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}?ref={branch}"

        return branch, file_path, file_name, api_url
