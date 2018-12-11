import requests
import sys


def get_request(url):
    try:
        request_page = requests.get(url)
        return request_page
    except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
        print(f"Request Time Out error: {e}")
    except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
        print(f"URL was bad: {e}")
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        print(e)
        sys.exit(1)
