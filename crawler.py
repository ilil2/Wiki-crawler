import requests
from bs4 import BeautifulSoup
import os

def validate_url(url):
    if url == None:
        return False
    if not url.startswith("/wiki/"):
        return False
    if ":" in url:
        return False
    return True

def get_all_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        urls = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if validate_url(href):
                urls.append(href)
        return urls
    else:
        return []

def verify_url(urls, verify_urls):
    res = []
    for i in range(len(urls)):
        full_url = "https://fr.wikipedia.org" + urls[i]
        if full_url not in verify_urls and full_url not in res:
            res.append(full_url)
    return res

def print_urls(urls):
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    for url in urls:
        print(url)

def crawl_wikipedia(i, start_url, verify_urls):
    if i == 0:
        return
    urls = get_all_url(start_url)
    urls = verify_url(urls, verify_urls)
    verify_urls.update(urls)
    urls = sorted(urls)
    print("level : %s, len verif : %s, len urls : %s, start : %s"%(2-i, len(verify_urls), len(urls), start_url.split("/")[-1]))
    for j in range(len(urls)):
        crawl_wikipedia(i-1, urls[j], verify_urls)

def main():
    start_url = "https://fr.wikipedia.org/wiki/Alan_Turing"
    verify_urls = {start_url}
    crawl_wikipedia(2, start_url, verify_urls)
    print_urls(verify_urls)
    print("len : %s"%len(verify_urls))

if __name__ == "__main__":
    main()