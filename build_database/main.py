from constants import REDIRECTS_TRIMMED_FILEPATH
from download import main as download
from trim_redirects import main as trim_redirects
from trim_pages import main as trim_pages

if __name__ == "__main__":
    download()
    trim_redirects()
    trim_pages()
