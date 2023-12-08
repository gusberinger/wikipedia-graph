import gzip
import pickle
import re
from tqdm import tqdm
from constants import PAGES_FILEPATH, PAGES_TRIMMED_FILEPATH


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


def main():
    if PAGES_TRIMMED_FILEPATH.exists():
        print("Pages file already trimmed")
        return

    page_info: list[tuple[int, str, bool]] = []
    with gzip.open(PAGES_FILEPATH, "rt") as f:
        for large_line in tqdm(f, total=6938, desc="Trimming pages file"):
            page_info.extend(process_large_line(large_line))

    with PAGES_TRIMMED_FILEPATH.open("wb") as f:
        pickle.dump(page_info, f)

    PAGES_FILEPATH.unlink()


if __name__ == "__main__":
    main()
