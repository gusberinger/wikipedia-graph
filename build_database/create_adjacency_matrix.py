import itertools
import pickle
from tqdm import tqdm
from constants import (
    LINKS_PARSED_FOLDER,
    PAGES_PRUNED_FILEPATH,
    TMP_FOLDER,
    WIKI_GRAPH_FILEPATH,
)
import scipy.sparse as sp
import numpy as np

link_csr_folder = TMP_FOLDER / "link_matrices"
link_csr_folder.mkdir(exist_ok=True)


def main():
    with open(PAGES_PRUNED_FILEPATH, "rb") as f:
        pages = pickle.load(f)
    main_page_ids = {
        page_id for page_id, _title, is_redirect in pages if not is_redirect
    }
    page_to_to_idx = {page_id: i for i, page_id in enumerate(main_page_ids)}
    # save memory
    del pages
    del main_page_ids
    size = len(page_to_to_idx)

    # matrix = sp.csr_matrix((size, size), dtype=int)
    link_files = list(LINKS_PARSED_FOLDER.glob("*.pickle"))
    for i, link_file in enumerate(
        tqdm(link_files, desc="Creating adjacency matrices from edge lists")
    ):
        with open(link_file, "rb") as f:
            links = pickle.load(f)
            rows = []
            cols = []
            for link in links:
                if link[0] in page_to_to_idx and link[1] in page_to_to_idx:
                    rows.append(page_to_to_idx[link[0]])
                    cols.append(page_to_to_idx[link[1]])

            coo_matrix = sp.coo_matrix(
                (np.ones(len(rows)), (rows, cols)), shape=(size, size)
            )
            csr_matrix = coo_matrix.tocsr()
            with open(link_csr_folder / f"{i}.npz", "wb") as f:
                sp.save_npz(f, csr_matrix)

    # combine all the matrices
    link_matrix_files = list(link_csr_folder.glob("*.npz"))
    matrix = sp.csr_matrix((size, size), dtype=int)
    for link_matrix_file in tqdm(
        link_matrix_files, desc="Combining adjacency matrices"
    ):
        with open(link_matrix_file, "rb") as f:
            matrix += sp.load_npz(f)

    with open(WIKI_GRAPH_FILEPATH, "wb") as f:
        sp.save_npz(f, matrix)


if __name__ == "__main__":
    main()
