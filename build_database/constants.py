from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
TMP_FOLDER = PROJECT_ROOT / "tmp"
TMP_FOLDER.mkdir(exist_ok=True)

SHA1SUM_FILEPATH = TMP_FOLDER / "enwiki-latest-sha1sums.txt"
REDIRECTS_FILEPATH = TMP_FOLDER / "enwiki-latest-redirect.sql.gz"
PAGES_FILEPATH = TMP_FOLDER / "enwiki-latest-page.sql.gz"
LINKS_FILEPATH = TMP_FOLDER / "enwiki-latest-pagelinks.sql.gz"