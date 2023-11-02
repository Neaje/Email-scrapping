##############################
# AUHTORS : Neaje & Potclean #
##############################

from bs4 import BeautifulSoup
import requests
import re
import csv
import time
import argparse
import pyfiglet

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
    
    print(pyfiglet.figlet_format("Email Scrapper"))
    
    parser =  argparse.ArgumentParser(description="Scrap emails from a list of websites")
    parser.add_argument("-f", "--file", help="path to the file containing the websites links", required=True)
    args = parser.parse_args()

    urls = []
    name = []
    extracted_emails = set()

    with open(args.file, "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        len_csv = sum(1 for row in csv_reader)
        csvfile.seek(0)
        next(csv_reader) 

        for line in csv_reader:
            urls.append(line[1])
            name.append(line[0])

    print(f"\033[1;32mScrapping {len_csv} websites...\033[0m" + "\n")

    for i, url in enumerate(urls):
        print(f"Scrapping {url} ({i + 1}/{len_csv})...")
        start_time = time.time()
        links_tried = 0

        try : 
            r = requests.get(url)
            soup = BeautifulSoup(r.text, "html.parser")
            links = get_url_intern(soup, url)
            len_links = len(links)

            for link in links:
                links_tried += 1
                r = requests.get(link)
                soup = BeautifulSoup(r.text, "html.parser")
                emails = extract_emails(r.text)
                print(f"Links tried for {url} : {links_tried}/{len_links}", end="\r")
            
                for email in emails:
                    email = email.lower()
                    if email not in extracted_emails:
                        extracted_emails.add(email)
                        with open ("emails.csv", "a") as csvfile:
                            csv_writer = csv.writer(csvfile)
                            csv_writer.writerow([name[urls.index(url)], email])

            print(f"\033[1;32mScrapping for {url} done in : {round(time.time() - start_time, 2)} seconds\033[0m" + "\n")

        except requests.RequestException as e:
            print(f"\033[1;31mError while scrapping {url} : {e}\033[0m" + "\n")

print("\033[1;32mScrapping done.\033[0m")
