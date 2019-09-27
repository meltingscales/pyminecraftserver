import argparse

from pyminecraftserver.downloadlib import save_response_to_file, get_results_from_url


def test_download():
    save_response_to_file(
        get_results_from_url(
            'https://www.curseforge.com/minecraft/modpacks/volcano-block/download/2786736/file'),
        'test.zip')


if __name__ == '__main__':
    test_download()

    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--file", required=True)

    args = parser.parse_args()

    save_response_to_file(get_results_from_url(args.url), args.file)
