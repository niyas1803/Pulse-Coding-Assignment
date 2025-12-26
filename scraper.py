
import requests
from bs4 import BeautifulSoup
import argparse
import json
from datetime import datetime

HEADERS = {"User-Agent": "Mozilla/5.0"}

def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d")

def valid_date(d, start, end):
    return start <= d <= end

def scrape_g2(company, start, end):
    reviews, page = [], 1
    while True:
        url = f"https://www.g2.com/products/{company}/reviews?page={page}"
        r = requests.get(url, headers=HEADERS)
        if r.status_code != 200:
            break
        soup = BeautifulSoup(r.text, "html.parser")
        cards = soup.find_all("div", class_="paper")
        if not cards:
            break
        for c in cards:
            try:
                title = c.find("h3").get_text(strip=True)
                review = c.find("div", itemprop="reviewBody").get_text(strip=True)
                date_str = c.find("time")["datetime"][:10]
                rating = c.find("span", itemprop="ratingValue").get_text(strip=True)
                d = parse_date(date_str)
                if valid_date(d, start, end):
                    reviews.append({
                        "source": "G2",
                        "title": title,
                        "review": review,
                        "date": date_str,
                        "rating": rating
                    })
            except:
                continue
        page += 1
    return reviews

def scrape_capterra(company, start, end):
    reviews, page = [], 1
    while True:
        url = f"https://www.capterra.com/p/{company}/reviews/?page={page}"
        r = requests.get(url, headers=HEADERS)
        if r.status_code != 200:
            break
        soup = BeautifulSoup(r.text, "html.parser")
        cards = soup.find_all("div", class_="review")
        if not cards:
            break
        for c in cards:
            try:
                title = c.find("h3").get_text(strip=True)
                review = c.find("p").get_text(strip=True)
                date_str = c.find("time")["datetime"][:10]
                rating = c.find("span", class_="star-rating").get_text(strip=True)
                d = parse_date(date_str)
                if valid_date(d, start, end):
                    reviews.append({
                        "source": "Capterra",
                        "title": title,
                        "review": review,
                        "date": date_str,
                        "rating": rating
                    })
            except:
                continue
        page += 1
    return reviews

def scrape_trustradius(company, start, end):
    reviews, page = [], 1
    while True:
        url = f"https://www.trustradius.com/products/{company}/reviews?page={page}"
        r = requests.get(url, headers=HEADERS)
        if r.status_code != 200:
            break
        soup = BeautifulSoup(r.text, "html.parser")
        cards = soup.find_all("div", class_="review")
        if not cards:
            break
        for c in cards:
            try:
                title = c.find("h3").get_text(strip=True)
                review = c.find("p").get_text(strip=True)
                date_str = c.find("time")["datetime"][:10]
                rating = c.find("span", class_="rating").get_text(strip=True)
                d = parse_date(date_str)
                if valid_date(d, start, end):
                    reviews.append({
                        "source": "TrustRadius",
                        "title": title,
                        "review": review,
                        "date": date_str,
                        "rating": rating
                    })
            except:
                continue
        page += 1
    return reviews

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--company", required=True)
    parser.add_argument("--start", required=True)
    parser.add_argument("--end", required=True)
    parser.add_argument("--source", required=True, choices=["g2", "capterra", "trustradius"])
    args = parser.parse_args()

    start = parse_date(args.start)
    end = parse_date(args.end)

    if args.source == "g2":
        data = scrape_g2(args.company, start, end)
    elif args.source == "capterra":
        data = scrape_capterra(args.company, start, end)
    else:
        data = scrape_trustradius(args.company, start, end)

    with open("sample_output.json", "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    main()
