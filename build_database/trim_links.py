import gzip
import itertools
import pickle
import re
from tqdm import tqdm
from constants import LINKS_FILEPATH, LINKS_TRIMMED_FOLDER

LINKS_REGEX = re.compile(r"(\d+),0,'(.+?)',0,(.*?)$")

def process_line(large_line: str) -> list[tuple[int, str, int]]:
    if not large_line.startswith("INSERT INTO `pagelinks` VALUES ("):
        return []
    large_line = large_line.replace("INSERT INTO `pagelinks` VALUES (", "")
    lines = large_line.replace("),(", "\n").splitlines()
    batch = []
    for line in lines:
        if match := re.match(LINKS_REGEX, line):
            line = line.replace(",NULL);", "NULL")
            if not line.strip().endswith("NULL"):
                print(f"{line=}")
            from_id, title, target_id_match = match.groups()
            target_id = None if "NULL" in target_id_match else int(target_id_match)
            assert target_id is None
            batch.append((int(from_id), title, target_id))
    return batch

def save_batch(batch: list[tuple[int, str, int]], batch_id: int):
    with (LINKS_TRIMMED_FOLDER / f"{batch_id:04}.pickle").open("wb") as f:
        pickle.dump(batch, f)

def main():
    with gzip.open(LINKS_FILEPATH, "rt") as f:
        chunk_size = 100
        for i, lines in tqdm(enumerate(itertools.batched(f, chunk_size)), total=67856 // chunk_size, desc="Trimming links file"):
            links = []
            for large_line in lines:
                links.extend(process_line(large_line))
            save_batch(links, i)
            

if __name__ == "__main__":
    main()