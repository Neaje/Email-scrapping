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

def extract_emails_from_wordlist(text, wordlist):
    emails = set()
    with open(wordlist, "r") as wordlist_file:
        wordlist_words = [word.strip() for word in wordlist_file]
        for word in wordlist_words:
            pattern = r'\b[\w\.-]*' + re.escape(word) + r'[\w\.-]*@[\w\.-]+'
            matches = re.findall(pattern, text, re.I)
            emails.update(matches)
    return emails
   
def get_url_intern(soup, base_url):  
    url_intern = set()

    for a_tag in soup.find_all("a", href=True):
        href = a_tag.attrs['href']

        if href.startswith("/"):
            href = base_url.rstrip('/') + '/' + href.lstrip('/')

        if base_url in href:
            url_intern.add(href)
                
    return url_intern

def print_logo(): 
    print(pyfiglet.figlet_format("Email Scrapper"))

if __name__ == "__main__":
    
    print_logo()
    
    parser =  argparse.ArgumentParser(description="Scrap emails from a list of websites")
    parser.add_argument("-f", "--file", help="Path to the file containing the websites links", required=True)
    parser.add_argument("-w" , "--wordlist", help="Path to the wordlist containing emails pattern", required=False)
    parser.add_argument("-t", "--timeout", help="Timeout in seconds for the requests", required=False, type=int)
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

    if args.wordlist:
        print(f"\033[1;32mScraping {len_csv} websites using {args.wordlist}...\033[0m" + "\n")
    else:
        print(f"\033[1;32mScrapping {len_csv} websites...\033[0m" + "\n")

    for i, url in enumerate(urls):
        print(f"Scrapping {url} ({i + 1}/{len_csv})...")
        start_time = time.time()
        links_tried = 0
        found_with_wordlist = False
        timeout_occured = False

        try : 
            r = requests.get(url)
            soup = BeautifulSoup(r.text, "html.parser")
            links = get_url_intern(soup, url)
            len_links = len(links)

            for link in links:
                links_tried += 1
                r = requests.get(link)
                if args.wordlist:
                    emails = extract_emails_from_wordlist(r.text, args.wordlist)
                    if emails:
                        found_with_wordlist = True
                else:
                    emails = extract_emails(r.text)

                if time.time() - start_time > args.timeout:
                    timeout_occured = True
                    print(f"\033[1;31mTimeout reached for {url}\033[0m")
                    break
                
                print(f"Links tried for {url} : {links_tried}/{len_links}", end="\r")

                for email in emails:
                    email = email.lower()
                    if email not in extracted_emails:
                        extracted_emails.add(email)
                        with open ("emails.csv", "a") as csvfile:
                            csv_writer = csv.writer(csvfile)
                            csv_writer.writerow([name[urls.index(url)], email])
            
            if args.wordlist and not found_with_wordlist:
                print(f"\033[1;31mNo emails found with the wordlist after trying on {links_tried} pages, trying with the initial regex pattern...")
                count_remaining_emails = 0

                for link in links:
                    r = requests.get(link)
                    remaining_emails = extract_emails(r.text)

                    for email in remaining_emails:
                        email = email.lower()
                        count_remaining_emails += 1
                        if email not in extracted_emails:
                            extracted_emails.add(email)
                            with open("emails.csv", "a") as csvfile:
                                csv_writer = csv.writer(csvfile)
                                csv_writer.writerow([name[urls.index(url)], email])

                    if count_remaining_emails >= 10:
                        print(f"\033[1;32m{count_remaining_emails} emails found with the initial regex pattern, stopping the search...\033[0m" + "\n")
                        break

            if not timeout_occured: 
                print(f"\033[1;32mScrapping for {url} done in : {round(time.time() - start_time, 2)} seconds\033[0m" + "\n")
 
        except requests.RequestException as e:
            print(f"\033[1;31mError while scrapping {url} : {e}\033[0m" + "\n")

print("\033[1;32mScrapping done.\033[0m")
