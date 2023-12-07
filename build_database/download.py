# from

from pathlib import Path
import requests
from tqdm import tqdm
from constants import REDIRECTS_FILEPATH, LINKS_FILEPATH, PAGES_FILEPATH


def main(*, replace_existing: bool = False):
    base_url = "https://dumps.wikimedia.org/enwiki/latest/"
    files: list[tuple[Path, str]] = [
        (REDIRECTS_FILEPATH, "enwiki-latest-redirect.sql.gz"),
        (LINKS_FILEPATH, "enwiki-latest-pagelinks.sql.gz"),
        (PAGES_FILEPATH, "enwiki-latest-page.sql.gz"),
    ]
    for path, download_name in files:
        if not replace_existing and path.exists():
            continue
        url = base_url + download_name
        response = requests.get(url, stream=True)
        with tqdm(total=int(response.headers["Content-Length"])) as pbar:
            pbar.set_description(f"Downloading {download_name}")
            with path.open("wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)
                    pbar.update(len(chunk))

if __name__ == "__main__":
    main()
