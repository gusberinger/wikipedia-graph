import gzip
import itertools
import pickle
import re
from tqdm import tqdm
from constants import LINKS_SQL_FILEPATH, LINKS_PARSED_FOLDER
from multiprocessing import Pool, cpu_count

LINKS_REGEX = re.compile(r"(\d+),0,'(.+?)',0,(.*?)$")


def process_line(large_line: str) -> list[tuple[int, str, int]]:
    if not large_line.startswith("INSERT INTO `pagelinks` VALUES ("):
        return []
    large_line = large_line.replace("INSERT INTO `pagelinks` VALUES (", "")
    lines = large_line.replace("),(", "\n").splitlines()
    batch = []
    for line in lines:
        if line.endswith(");"):
            line = line[:-2]
        if match := re.match(LINKS_REGEX, line):
            from_id, title, target_id_match = match.groups()
            target_id = None if "NULL" in target_id_match else int(target_id_match)

            # print(f"{line=} {from_id=} {title=} {target_id=}")
            batch.append((int(from_id), title, target_id))
    return batch


def save_batch(batch: list[tuple[int, str, int]], batch_id: int):
    with (LINKS_PARSED_FOLDER / f"{batch_id:03}.pickle").open("wb") as f:
        pickle.dump(batch, f)


def process_lines(lines):
    links = []
    for large_line in lines:
        links.extend(process_line(large_line))
    return links


def main():
    with gzip.open(LINKS_SQL_FILEPATH, "rt") as f:
        chunk_size = 100
        num_processes = cpu_count()  # Use the number of available CPU cores
        with Pool(num_processes) as pool:
            for i, links in tqdm(
                enumerate(pool.imap(process_lines, itertools.batched(f, chunk_size))),
                total=67856 // chunk_size,
                desc="Trimming links file",
            ):
                print(len(links), i)
                save_batch(links, i)


if __name__ == "__main__":
    main()
