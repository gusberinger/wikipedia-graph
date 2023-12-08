from tqdm import tqdm
import gzip
from constants import REDIRECTS_SQL_FILEPATH, REDIRECTS_PARSED_FILEPATH
import re
import pickle


def main():
    redirects: list[tuple[int, str]] = []
    with gzip.open(REDIRECTS_SQL_FILEPATH, "rt") as f:
        for large_line in tqdm(f, total=655, desc="Trimming redirects file"):
            if not large_line.startswith("INSERT INTO `redirect` VALUES ("):
                continue
            large_line = large_line.replace("INSERT INTO `redirect` VALUES (", "")
            lines = large_line.replace("),(", "\n").splitlines()
            for line in lines:
                if not re.match(r"^[0-9]+,0,", line):
                    continue
                line = line.replace(",0,'", "\t")
                line = line.split("','")[0]
                page_id, title = line.split("\t")
                redirects.append((int(page_id), title))

    with REDIRECTS_PARSED_FILEPATH.open("wb") as f:
        pickle.dump(redirects, f)


if __name__ == "__main__":
    main()
