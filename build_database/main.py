from constants import REDIRECTS_PARSED_FILEPATH
from download import main as download
from parse_redirects import main as parse_redirects
from parse_pages import main as parse_pages

if __name__ == "__main__":
    download()
    parse_redirects()
    parse_pages()
