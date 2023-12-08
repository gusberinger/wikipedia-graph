import gzip
import pickle
import re
from tqdm import tqdm
from constants import PAGES_FILEPATH, PAGES_TRIMMED_FILEPATH
from multiprocessing import Pool, cpu_count
import itertools


def process_large_line(large_line: str) -> list[tuple[int, str, bool]]:
    if not large_line.startswith("INSERT INTO `page` VALUES ("):
        return []
    large_line = large_line.replace("INSERT INTO `page` VALUES (", "")
    lines = large_line.replace("),(", "\n").splitlines()
    batch = []
    for line in lines:
        if not re.match(r"^[0-9]+,0,", line):
            continue

        # newline character breaks the script so we need to add it manually
        if line.startswith("28644448"):
            batch.append((28644448, r"\n", True))
            continue

        if line.startswith("71701640"):
            batch.append((71701640, "104-2,3,(6),(7),11", True))
            continue

        line = line.replace(",0,'", "\t")
        line = re.sub(r"',[^,]*,([01]).*", r"\t\1", line)
        page_id, title, is_redirect = line.split("\t")
        batch.append((int(page_id), title, bool(int(is_redirect))))

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
    with gzip.open(PAGES_FILEPATH, "rt") as f:
        with Pool(num_processes) as pool:
            for links in tqdm(
                enumerate(pool.imap(process_lines, itertools.batched(f, chunk_size))),
                total=6938 // chunk_size,
                desc="Trimming links file",
            ):
                page_info.extend(links)

        with PAGES_TRIMMED_FILEPATH.open("wb") as f:
            pickle.dump(page_info, f)


if __name__ == "__main__":
    main()
