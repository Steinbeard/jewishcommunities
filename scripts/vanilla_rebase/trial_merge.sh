#!/bin/sh
# Trial three-way merge of the mod's whole-file overrides: ours = mod, base = 1.20.1, theirs = 1.21.
# Writes merged results to $OUT (not into the mod) and prints stats per file.
MOD="/c/Users/Daniel/Documents/Paradox Interactive/Crusader Kings III/mod/jewishcommunities-1.21-port"
BASE="/d/ck3-base-1.20/game"
NEW="/e/Program Files (x86)/Steam/steamapps/common/Crusader Kings III/game"
OUT="$1"
mkdir -p "$OUT"
shift
for f in "$@"; do
  o="$OUT/$(echo "$f" | tr '/' '_')"
  # normalise line endings so CRLF/LF differences do not count as edits
  tr -d '\r' < "$MOD/$f" > "$o.ours"; tr -d '\r' < "$BASE/$f" > "$o.base"; tr -d '\r' < "$NEW/$f" > "$o.theirs"
  ours=$(diff "$o.base" "$o.ours" | grep -c '^[<>]')
  theirs=$(diff "$o.base" "$o.theirs" | grep -c '^[<>]')
  cp "$o.ours" "$o.merged"
  git merge-file -L mod -L base-1.20 -L game-1.21 "$o.merged" "$o.base" "$o.theirs"
  conflicts=$?
  printf "%-62s our-edits=%-5s game-changes=%-5s conflicts=%s\n" "$f" "$ours" "$theirs" "$conflicts"
done
