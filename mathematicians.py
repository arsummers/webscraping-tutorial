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

def get_names():
    """
    downloads the page where the list of mathematicians is, then returns a list of strings. One string per mathematician
    """
    url = 'http://www.fabpedigree.com/james/mathmen.htm'
    response = simple_get(url)

    if response is not None:
        html = BeautifulSoup(response, 'html.parser')
        names = set()
        for li in html.select('li'):
            for name in li.text.split('\n'):
                if len(name) > 0:
                    names.add(name.strip())
        return list(names)

    # if no data from url, raise exception
    raise Exception('Error retrieving contents at {}'.format(url))

def get_hits_on_name(name):
     """
    Accepts a `name` of a mathematician and returns the number
    of hits that mathematician's Wikipedia page received in the 
    last 60 days, as an `int`
    """
    # url_root is a template string that is used to build a URL.
    url_root = 'URL_REMOVED_SEE_NOTICE_AT_START_OF_ARTICLE'
    response = simple_get(url_root.format(name))

    if response is not None:
        html = BeautifulSoup(response, 'html.parser')

        hit_link = [a for a in html.select('a')
                    if a['href'].find('latest-60') > -1]

        if len(hit_link) > 0:
            #gets rid of commas
            link_text = hit_link[0].text.replace(',', '')
            try:
                # converts to integer
                return int(link_text)
            except:
                log_error("couldn't parse {} as an `int`".format(link_text))

    log_error('No pageviews found for {}'.format(name))
    return None

# MAIN CODE RUNNING HERE. EVERYTHING ABOVE IS SETUP
