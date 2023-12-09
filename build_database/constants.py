from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
TMP_FOLDER = PROJECT_ROOT / "tmp"
DATA_FOLDER = PROJECT_ROOT / "data"
TMP_FOLDER.mkdir(exist_ok=True)
DATA_FOLDER.mkdir(exist_ok=True)

SHA1SUM_FILEPATH = TMP_FOLDER / "enwiki-latest-sha1sums.txt"

LINKS_SQL_FILEPATH = TMP_FOLDER / "enwiki-latest-pagelinks.sql.gz"
LINKS_PARSED_FOLDER = TMP_FOLDER / "parsed_links"
LINKS_PARSED_FOLDER.mkdir(exist_ok=True)

PAGES_SQL_FILEPATH = TMP_FOLDER / "enwiki-latest-page.sql.gz"
PAGES_PARSED_FILEPATH = PAGES_SQL_FILEPATH.with_suffix(".pickle")
PAGES_PRUNED_FILEPATH = TMP_FOLDER / "pages_pruned.pickle"

REDIRECTS_SQL_FILEPATH = TMP_FOLDER / "enwiki-latest-redirect.sql.gz"
REDIRECTS_PARSED_FILEPATH = REDIRECTS_SQL_FILEPATH.with_suffix(".pickle")
REDIRECTS_PRUNED_FILEPATH = TMP_FOLDER / "redirects_pruned.pickle"

WIKI_TITLE_TO_ID_FILEPATH = DATA_FOLDER / "wiki_title_to_id.pickle"
WIKI_ID_TO_TITLE_FILEPATH = DATA_FOLDER / "wiki_id_to_title.pickle"
