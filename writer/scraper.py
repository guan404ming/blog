from math import floor
from bs4 import BeautifulSoup
import requests
from typing import List, Dict

def scrape_repo() -> List[Dict[str, str]]:
    url = "https://github.com/trending?since=weekly"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    repositories = []
    repo_elements = soup.select("article")
    for repo_element in repo_elements:
        try: 
            link = repo_element.select_one("h2 > a")["href"]

            for element in ["article", "pre"]:
                readme_elements = BeautifulSoup(requests.get(f'https://github.com{link}').text, "html.parser").select(element)
                if len(readme_elements) > 0:
                    readme = readme_elements[0].text
                    break

            repository = {
                "title": link[1:],
                "link": link,
                "description": repo_element.select("p")[0].text.strip() if len(repo_element.select("p")) > 0 else "",
                "language": repo_element.select_one("span[itemprop='programmingLanguage']").text.strip(),
                "stars": repo_element.select_one(f'a[href="{link}/stargazers"]').text.strip(),
                "week_stars": int(repo_element.select("span.d-inline-block")[-1].text.strip().split(" ")[0].replace(",", "")),
                "readme": readme[:floor(len(readme) * 0.8)],
            }
            repositories.append(repository)

        except AttributeError:
            pass
            
    repositories.sort(key=lambda x: x["week_stars"], reverse=True)
    return repositories