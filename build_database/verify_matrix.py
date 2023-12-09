from constants import (
    PAGES_PRUNED_FILEPATH,
    WIKI_GRAPH_FILEPATH,
)
import pickle
import scipy.sparse as sp
from bidict import bidict

US_PAGE_ID = 3434750
ISBN_PAGE_ID = 14919


def main():
    with open(PAGES_PRUNED_FILEPATH, "rb") as f:
        pages = pickle.load(f)
    main_page_ids = {
        page_id for page_id, _title, is_redirect in pages if not is_redirect
    }
    page_id_to_idx = bidict({page_id: i for i, page_id in enumerate(main_page_ids)})
    title_id_map = bidict(
        {page_id: title for page_id, title, is_redirect in pages if not is_redirect}
    )

    # page_id_to_idx = bidict({page_id: i for i, page_id in enumerate(title_id_map)})

    pages = [3434750, 14919, 39394532]
    pages = [39394532]
    graph = sp.load_npz(WIKI_GRAPH_FILEPATH)
    subgraph = graph.sub

    for page_id in pages:
        title = title_id_map[page_id]
        idx = page_id_to_idx[page_id]
        # find the indices of all the incoming links
        incoming = graph[:, idx].nonzero()[0]
        incoming_ids = [page_id_to_idx.inverse[i] for i in incoming]
        incoming_titles = [title_id_map[i] for i in incoming_ids]


if __name__ == "__main__":
    main()
