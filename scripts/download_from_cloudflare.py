#! /usr/bin/env python3

import argparse
import cfscrape
import os
import sys

# see https://github.com/Anorov/cloudflare-scrape
from requests import Response

parser = argparse.ArgumentParser()
parser.add_argument("--url", required=True, default='')
parser.add_argument("--file", required=True)


def get_results_from_url(url: str) -> Response:
    print("getting " + url)

    scraper = cfscrape.create_scraper()
    return scraper.get(url)


def save_response_to_file(response: Response, filepath: str):
    print("Saving this:")
    print(response)

    print("To this:")
    print(filepath)

    if(response.status_code != 200):
        print("Response is NOT ok. Cloudflare is on to us!")
        exit(1)

    with open(filepath, 'wb') as file:
        file.write(response.content)

    print("Saved!")


if __name__ == '__main__':
    # # test
    # save_response_to_file(
    #     get_results_from_url('https://www.curseforge.com/minecraft/modpacks/volcano-block/download/2786736/file'),
    #     'test.zip')

    args = parser.parse_args()

    save_response_to_file(get_results_from_url(args.url), args.file)
