#! /usr/bin/env python3

import argparse
import time

import cfscrape
from joblib import Memory
import os
import sys

# see https://github.com/Anorov/cloudflare-scrape
from requests import Response

location = os.path.join(os.path.abspath(os.path.dirname(__file__)), ".cache_download_file")
file_memory_cache = Memory(location)


def url_filename(url: str) -> str:
    return os.path.basename(url)


def response_filename(response: Response, bad_filenames=frozenset(['file', 'download'])):
    """
    Given a Response, return a filename.

    Useful for crappy site URLs like 'www.mycoolshit.ru/download/2315623/file' that redirect you to some ZIP file with
    an actual name, but the URL has no name.

    :param response: the Response object.
    :param bad_filenames: Filenames to not consider.
    :return: A filename not in bad_filenames
    """

    # If its filename sucks,
    if url_filename(response.url) in bad_filenames:

        # Go through its previous responses.
        for prev_response in response.history:

            potential_filename = response_filename(prev_response)

            # If its filename doesn't suck, return it.
            if potential_filename is not None:
                return potential_filename
            else:  # Return None.
                return None

        # We've run out of candidates!
        return 'unknown_filename.fileext'

    else:
        return url_filename(response.url)


def get_results_from_url(url: str, cache=file_memory_cache) -> Response:
    """
    Given a URL, return the response from it.
    This function caches responses that are HTTP 200.

    :param cache: The cache.
    :param url: The URL.
    :return: a Response object.
    """

    def _get_results_from_url(url):
        """Internal method that caches per-URL responses."""
        print('[NEW URL] {}'.format(url))
        scraper = cfscrape.create_scraper()
        result = scraper.get(url)

        if result.status_code != 200:
            raise Exception("Response did not return HTTP OK!")

        return result

    # Cache our function.
    _get_results_from_url = cache.cache(_get_results_from_url)

    return _get_results_from_url(url)


def save_response_to_file(response: Response, filepath: str):
    print('{}\n'
          '-->\n'
          '{}...'.format(response,
                         filepath))

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

