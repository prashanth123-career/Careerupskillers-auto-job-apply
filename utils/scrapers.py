
import requests
from bs4 import BeautifulSoup

def scrape_internshala(keyword):
    url = f"https://internshala.com/internships/keywords-{keyword.replace(' ', '%20')}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    jobs = []
    for card in soup.find_all("div", class_="individual_internship")[:10]:
        title = card.find("a", class_="view_detail_button")
        link = "https://internshala.com" + title["href"] if title else ""
        role = card.find("div", class_="heading_4_5 profile")
        company = card.find("a", class_="link_display_like_text")
        jobs.append({
            "Title": role.text.strip() if role else "",
            "Company": company.text.strip() if company else "",
            "Link": link,
            "Platform": "Internshala"
        })
    return jobs

def scrape_naukri(keyword, location):
    return []

def scrape_indeed(keyword, location):
    return []

def scrape_timesjobs(keyword, location):
    return []
