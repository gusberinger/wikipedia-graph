from pathlib import Path
import requests
from tqdm import tqdm
from .constants import REDIRECTS_SQL_FILEPATH, LINKS_SQL_FILEPATH, PAGES_SQL_FILEPATH


def main(*, replace_existing: bool = False):
    base_url = "https://dumps.wikimedia.org/enwiki/latest/"
    files = [
        REDIRECTS_SQL_FILEPATH,
        PAGES_SQL_FILEPATH,
        LINKS_SQL_FILEPATH,
    ]
    for path in files:
        if not replace_existing and path.exists():
            continue
        url = base_url + path.name
        response = requests.get(url, stream=True)
        with tqdm(
            total=int(response.headers["Content-Length"]),
            desc=f"Downloading {path.name}",
        ) as pbar:
            with path.open("wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)
                    pbar.update(len(chunk))


if __name__ == "__main__":
    main()
