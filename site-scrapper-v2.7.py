#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests, re, sys, time, os
from multiprocessing.dummy import Pool
from colorama import Fore, Style, init

init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

PRIMARY = Fore.CYAN + Style.BRIGHT
ACCENT = Fore.MAGENTA + Style.BRIGHT
GOOD = Fore.GREEN + Style.BRIGHT
WARN = Fore.YELLOW + Style.BRIGHT
BAD = Fore.RED + Style.BRIGHT
DIM = Style.DIM + Fore.WHITE
RESET = Style.RESET_ALL


def cinput(prompt: str, color: str = PRIMARY) -> str:
    """Colorized input prompt."""
    return input(color + prompt + RESET)

def show_banner():
    clear_screen()
    print(ACCENT + r"""
===========================================
 SITE SCRAPER v2.7 - By T.ME/R00TXATTACKER
===========================================
""" + RESET)

    print(PRIMARY + "Scrape Directly:" + RESET)
    print(GOOD + "  [1] " + Fore.WHITE + "topmillion.net" + RESET)
    print()

    print(PRIMARY + "Scrape By TLD:" + RESET)
    print(GOOD + "  [2] " + Fore.WHITE + "azstats.org" + RESET)
    print(GOOD + "  [3] " + Fore.WHITE + "dubdomain.com" + RESET)
    print(GOOD + "  [4] " + Fore.WHITE + "greensiteinfo.com" + RESET)
    print()

    print(PRIMARY + "Scrape By Date:" + RESET)
    print(GOOD + "  [5] " + Fore.WHITE + "uidomains.com" + RESET)
    print(GOOD + "  [6] " + Fore.WHITE + "websitebiography.com" + RESET)
    print(ACCENT + "==========================================" + RESET)


def save_domains(source: str, domains: list, option_number: int):
    """Persist domains and print standardized colored lines + count."""
    total = 0
    with open("domain.txt", "a", encoding="utf-8") as file:
        for host in domains:
            print(GOOD + f"[{option_number}] " + Fore.WHITE + f"From-{source}:" + GOOD + f"{host}" + RESET)
            file.write(host + "\n")
            total += 1
    print(WARN + f"[+] {total} websites scraped from {source}\n" + RESET)

def scrape_azstats():
    tld = cinput("Enter Top-Level Domain (e.g., com, org): ").strip()
    headers = {"User-Agent": "Mozilla/5.0"}
    results = []
    for page in range(1, 5):
        url = f"https://azstats.org/top/domain-zone/{tld}/{page}"
        try:
            html = requests.get(url, headers=headers, timeout=10).text
            hits = re.findall(r'style="margin-left: 0;">(.*?)</a>', html)
            results.extend(hits)
        except Exception as e:
            print(BAD + f"[!] Error fetching {url}: {e}" + RESET)
            continue
    save_domains("azstats.org", results, 2)


def scrape_topmillion():
    start_page = int(cinput("Enter starting page number: "))
    end_page = int(cinput("Enter ending page number: "))
    threads = int(cinput("Enter number of threads (e.g., 10): "))
    headers = {"User-Agent": "Mozilla/5.0"}
    results = []

    def fetch_page(page):
        url = f"https://www.topmillion.net/pages/websites/page/{page}/"
        try:
            html = requests.get(url, headers=headers, timeout=10).text
            matches = re.findall(r'https://(.*?)\?w=400" alt=', html)
            return [f"http://{m}" for m in matches]
        except Exception as e:
            print(BAD + f"[!] Error fetching {url}: {e}" + RESET)
            return []

    pool = Pool(threads)
    pages_data = pool.map(fetch_page, range(start_page, end_page + 1))
    pool.close(); pool.join()

    for batch in pages_data:
        results.extend(batch)

    save_domains("topmillion.net", results, 1)


def scrape_dubdomain():
    start_page = int(cinput("Enter starting page number: "))
    end_page = int(cinput("Enter ending page number: "))
    headers = {"User-Agent": "Mozilla/5.0"}
    results = []
    for page in range(start_page, end_page + 1):
        url = f"https://www.dubdomain.com/index.php?page={page}"
        try:
            html = requests.get(url, headers=headers, timeout=10).text
            matches = re.findall(r'data-src="https://www.google.com/s2/favicons\?domain_url=(.*?)"', html)
            results.extend([f"http://{m}" for m in matches])
        except Exception as e:
            print(BAD + f"[!] Error fetching {url}: {e}" + RESET)
            continue
    save_domains("dubdomain.com", results, 3)


def scrape_uidomains():
    date_input = cinput("Enter date (format: YYYY-MM-DD): ").strip()
    headers = {"User-Agent": "Mozilla/5.0"}
    results = []
    url = f"https://www.uidomains.com/browse-daily-domains-difference/0/{date_input}"
    try:
        html = requests.get(url, headers=headers, timeout=10).text
        matches = re.findall(r'<li>([a-zA-Z0-9\-.]+)</li>', html)
        results.extend([f"http://{m}" for m in matches])
    except Exception as e:
        print(BAD + f"[!] Error: {e}" + RESET)
    save_domains("uidomains.com", results, 5)


def scrape_greensiteinfo():
    tld = cinput("Enter Top-Level Domain (e.g., com, org): ").strip()
    start_page = int(cinput("Enter starting page number: "))
    end_page = int(cinput("Enter ending page number: "))
    headers = {"User-Agent": "Mozilla/5.0"}
    results = []
    for page in range(start_page, end_page + 1):
        url = f"https://www.greensiteinfo.com/domains/.{tld}/{page}/"
        try:
            html = requests.get(url, headers=headers, timeout=10).text
            matches = re.findall(r'<a href = https://www.greensiteinfo.com/search/(.*?)/ >', html)
            results.extend([f"http://{m}" for m in matches])
        except Exception as e:
            print(BAD + f"[!] Error fetching {url}: {e}" + RESET)
            continue
    save_domains("greensiteinfo.com", results, 4)


def scrape_websitebiography():
    date_input = cinput("Enter date (format: YYYY-MM-DD): ").strip()
    start_page = int(cinput("Enter starting page number: "))
    end_page = int(cinput("Enter ending page number: "))
    headers = {"User-Agent": "Mozilla/5.0"}
    results = []
    for page in range(start_page, end_page + 1):
        url = f"https://websitebiography.com/new_domain_registrations/{date_input}/{page}/"
        try:
            html = requests.get(url, headers=headers, timeout=10).text
            matches = re.findall(r"<a href='https://(.*?).websitebiography.com' title=", html)
            results.extend([f"http://{m}" for m in matches])
        except Exception as e:
            print(BAD + f"[!] Error fetching {url}: {e}" + RESET)
            continue
    save_domains("websitebiography.com", results, 6)

def main():
    show_banner()
    choice = cinput("Please select an option number from the menu: ").strip()
    if choice == '1': scrape_topmillion()
    elif choice == '2': scrape_azstats()
    elif choice == '3': scrape_dubdomain()
    elif choice == '4': scrape_greensiteinfo()
    elif choice == '5': scrape_uidomains()
    elif choice == '6': scrape_websitebiography()
    else:
        print(BAD + "Invalid Option! Please try again." + RESET)


if __name__ == "__main__":
    main()
