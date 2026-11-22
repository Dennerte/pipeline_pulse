import os
import sys
from time import sleep

def health_checker(formatted_url):
    i = 0

    while i < 4:
        exit_code = os.system(f'curl.exe --fail -i "{formatted_url}"')

        if exit_code != 0:
            sleep(3)
            i += 1
            continue
        else:
            exit(0)


def url_formatter(url):
    health_postfix = "/health"

    url = url[1] + health_postfix
    print (url)

    return url

def main(argv):
    formatted_url = url_formatter(argv)
    health_checker(formatted_url)

main(sys.argv)