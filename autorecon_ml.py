import requests
import pandas as pd
import time
import re
from googlesearch import search
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)


# PHASE 1: THE ML BRAIN (Training the Model)

def train_model():
    print(f"{Fore.CYAN}[*] Training ML Model on Recon Patterns...")
    
    # Synthetic dataset for training
    data = {
        'url': [
            'admin.php', 'login', 'wp-admin', '.env', 'config.js', 'backup.sql', 'db_backup', 
            'dashboard', 'cpanel', 'phpinfo.php', 'root', 'passwd', 'shadow', 'api_key',
            'about-us', 'contact', 'blog', 'news', 'privacy-policy', 'terms', 'sitemap', 
            'index.html', 'home', 'products', 'services', 'careers', 'faq'
        ],
        'label': [
            1, 1, 1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 1, 1,
            0, 0, 0, 0, 0, 0, 0, 
            0, 0, 0, 0, 0, 0
        ] # 1 = High Value, 0 = Low Value
    }
    
    df = pd.DataFrame(data)
    model = make_pipeline(CountVectorizer(), MultinomialNB())
    model.fit(df['url'], df['label'])
    print(f"{Fore.GREEN}[+] Model Trained Successfully!")
    return model


# PHASE 2: THE COLLECTOR (Gathering Data)

def get_subdomains(domain):
    print(f"{Fore.YELLOW}[*] Scraping Subdomains via crt.sh (Passive)...")
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    subdomains = set()
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            for entry in data:
                subdomains.add(entry['name_value'])
    except Exception as e:
        print(f"{Fore.RED}[!] Error fetching subdomains: {e}")
        
    print(f"{Fore.GREEN}[+] Found {len(subdomains)} unique subdomains.")
    return list(subdomains)

def google_dork_scan(domain):
    print(f"{Fore.YELLOW}[*] Running Automated Google Dorking (Active)...")
    dorks = [
        f"site:{domain} filetype:env",
        f"site:{domain} filetype:sql",
        f"site:{domain} inurl:admin",
        f"site:{domain} inurl:dashboard",
        f"site:{domain} intitle:\"index of\""
    ]
    
    found_urls = []
    for dork in dorks:
        print(f"    - Running: {dork}")
        try:
            time.sleep(2) 
            results = search(dork, num_results=5)
            for result in results:
                found_urls.append(result)
        except Exception as e:
            print(f"{Fore.RED}[!] Google Blocked or Error: {e}")
            break
            
    return found_urls


# PHASE 3: THE ANALYZER (Tech Stack & Emails)

def get_tech_stack(url):
    try:
        if not url.startswith("http"): url = "http://" + url
        response = requests.get(url, timeout=3)
        server = response.headers.get('Server', 'Unknown')
        powered_by = response.headers.get('X-Powered-By', 'Unknown')
        print(f"{Fore.BLUE}    [Tech] {url}: Server={server} | Backend={powered_by}")
        return f"{server} | {powered_by}"
    except:
        return "Dead"

def extract_emails(domain):
    print(f"{Fore.YELLOW}[*] Hunting for Employees/Emails...")
    dork = f"site:{domain} \"@ {domain}\"" 
    emails = set()
    try:
        results = search(dork, num_results=5)
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        
        for link in results:
            try:
                page_content = requests.get(link, timeout=5).text
                found = re.findall(email_pattern, page_content)
                for email in found:
                    if domain in email:
                        emails.add(email)
            except: continue
    except Exception as e:
        print(f"{Fore.RED}[!] Email hunt blocked: {e}")
    
    print(f"{Fore.GREEN}[+] Found {len(emails)} emails.")
    return list(emails)


# PHASE 4: MAIN EXECUTION

def main():
    print(f"{Fore.MAGENTA}=== AutoRecon-ML: The Complete Suite ===")
    target = input("Enter Target Domain (e.g., tesla.com): ")
    
    # 1. Train
    model = train_model()
    
    # 2. Recon
    subdomains = get_subdomains(target)
    emails = extract_emails(target)
    dork_links = google_dork_scan(target)
    
    # 3. Analysis
    print(f"\n{Fore.CYAN}[*] Running ML Analysis & Tech Fingerprinting...")
    high_value_targets = []
    all_assets = subdomains + dork_links
    
    # Check Tech Stack for first 5 subdomains
    for s in subdomains[:5]:
        get_tech_stack(s)

    # ML Prediction
    for asset in all_assets:
        prediction = model.predict([asset])[0]
        if prediction == 1:
            high_value_targets.append(asset)
            
    # 4. Report
    print(f"\n{Fore.WHITE}=== [RECON REPORT FOR {target}] ===")
    print(f"Emails Found: {len(emails)}")
    print(f"Subdomains: {len(subdomains)}")
    print(f"{Fore.RED}[CRITICAL] High-Risk Assets Found:")
    for t in high_value_targets:
        print(f" -> {t}")

if __name__ == "__main__":
    main()