import requests
import sys

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

MAX_RETRY_NUM = 5
BACKOFF_FACTOR = 1
STATUS_FORCELIST = [502, 503, 504]


def get_request(url):
    """
    Attempts to get the HTML content with the given URL by making an HTTP GET request. It is set up to
    retry the request for a maximum number of retries.
    :param url:
    :return:
    """
    try:
        session = requests.Session()
        retries = Retry(total=MAX_RETRY_NUM, backoff_factor=BACKOFF_FACTOR, status_forcelist=STATUS_FORCELIST)
        session.mount('http://', HTTPAdapter(max_retries=retries))
        request_page = session.get(url)
        return request_page
    except requests.exceptions.ConnectionError as errc:
        # ConnectionError occurs in the event of a network problem (DNS failure, refused connection)
        print(f"Connection error: {errc}")
    except requests.exceptions.HTTPError as errh:
        # HTTPError occurs in the event of a rare invalid HTTP response
        print(f"HTTP error: {errh}")
    except requests.exceptions.Timeout as errt:
        # Timeout exception occurs whenever a request times out
        print(f"Request timeout error: {errt}")
    except requests.exceptions.TooManyRedirects as errm:
        # TooManyRedirects exception occurs if a request exceeds the configured number of maximum redirections
        print(f"URL was bad: {errm}")
    except requests.exceptions.RequestException as err:
        # RequestException occurs for any kind of exceptions that are raised
        print(f"Error during requests to {url}: {err}")
        sys.exit(1)
