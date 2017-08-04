import requests
from bs4 import BeautifulSoup
import csv

issue_url = "https://www.ets.org/gre/revised_general/prepare/analytical_writing/issue/pool"

def scrape(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    peas = soup.find(class_="contents left").find_all(["p", "div"], recursive=False)
    prompts = []
    prompt = {"prompt":"", "instructions":""}
    for pea in peas:
        if pea.get("class") == ["divider-50"]:
            prompts.append(prompt)
            prompt = {"prompt":"", "instructions":""}

        elif pea.get("class") == ["indented"]:
            prompt["instructions"] += pea.get_text()

        else:
            prompt["prompt"] += pea.get_text()
    return prompts[1:]


def save(prompts, name):
    with open(name, "w") as out:
        writer = csv.DictWriter(out, ["prompt", "instructions"])
        writer.writeheader()
        writer.writerows(prompts)

save(scrape(issue_url), "issues.csv")
