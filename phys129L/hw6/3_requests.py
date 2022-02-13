"""
TKC!
Web Page with requests
Matthew Wong
Phys 129L Hw6 Pb3
2022-02-17
"""

import re
import requests

def main():
    """Checks when the web page announcements were last updated."""
    r = requests.get("https://web.physics.ucsb.edu/~phys129/lipman")
    match = re.search(r"Latest update:.*?>(.*?)<", r.text)
    if match:
        last_updated = re.sub("&nbsp;", ' ', match.group(1))
    print(f"The web page announcements were last updated on:\n{last_updated}")

if __name__ == "__main__":
    main()
