import requests

def check_connection_and_api_status(api_urls):
    """
    Check if there is an active internet connection and if APIs are reachable.

    Args:
        api_urls (list): A list of API base URLs to check.

    Raises:
        ConnectionError: If there is no internet connection or if any API is not reachable.
    """
    # Check for internet connection
    try:
        requests.get('https://www.google.com/', timeout=5)
    except (requests.ConnectionError, requests.Timeout):
        raise ConnectionError("No internet connection available.")

    # Check API statuses
    for api_url in api_urls:
        try:
            response = requests.get(api_url, timeout=5)
            if response.status_code != 200:
                raise ConnectionError(f"API at {api_url} is not responding correctly.")
        except (requests.ConnectionError, requests.Timeout):
            raise ConnectionError(f"API at {api_url} is not reachable.")
