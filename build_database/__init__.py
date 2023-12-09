from .download import main as download
from .parse_pages import main as parse_pages
from .parse_redirects import main as parse_redirects
from .prune_pages_and_redirects import main as prune_pages_and_redirects
from .parse_links import main as parse_links
from .create_adjacency_matrix import main as create_adjacency_matrix


def build():
    download()
    parse_redirects()
    parse_pages()
    prune_pages_and_redirects()
    parse_links()
    create_adjacency_matrix()
