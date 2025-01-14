import requests
import re
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

# Function to get domains from Google Custom Search API
def get_domains_from_google(tld, api_key, search_engine_id, max_results=100, query_variation=""):
    query = f"site:{tld} {query_variation}"
    url = "https://www.googleapis.com/customsearch/v1"
    domains = []
    
    for start_index in range(1, max_results, 10):  # 10 results per request
        params = {
            "q": query,
            "key": api_key,
            "cx": search_engine_id,
            "num": 10,
            "start": start_index,
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            for item in data.get("items", []):
                match = re.search(r"https?://(www\.)?([^/]+)", item["link"])
                if match:
                    domains.append(match.group(2))
            
            # Stop if fewer results than expected are returned
            if len(data.get("items", [])) < 10:
                break

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            break
        except KeyError:
            print("Unexpected response format.")
            break

    return domains

# Function to save domains to a file
def save_domains_to_file(domains, filename="domains.txt"):
    try:
        with open(filename, "w") as file:
            for domain in domains:
                file.write(domain + "\n")
        print(Fore.CYAN + f"Domains saved to {filename}")
    except Exception as e:
        print(f"Error saving to file: {e}")

# Main script logic
if __name__ == "__main__":
    # Replace with your actual API key and search engine ID
    API_KEY = "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
    SEARCH_ENGINE_ID = "$$$$$$$$$$$$$$"
    
    tld = input(Fore.CYAN + "Enter the TLD (e.g., .com, .org, .net): ").strip()
    if not tld.startswith("."):
        print(Fore.RED + "Please provide a valid TLD starting with '.'")
    else:
        print(Fore.YELLOW + f"Searching for domains with TLD '{tld}'...")
        
        # First 100 results
        results_1 = get_domains_from_google(tld, API_KEY, SEARCH_ENGINE_ID, max_results=100)
        
        # Second 100 results (using query variation, e.g., additional keyword "a")
        results_2 = get_domains_from_google(tld, API_KEY, SEARCH_ENGINE_ID, max_results=100, query_variation="a")
        
        # Combine and remove duplicates
        all_results = list(set(results_1 + results_2))
        
        if all_results:
            print(Fore.MAGENTA + f"Found {len(all_results)} unique domains:")
            for domain in all_results:
                print(Fore.GREEN + domain)
            
            # Save domains to file
            save_domains_to_file(all_results, "domains.txt")
        else:
            print(Fore.RED + "No domains found or an error occurred.")
