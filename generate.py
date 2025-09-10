from datetime import datetime
import os
import re
import urllib.request

import pytz
from tqdm import tqdm
import validators

LOG_PATH   = "./log.log"
TIMEZONE   = "America/Chicago"
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.3"

def log (*args, file_only = False):
    message   = " ".join(str(arg) for arg in args)
    timestamp = datetime.now(pytz.timezone(TIMEZONE)).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    entry     = f"[{timestamp}] {message}"

    print(entry)

    if LOG_PATH is not None:
        with open(LOG_PATH, "a") as log_file:
            log_file.write(f"{entry}\n")

def read_file_lines (filepath):
    with open(filepath, "r") as target_file:
        return target_file.read().splitlines()

def download_file_and_get_lines (url):
    request = urllib.request.Request(url, headers={ "User-Agent": USER_AGENT })

    try:
        log("Downloading:", url)

        with urllib.request.urlopen(request) as response:
            data = response.read().decode('utf-8')
            return data.splitlines()
    except urllib.error.URLError as e:
        print(f"Error on {url}: {e.reason}")

def write_list (lines, output_path):
    with open(output_path, "w") as output_file:
        for line in lines:
            output_file.write(line + "\n")

def validate_source_url (url):
    is_valid = False

    if len(url) == 0:
        pass
    elif url.startswith("#"):
        pass
    elif ' ' in url:
        log('Skipping - space found in URL:', url)
    elif not url.startswith("https"):
        log('Skipping - URL must begin with https://... :', url)
    elif not validators.url(url):
        log('Skipping - invalid URL passed in:', url)
    else:
        is_valid = True

    return is_valid

def extract_domains (domains_list, prepend_www = False):
    domains = []

    for line in domains_list:
        domain = line.strip()
        domain = re.sub(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", '', domain).strip() # strip IP
        domain = re.sub(r"\s*#.*$", '', domain).strip() # strip comment
        domain = re.sub(r"^\|\||\^.*$", '', domain).strip() # support uBlock static filter syntax

        if len(domain) == 0:
            pass
        elif domain.startswith('#'):
            pass
        elif ' ' in domain:
            log('Skipping - space found in domain:', domain)
        elif '.' not in domain:
            log('Skipping - dot not found in domain:', domain)
        elif '::' in domain:
            log('Skipping - ipv6 IP found:', domain)
        elif domain in ['localhost', 'localhost.localdomain', 'broadcasthost', 'local']:
            log('Skipping - ipv6 IP found:', domain)
        elif domain in ['ip6-localhost', 'ip6-loopback', 'ip6-localnet', 'ip6-mcastprefix', 'ip6-allnodes', 'ip6-allrouters', 'ip6-allhosts']:
            log('Skipping - ip6 loopback found:', domain)
        elif domain in ['0.0.0.0', '127.0.0.1']:
            log('Skipping - local IP found:', domain)
        else:
            domains.append(domain)

            if prepend_www:
                domains.append(f"www.{domain}")

    return domains

def get_domains_from_source_url (source_url):
    return extract_domains(download_file_and_get_lines(source_url), False)

def get_domains_from_sources (source_url_list):
    return [
        domain
        for source_url in tqdm(source_url_list, desc="Processing source list.")
        if validate_source_url(source_url)
        for domain in get_domains_from_source_url(source_url)
    ]

def get_lists_in_directory (directory_path):
    return [
        f"{directory_path}/{filepath}"
        for filepath in os.listdir(directory_path)
        if (not filepath.startswith('.') and (filepath.endswith('.txt')))
    ]

def get_domains_from_list (list_filepath):
    return extract_domains(read_file_lines(list_filepath), True)

def get_domains_from_lists (list_filepaths, description):
    return [
        domain
        for list_filepath in tqdm(list_filepaths, desc=description)
        for domain in get_domains_from_list(list_filepath)
    ]

def main ():
    log("START.")

    blacklist = []
    whitelist = []

    blacklists_sources = read_file_lines("./data/sources/blacklists.txt")
    whitelists_sources = read_file_lines("./data/sources/whitelists.txt")

    blacklist += get_domains_from_sources(blacklists_sources)
    whitelist += get_domains_from_sources(whitelists_sources)

    blacklist_files = get_lists_in_directory("./data/blacklists")
    whitelist_files = get_lists_in_directory("./data/whitelists")

    blacklist += get_domains_from_lists(blacklist_files, "Processing blacklist files.")
    whitelist += get_domains_from_lists(whitelist_files, "Processing whitelist files.")

    blacklist = sorted(list(set(blacklist) - set(whitelist)))

    blacklist_preamble = ["# SOURCE: https://raw.githubusercontent.com/rramphal/hosts/master/lists/blacklist\n"]
    hosts_preamble     = ["# SOURCE: https://raw.githubusercontent.com/rramphal/hosts/master/lists/hosts\n"]
    postamble          = [f"\n# LAST UPDATED: {datetime.now(pytz.timezone(TIMEZONE)).strftime('%Y-%m-%d %H:%M:%S')}"]

    localhost = read_file_lines("./data/localhost.txt")

    write_list(blacklist_preamble + blacklist + postamble, "./lists/blacklist")
    write_list(hosts_preamble + localhost + ["0.0.0.0 " + item for item in blacklist] + postamble, "./lists/hosts")

    log("END.")

main()
