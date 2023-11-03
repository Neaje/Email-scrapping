# Email scrapper
Python script extracts email addresses from a list of websites using libraries like BeautifulSoup and Requests. It parses websites, locates internal links (Non-recursive), and filters unique email addresses, associating them with website names. Users must use it responsibly and comply with website terms and regulations.

## Installation
```bash
git clone https://github.com/Neaje/Email-scrapping.git
cd Email-scrapping
pip3.11 install -r requirements.txt
```

## Usage 
```bash
 _____                 _ _   ____                                       
| ____|_ __ ___   __ _(_) | / ___|  ___ _ __ __ _ _ __  _ __   ___ _ __ 
|  _| | '_ ` _ \ / _` | | | \___ \ / __| '__/ _` | '_ \| '_ \ / _ \ '__|
| |___| | | | | | (_| | | |  ___) | (__| | | (_| | |_) | |_) |  __/ |   
|_____|_| |_| |_|\__,_|_|_| |____/ \___|_|  \__,_| .__/| .__/ \___|_|   
                                                 |_|   |_|              

usage: scrapper.py [-h] -f FILE [-w WORDLIST]

Scrap emails from a list of websites

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  path to the file containing the websites links
  -w WORDLIST, --wordlist WORDLIST
                        path to the wordlist containing emails pattern
```

### Specification
Your CSV file should be in the following format :
```
<name_of_website>,<link>
```

And The wordlist should be in the following format :
```
<email_pattern>
```

it will match for example :
```
<email_pattern>@exemple.com
```

## Disclaimer: Use of this script 
This script is provided for informational purposes and convenience. Please be aware that its use is at your own discretion and risk. I, as the provider of this script, cannot be held responsible for any misuse or unauthorized activities.

I strongly advise all users to use this script exclusively on websites for which they possess the necessary permissions and authorizations. It is essential to respect the terms of service and regulations of any website you interact with using this script.

Remember that unauthorized or improper use of this script may violate applicable laws and the terms of service of the respective websites, potentially resulting in legal consequences.

By using this script, you acknowledge and accept your responsibility to use it responsibly and within the bounds of the law. Always ensure you have the appropriate permissions and follow ethical guidelines when using any software or script.
