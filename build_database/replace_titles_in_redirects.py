from tqdm import tqdm
from constants import (
    PAGES_PARSED_FILEPATH,
    REDIRECTS_PARSED_FILEPATH,
    REDIRECTS_PRUNED_FILEPATH,
)
import pickle


def main():
    with open(PAGES_PARSED_FILEPATH, "rb") as f:
        pages = pickle.load(f)

    with open(REDIRECTS_PARSED_FILEPATH, "rb") as f:
        redirects = pickle.load(f)

    page_ids = {page_id for page_id, _, _ in pages}
    titles_to_id_map = {
        title: page_id
        for page_id, title, _ in tqdm(pages, desc="Mapping titles to IDs")
    }

    pruned_redirects = {}
    for source_id, target_title in tqdm(
        redirects, desc="Replacing titles with page IDs"
    ):
        # remove source_ids that are not namespace 0
        if source_id not in page_ids:
            continue

        # there are ~245 articles titles that aren't parsed correctly.
        # the number is low enough that we can just ignore them, but
        # we should probably fix this in the future
        if target_title not in titles_to_id_map:
            continue

        target_id = titles_to_id_map[target_title]
        pruned_redirects[source_id] = target_id

    # ensure that the target_page_id is not itself a redirect
    for source_page_id, target_page_id in tqdm(
        pruned_redirects.items(), desc="Resolving redirects"
    ):
        start_target_page_id = target_page_id
        redirected_count = 0
        while target_page_id in pruned_redirects:
            target_page_id = pruned_redirects[target_page_id]

            # check for infinite loops
            redirected_count += 1
            if target_page_id == start_target_page_id or redirected_count > 100:
                target_page_id = None

        if target_page_id is not None:
            pruned_redirects[source_page_id] = target_page_id

    with open(REDIRECTS_PRUNED_FILEPATH, "wb") as f:
        pickle.dump(pruned_redirects, f)


if __name__ == "__main__":
    main()
