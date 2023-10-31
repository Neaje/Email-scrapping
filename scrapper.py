##############################
# AUHTORS : Neaje & Potclean #
##############################

from bs4 import BeautifulSoup
import requests
import re
import csv
import time
import argparse


def extract_emails(text):
    return set(re.findall(r"[a-z0-9.\-+_]+@[a-z0-9.\-+_]+\.(?!png\b)[a-z]+", text, re.I))

def get_url_intern(soup, base_url):  
    url_intern = set()

    for a_tag in soup.find_all("a", href=True):
        href = a_tag.attrs['href']

        if href.startswith("/"):
            href = base_url.rstrip('/') + '/' + href.lstrip('/')

        if base_url in href:
            url_intern.add(href)
                
    return url_intern

if __name__ == "__main__":
    
    parser =  argparse.ArgumentParser(description="Scrap emails from a list of universities")
    parser.add_argument("-f", "--file", help="path to the file containing the universities links", required=True)
    args = parser.parse_args()

    urls = []
    univ = []
    extracted_emails = set()

    with open(args.file, "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader) 

        for line in csv_reader:
            urls.append(line[1])
            univ.append(line[0])

    print("Starting scrapping..." + "\n")

    for url in urls:
        print(f"Scrapping {url}...")
        start_time = time.time()

        try : 
            r = requests.get(url)
            soup = BeautifulSoup(r.text, "html.parser")
            links = get_url_intern(soup, url)

            for link in links:
                r = requests.get(link)
                soup = BeautifulSoup(r.text, "html.parser")
                emails = extract_emails(r.text)

                for email in emails: 
                    email = email.lower()
                    if email not in extracted_emails:
                        extracted_emails.add(email)
                        with open ("emails.csv", "a") as csvfile:
                            csv_writer = csv.writer(csvfile)
                            csv_writer.writerow([univ[urls.index(url)], email])

            print(f"Scrapping for {url} done in : {time.time() - start_time} seconds" + "\n")

        except requests.RequestException as e:
            print(f"Erreur lors du scrapping de {url} : {e}")

print("Scrapping done.")
