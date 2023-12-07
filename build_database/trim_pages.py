# if [ ! -f pages.txt.gz ]; then
#   echo
#   echo "[INFO] Trimming pages file"

#   # Unzip
#   # Remove all lines that don't start with INSERT INTO...
#   # Split into individual records
#   # Only keep records in namespace 0
#   # Replace namespace with a tab
#   # Splice out the page title and whether or not the page is a redirect
#   # Zip into output file
#   time pigz -dc $PAGES_FILENAME \
#     | sed -n 's/^INSERT INTO `page` VALUES (//p' \
#     | sed -e 's/),(/\'$'\n/g' \
#     | egrep "^[0-9]+,0," \
#     | sed -e $"s/,0,'/\t/" \
#     | sed -e $"s/',[^,]*,\([01]\).*/\t\1/" \
#     | pigz --fast > pages.txt.gz.tmp
#   mv pages.txt.gz.tmp pages.txt.gz
# else
#   echo "[WARN] Already trimmed pages file"
# fi
import gzip

from tqdm import tqdm
from constants import PAGES_FILEPATH, PAGES_TRIMMED_FILEPATH

def main():
    new_lines = []
    with gzip.open(PAGES_FILEPATH, "rt") as f:
        with tqdm(desc="Trimming pages file", total=6938) as pbar-d:
            for line in f:
                if line.startswith("INSERT INTO `page` VALUES ("):
                    line = line[27:-3]
                    line = line.replace("),(", "\n")
                    line = line.replace("',", "\t")
                    line = line.replace("'", "")
                    new_lines.append(line)
                pbar.update(1)

if __name__ == "__main__":
    main()