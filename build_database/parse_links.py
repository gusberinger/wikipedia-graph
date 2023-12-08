import gzip
import pickle
import re
from tqdm import tqdm
from constants import (
    LINKS_SQL_FILEPATH,
    PAGES_PRUNED_FILEPATH,
    REDIRECTS_PRUNED_FILEPATH,
)

LINKS_REGEX = re.compile(r"(\d+),0,'(.+?)',0,(.*?)$")


def main():
    with open(REDIRECTS_PRUNED_FILEPATH, "rb") as f:
        redirects = pickle.load(f)

    with open(PAGES_PRUNED_FILEPATH, "rb") as f:
        pages = pickle.load(f)

    titles_to_id_map = {
        title: page_id
        for page_id, title, _ in tqdm(pages, desc="Mapping titles to IDs")
    }

    def process_line(large_line: str) -> list[tuple[int, str, int]]:
        if not large_line.startswith("INSERT INTO `pagelinks` VALUES ("):
            return []
        large_line = large_line.replace("INSERT INTO `pagelinks` VALUES (", "")
        lines = large_line.replace("),(", "\n").splitlines()
        batch = []
        for line in lines:
            if line.endswith(");"):
                line = line[:-2]

            # print(line)
            if match := re.match(LINKS_REGEX, line):
                from_id, target_title, target_id_match = match.groups()

                # the target_id is sometimes NULL
                # we are unsure why this is the case
                # so we will just find it from the title
                target_id = None if "NULL" == target_id_match else int(target_id_match)
                if target_id is None and target_title in titles_to_id_map:
                    target_id = titles_to_id_map[target_title]

                if target_id is None:
                    continue

                if target_id in redirects:
                    target_id = redirects[target_id]

                batch.append((int(from_id), target_id))
        return batch

    links = []
    with gzip.open(LINKS_SQL_FILEPATH, "rt") as f:
        for large_line in tqdm(f, total=67856, desc="Trimming links file"):
            links.extend(process_line(large_line))


if __name__ == "__main__":
    main()
