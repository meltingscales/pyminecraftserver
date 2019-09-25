#! /usr/bin/env python3

import argparse
import time

import cfscrape
from joblib import Memory
import os
import sys

# see https://github.com/Anorov/cloudflare-scrape
from requests import Response

parser = argparse.ArgumentParser()
parser.add_argument("--url", required=True)
parser.add_argument("--file", required=True)

location = "./.cache_download_file"
file_memory_cache = Memory(location)


def get_results_from_url(url: str) -> Response:
    """
    Given a URL, return the response from it.
    :param url: The URL.
    :return: a Response object.
    """
    print("getting " + url)

    scraper = cfscrape.create_scraper()
    result = scraper.get(url)

    return result


def get_results_from_url_cached(url: str, cache=file_memory_cache) -> Response:
    """
    Given a URL, return the response from it.
    This function caches responses that are HTTP 200.
    :param cache: The cache.
    :param url: The URL.
    :return: a Response object.
    """

    def _get_results_from_url(url):
        """Internal method that caches per-URL responses."""
        print('We have never seen %s before.'.format(url))
        scraper = cfscrape.create_scraper()
        result = scraper.get(url)

        if result.status_code != 200:
            raise Exception("Response did not return HTTP OK!")

        return result

    # Cache our function.
    _get_results_from_url = cache.cache(_get_results_from_url)

    return _get_results_from_url(url)


def save_response_to_file(response: Response, filepath: str):
    print("Saving this:")
    print(response)

    print("To this:")
    print(filepath)

    if response.status_code != 200:
        print("Response is NOT ok. Cloudflare is on to us!")
        exit(1)

    with open(filepath, 'wb') as file:
        file.write(response.content)

    print("Saved!")


def test_cache():
    def expensive_function(x):
        time.sleep(5)
        return x + 1

    print(file_memory_cache.cache(expensive_function)(3))


def test_download():
    save_response_to_file(
        get_results_from_url_cached(
            'https://www.curseforge.com/minecraft/modpacks/volcano-block/download/2786736/file'),
        'test.zip')


if __name__ == '__main__':

    # test_download()

    args = parser.parse_args()

    save_response_to_file(get_results_from_url_cached(args.url), args.file)
