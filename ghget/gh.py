import requests


class GH:
    def __init__(self, url: str, token: str = "") -> None:
        self.url = url
        self.token = token
        self.headers = self.generate_headers(self.token)

        self.trimmed_url = self.trim_url(self.url)
        self.components = self.trimmed_url.split("/")
        self.owner = self.components[1]
        self.repo = self.components[2]
        self.branches_and_tags = self.get_branches_and_tags(self.owner, self.repo)
        print(self.branches_and_tags)

        (
            self.branch,
            self.file_path,
            self.file_name,
            self.api_url,
        ) = self.generate_api_url(self.components, self.owner, self.repo)

        self.response = self.get_http_reponse(self.api_url, self.headers)
        self.response_content = self.response.json()

    def trim_url(self, url: str) -> str:
        return url.partition("https://")[-1].rstrip("/")

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

    def get_branches_and_tags(self, owner, repo) -> list:
        branches_api_url = f"https://api.github.com/repos/{owner}/{repo}/branches"
        branches_objects = self.get_http_reponse(branches_api_url, self.headers).json()
        branches = [obj["name"] for obj in branches_objects]

        tags_api_url = f"https://api.github.com/repos/{owner}/{repo}/tags"
        tags_objects = self.get_http_reponse(tags_api_url, self.headers).json()
        tags = [obj["name"] for obj in tags_objects]

        return branches + tags

    def generate_api_url(self, components: list, owner: str, repo: str) -> tuple:
        # Repo homepage, default branch
        if len(components) == 3:
            repo_api_url = f"https://api.github.com/repos/{owner}/{repo}"
            branch = self.get_http_reponse(repo_api_url, self.headers).json()[
                "default_branch"
            ]
            file_path = ""
            file_name = repo
        # Repo homepage, on a tag or non-default branch
        elif len(components) == 5:
            branch = components[4]
            file_path = ""
            file_name = repo
        # File or folder within the repo
        elif len(components) > 5:
            branch = components[4]
            file_path = "/".join(components[5:])
            file_name = components[-1]

        api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=true"

        return branch, file_path, file_name, api_url
