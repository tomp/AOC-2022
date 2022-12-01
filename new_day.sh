#!/bin/bash
# Create the directory for a new day's code.
#

usage () {
    echo "Usage: $0 <day>"
    echo "Create the directory for the given day."
    exit 0
}

error () {
    echo "Error: $*"
    exit 1
}

test -n "$1" || usage
DAY="$1"

dir="day${DAY}"
prog="$dir/day${DAY}.py"
infile="$dir/input.txt"
desc="$dir/day${DAY}.md"

mkdir -p "$dir" || error "Unable to create $dir"
echo "Created $dir"

test -f "$prog" || \
    sed -E 's!([dD][aA][yY]) N *$!\1 '$DAY'!' dayN.py > "$prog" || \
    error "Unable to install $prog"

chmod +x "$prog"
echo "Wrote $prog"

./download.py -d "$DAY" --outfile "$desc" || \
    error "Unable to download puzzle description"

./download.py -d "$DAY" --input --outfile "$infile" || \
    error "Unable to download input data"
echo "$infile has $(wc -l $infile | awk '{print $1}') lines"

git add "$prog" "$infile"

gvim "$prog" "$desc" "$infile"


