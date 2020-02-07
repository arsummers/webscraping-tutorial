from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

def simple_get(url):
    """
    makes an HTTP GET request at the url. Returns HTML or XML if that content exists, otherwise returns none
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    
    except RequestException as e:
        log_error('Error during request to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    """
    returns True if the response is HTML, otherwise returns False
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)

def log_error(e):
    """
    logs error as string
    """
    print(e)
    