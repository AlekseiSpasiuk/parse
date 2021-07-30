import requests

github_username = "AlekseiSpasiuk"
url = f"https://api.github.com/users/{github_username}/repos"
response = requests.get(url)
out_repos = [rep["name"] for rep in response.json()]
print(out_repos)
with open(f"{github_username}.json", "w") as out_file:
    out_file.write(str(response.json()))
