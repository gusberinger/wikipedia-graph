from constants import REDIRECTS_TRIMMED_FILEPATH
import gzip


with gzip.open(REDIRECTS_TRIMMED_FILEPATH, "rb") as f:
    for i, line in enumerate(f):
        print(line)