import requests
from bs4 import BeautifulSoup

def scrape_internshala(keyword):
    url = f"https://internshala.com/internships/keywords-{keyword.replace(' ', '-')}/"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    jobs = []
    cards = soup.select(".internship_meta")
    for card in cards[:5]:
        title_tag = card.find_previous("a", class_="view_detail_button")
        company_tag = card.find_previous("div", class_="company_name")
        if title_tag and company_tag:
            jobs.append({
                "Title": title_tag.text.strip(),
                "Company": company_tag.text.strip(),
                "Platform": "Internshala",
                "Link": "https://internshala.com" + title_tag["href"]
            })
    return jobs

def scrape_indeed(keyword, location):
    url = f"https://www.indeed.com/jobs?q={keyword}&l={location}"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    jobs = []
    cards = soup.select("a.tapItem")
    for card in cards[:5]:
        title = card.find("h2").text.strip() if card.find("h2") else "No Title"
        company = card.find("span", class_="companyName").text.strip() if card.find("span", class_="companyName") else "Unknown"
        link = "https://www.indeed.com" + card["href"]
        jobs.append({
            "Title": title,
            "Company": company,
            "Platform": "Indeed",
            "Link": link
        })
    return jobs

def scrape_naukri(keyword, location):
    url = f"https://www.naukri.com/{keyword.replace(' ', '-')}-jobs-in-{location.replace(' ', '-')}"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    jobs = []
    cards = soup.select("article.jobTuple")
    for card in cards[:5]:
        title = card.find("a", class_="title").text.strip()
        company = card.find("a", class_="subTitle").text.strip()
        link = card.find("a", class_="title")["href"]
        jobs.append({
            "Title": title,
            "Company": company,
            "Platform": "Naukri",
            "Link": link
        })
    return jobs

def scrape_timesjobs(keyword, location):
    url = f"https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&txtKeywords={keyword}&txtLocation={location}"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    jobs = []
    cards = soup.select(".job-bx")
    for card in cards[:5]:
        title = card.find("h2").text.strip()
        company = card.find("h3", class_="joblist-comp-name").text.strip()
        link = card.find("a")["href"]
        jobs.append({
            "Title": title,
            "Company": company,
            "Platform": "TimesJobs",
            "Link": link
        })
    return jobs
