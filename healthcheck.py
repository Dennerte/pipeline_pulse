import os
import sys
from time import sleep

def health_checker(formatted_url):
    for attempt in range(4):
        exit_code = os.system(f'curl.exe --fail -i "{formatted_url}"')

        if exit_code == 0:
            sys.exit(0)

        if attempt < 3:
            sleep(3)

    print("Healthcheck failed after 4 tries.")
    sys.exit(1)


def url_formatter(url):
    health_postfix = "/health"

    url = url[1] + health_postfix
    return url

def main(argv):
    formatted_url = url_formatter(argv)
    health_checker(formatted_url)

main(sys.argv)
