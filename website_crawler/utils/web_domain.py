from urllib import parse  # module that splits and parses URLs into (string) components
from urllib.request import urlopen  # module that allows us to connect to web pages from Python


# get a full ("absolute") url by combining a "base_url" with another url in case of the url being relative
def get_absolute_url(base_url, url):
    return parse.urljoin(base_url, url)


def get_protocol(url):
    sep = "://"
    protocol = str(url).split(sep)[0]
    if protocol == "https" or protocol == "http":
        return protocol + sep
    else:
        # get other href links ('mailto:', 'tel:', 'javascript':)
        sep = ":"
        return str(url).split(sep)[0] + sep


# get (host) domain
def get_domain(url):
    results = get_sub_domain(url).split(".")
    if len(results) > 1:
        domain_name = str(results[-2]) + "." + str(results[-1])
        return domain_name
    else:
        return results


# get sub domain name name (name.example.com)
def get_sub_domain(url):
    try:
        return parse.urlparse(url).netloc
    except:
        return ""


def get_html_response(url):
    try:
        page = urlopen(url).read().decode("utf-8")
        return page
    except:
        print("Could not get (response) html page from url request")
        return ""


def get_href_format(url):
    return "." + url.split(".")[-1]


def check_domain_link(url, domain):
    """
    function check if the url contains the domain and returns TRUE or False
    """
    if str(url).__contains__(str(domain)):
        # print("%s contains %s" % (domain, url))
        return True
    else:
        # print("%s not in %s" % (domain, url))
        return False
    pass


def open_web_page(url):
    try:
        page = urlopen(url)
        return page
    except:
        return ""
