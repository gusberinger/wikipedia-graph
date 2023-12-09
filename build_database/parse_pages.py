import gzip
import pickle
import re
from tqdm import tqdm
from constants import PAGES_SQL_FILEPATH, PAGES_PARSED_FILEPATH
from multiprocessing import Pool, cpu_count
import itertools

# the partial match doesn't get data but it a simple
# way to ensure that if we don't match the main regex
# it is because of an error in the main expression
PAGE_PARTIAL_MATCH = re.compile(r"\d+,0")

PAGE_REGEX = re.compile(
    r"(\d+),0,'(.*)',([01]),[01],0\.\d+,'\d+','\d+',\d+,\d+,'wikitext',NULL"
)


def process_large_line(large_line: str) -> list[tuple[int, str, bool]]:
    if not large_line.startswith("INSERT INTO `page` VALUES ("):
        return []
    large_line = large_line.replace("INSERT INTO `page` VALUES (", "")
    lines = large_line.replace("),(", "\n").splitlines()
    batch = []
    for line in lines:
        if not re.match(PAGE_PARTIAL_MATCH, line):
            continue
        if line.startswith("28644448"):
            # newline character breaks the script so we need to add it manually
            batch.append((28644448, r"\n", True))
            continue

        if line.startswith("71701640"):
            batch.append((71701640, "104-2,3,(6),(7),11", True))
            continue

        page_info = re.match(PAGE_REGEX, line)
        if not page_info:
            raise ValueError(f"Could not parse line: {line}")

        page_id, title, is_redirect = page_info.groups()
        batch.append((int(page_id), title, is_redirect == "1"))

    return batch


def process_lines(lines):
    links = []
    for large_line in lines:
        links.extend(process_large_line(large_line))
    return links


def main():
    page_info: list[tuple[int, str, bool]] = []
    num_processes = cpu_count()  # Use the number of available CPU cores
    chunk_size = 100
    with gzip.open(PAGES_SQL_FILEPATH, "rt") as f:
        with Pool(num_processes) as pool:
            for links in tqdm(
                pool.imap(process_lines, itertools.batched(f, chunk_size)),
                total=6938 // chunk_size,
                desc="Parsing pages file",
            ):
                page_info.extend(links)

        with PAGES_PARSED_FILEPATH.open("wb") as f:
            pickle.dump(page_info, f)

    # avoid duplicate titles
    titles = {title for _, title, _ in page_info}
    assert len(titles) == len(page_info)


if __name__ == "__main__":
    main()
