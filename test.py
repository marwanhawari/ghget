import requests

r = requests.get(
    "https://api.github.com/repos/marwanhawari/pyinterview/git/trees/main?recursive=true"
)

# print(r.json()["tree"])

# print(len(r.json()["tree"]))

all_paths = r.json()["tree"]

for i, path in enumerate(all_paths):
    print(path)
