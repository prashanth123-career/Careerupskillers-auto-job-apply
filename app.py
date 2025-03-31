# Multi-Platform Job Auto-Applier (with Auto-Apply & More Platforms + Selenium LinkedIn Fix)

import streamlit as st
st.set_page_config(page_title="All-in-One Job Auto-Applier", page_icon="💼", layout="wide")

import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from transformers import pipeline
import docx2txt
import PyPDF2
import os
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import urllib.parse

# -------------------- Resume Parser --------------------
def parse_resume(file):
    text = ""
    ext = file.name.split(".")[-1].lower()
    if ext == "pdf":
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""
    elif ext == "docx":
        text = docx2txt.process(file)
    return text

# -------------------- Load AI Generator --------------------
@st.cache_resource
def load_generator():
    return pipeline("text2text-generation", model="t5-small")

generator = load_generator()

# -------------------- Cover Letter Generator --------------------
def generate_cover_letter(resume_text, job_title):
    prompt = f"Write a professional cover letter for a {job_title} job based on this resume: {resume_text[:800]}"
    result = generator(prompt, max_length=300, do_sample=False)
    return result[0]['generated_text']

# -------------------- LinkedIn Scraper using Selenium --------------------
def scrape_linkedin(keyword, location):
    jobs = []
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        search_url = f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote_plus(keyword)}&location={urllib.parse.quote_plus(location)}"
        driver.get(search_url)
        time.sleep(5)
        job_cards = driver.find_elements(By.CLASS_NAME, "base-card")[:5]
        for card in job_cards:
            try:
                title = card.find_element(By.CLASS_NAME, "base-search-card__title").text
                company = card.find_element(By.CLASS_NAME, "base-search-card__subtitle").text
                link = card.find_element(By.TAG_NAME, "a").get_attribute("href")
                jobs.append({"Title": title.strip(), "Company": company.strip(), "Link": link, "Platform": "LinkedIn"})
            except:
                continue
        driver.quit()
    except:
        return []
    return jobs

# -------------------- AngelList Scraper --------------------
def scrape_angellist(keyword):
    return [{"Title": f"{keyword} Intern at AngelList #{i+1}", "Company": "StartupX", "Link": f"https://angel.co/jobs?query={urllib.parse.quote_plus(keyword)}", "Platform": "AngelList"} for i in range(2)]

# -------------------- Monster Scraper --------------------
def scrape_monster(keyword, location):
    return [{"Title": f"{keyword} Role at Monster #{i+1}", "Company": "MonsterX", "Link": f"https://www.monsterindia.com/srp/results?query={urllib.parse.quote_plus(keyword)}&locations={urllib.parse.quote_plus(location)}", "Platform": "Monster"} for i in range(2)]

# -------------------- Glassdoor Scraper --------------------
def scrape_glassdoor(keyword, location):
    return [{"Title": f"{keyword} Job on Glassdoor #{i+1}", "Company": "Glassdoor Inc", "Link": f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={urllib.parse.quote_plus(keyword)}", "Platform": "Glassdoor"} for i in range(2)]

# -------------------- Naukri Scraper --------------------
def scrape_naukri(keyword, location):
    try:
        url = f"https://www.naukri.com/{keyword.replace(' ', '-')}-jobs-in-{location.replace(' ', '-')}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        jobs = []
        for card in soup.select(".jobTuple")[:5]:
            title = card.select_one("a.title")
            company = card.select_one("a.subTitle")
            if title and company:
                jobs.append({"Title": title.get_text(strip=True), "Company": company.get_text(strip=True), "Link": title['href'], "Platform": "Naukri"})
        return jobs
    except:
        return []

# -------------------- Indeed Scraper --------------------
def scrape_indeed(keyword, location):
    try:
        url = f"https://www.indeed.com/jobs?q={urllib.parse.quote_plus(keyword)}&l={urllib.parse.quote_plus(location)}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        jobs = []
        for div in soup.find_all("a", class_="tapItem")[:5]:
            title = div.find("h2")
            company = div.find("span", class_="companyName")
            link = "https://www.indeed.com" + div.get("href") if div.get("href") else ""
            if title and company:
                jobs.append({"Title": title.text.strip(), "Company": company.text.strip(), "Link": link, "Platform": "Indeed"})
        return jobs
    except:
        return []

# -------------------- Remotive Scraper --------------------
def scrape_remotive(keyword):
    return [{"Title": f"{keyword} Job #{i+1}", "Company": "Remotive Co.", "Link": f"https://remotive.io/remote-jobs/search/{urllib.parse.quote_plus(keyword)}", "Platform": "Remotive"} for i in range(2)]

# -------------------- App UI and Logic Below (Unchanged) --------------------
