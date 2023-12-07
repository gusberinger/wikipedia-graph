import gzip
import pickle
import re
from tqdm import tqdm
from constants import PAGES_FILEPATH, PAGES_TRIMMED_FILEPATH

def main():
    page_info: list[tuple[int, str, bool]] = []
    with gzip.open(PAGES_FILEPATH, "rt") as f:
        for large_line in tqdm(f, total=6938, desc="Trimming pages file"):
            if not large_line.startswith("INSERT INTO `page` VALUES ("):
                continue
            large_line = large_line.replace("INSERT INTO `page` VALUES (", "")
            lines = large_line.replace("),(", "\n").splitlines()
            for line in lines:
                if not re.match(r"^[0-9]+,0,", line):
                    continue

                # newline character breaks the script so we need to add it manually
                if line.startswith("28644448"):
                    page_info.append((28644448, r"\n", True))
                    continue
                line = line.replace(",0,'", "\t")
                line = re.sub(r"',[^,]*,([01]).*", r"\t\1", line)
                page_id, title, is_redirect = line.split("\t")
                page_info.append((int(page_id), title, bool(int(is_redirect))))

    with PAGES_TRIMMED_FILEPATH.open("wb") as f:
        pickle.dump(page_info, f)

if __name__ == "__main__":
    main()