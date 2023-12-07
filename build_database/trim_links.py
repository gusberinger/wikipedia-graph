import gzip
import pickle
import re
from tqdm import tqdm
from constants import LINKS_FILEPATH, LINKS_TRIMMED_FOLDER

LINKS_REGEX = re.compile(r"(\d+),0,'(.+?)',0,(.*?)$")

def main():

    with gzip.open(LINKS_FILEPATH, "rt") as f:
        links_batch: list[tuple[int, str, int]] = []
        links_batch_id = 0
        for large_line in tqdm(f, total=67856, desc="Trimming links file"):
            if not large_line.startswith("INSERT INTO `pagelinks` VALUES ("):
                continue
            large_line = large_line.replace("INSERT INTO `pagelinks` VALUES (", "")
            lines = large_line.replace("),(", "\n").splitlines()
            for line in lines:
                if match := re.match(LINKS_REGEX, line):
                    line = line.replace(",NULL);", "NULL")
                    if not line.strip().endswith("NULL"):
                        print(f"{line=}")
                    from_id, title, target_id_match = match.groups()
                    target_id = None if "NULL" in target_id_match else int(target_id_match)
                    links_batch.append((int(from_id), title, target_id))
                    
                    if len(links_batch) > 10 ** 6:
                        with (LINKS_TRIMMED_FOLDER / f"{links_batch_id:04}.pickle").open("wb") as f:
                            pickle.dump(links_batch, f)
                        links_batch = []
                        links_batch_id += 1
                
    with (LINKS_TRIMMED_FOLDER / f"{links_batch_id + 1:04}.pickle").open("wb") as f:
        pickle.dump(links_batch, f)

if __name__ == "__main__":
    main()