import requests
from bs4 import BeautifulSoup
import time
from colorama import Fore

ascii_art = r"""
██╗  ██╗██████╗ ██╗  ██╗██████╗ ██╗      ██████╗ ██╗████████╗ ██████╗ ██╗  ██╗ ██╗
██║  ██║╚════██╗╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝██╔═████╗╚██╗██╔╝███║
███████║ █████╔╝ ╚███╔╝ ██████╔╝██║     ██║   ██║██║   ██║   ██║██╔██║ ╚███╔╝ ╚██║
██╔══██║ ╚═══██╗ ██╔██╗ ██╔═══╝ ██║     ██║   ██║██║   ██║   ████╔╝██║ ██╔██╗  ██║
██║  ██║██████╔╝██╔╝ ██╗██║     ███████╗╚██████╔╝██║   ██║   ╚██████╔╝██╔╝ ██╗ ██║
╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝ ╚═╝                            
	 Telegram: H3Xploit0X1  ***  Github: H3Xploit0X1
"""

print(Fore.RED + ascii_art)

def scrape_domains_and_ips(tld, max_pages):
    base_url = "https://www.topsitessearch.com/domains/"
    full_url = f"{base_url}{tld}/"
    domains_and_ips = []

    for page in range(1, max_pages + 1):
        print(Fore.MAGENTA + f"Scraping page {page} ", end="")
        for _ in range(5):  # Add a countdown or dots
            print(".", end="", flush=True)
            time.sleep(0.3)  # Pause for effect
        print()  # Move to the next line after dots

        url = f"{full_url}{page}/"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for HTTP issues
        except requests.exceptions.RequestException as e:
            print(Fore.RED + f"Error accessing {url}: {e}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')

        # Locate the table rows containing domains and IP addresses
        rows = soup.find_all('tr')  # Find all table rows (<tr> tags)

        for row in rows:
            cols = row.find_all('td')  # Find all table cells (<td> tags) in a row
            if len(cols) >= 2:  # Ensure there are enough columns (Domain, IP Server)
                domain = cols[0].get_text(strip=True)  # First column: domain
                ip_address = cols[1].get_text(strip=True)  # Second column: IP address
                domains_and_ips.append((domain, ip_address))

        # Stop if no "Next Page" link is found (to avoid unnecessary requests)
        next_page = soup.find('a', string="Next Page »")
        if not next_page:
            print(Fore.RED + "No more pages to scrape. Exiting.")
            break

    return domains_and_ips

if __name__ == "__main__":
    tld = input(Fore.CYAN + "Enter the TLD (e.g., .com, .org, .net): ").strip()
    try:
        max_pages = int(input(Fore.CYAN + "Enter the number of pages to scrape: ").strip())
        if max_pages <= 0:
            raise ValueError("Number of pages must be greater than 0.")
    except ValueError as e:
        print(Fore.RED + f"Invalid input for number of pages: {e}")
        exit()

    domains_and_ips = scrape_domains_and_ips(tld, max_pages)
    
    if domains_and_ips:
        print(Fore.YELLOW + "\nFound domains and IP addresses:")
        for domain, ip in domains_and_ips:
            print(Fore.GREEN + f"{domain} , {ip}")
    else:
        print(Fore.RED + "No domains and IP addresses found.")
