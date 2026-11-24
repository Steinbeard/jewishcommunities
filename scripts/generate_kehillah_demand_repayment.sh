#!/bin/sh
# Generate the Kehillah Demand Repayment interaction from vanilla 1.21's own text.
G="/e/Program Files (x86)/Steam/steamapps/common/Crusader Kings III/game"
M="/c/Users/Daniel/Documents/Paradox Interactive/Crusader Kings III/mod/jewishcommunities"
OUT="$M/common/character_interactions/kehillah_demand_repayment_interactions.txt"
SRC="$G/common/character_interactions/11_gdp_merchant_interactions.txt"
{
printf '\357\273\277'
cat <<'HDR'
# =====================================================================
# DEMAND REPAYMENT for Kehillah lenders (2026-11-20).
# GENERATED from vanilla 1.21's demand_repayment_interaction
# (common/character_interactions/11_gdp_merchant_interactions.txt) with
# exactly three changes, so it behaves and reads like vanilla's:
#   1. key: kehillah_demand_repayment_interaction (and its self-reference);
#   2. is_available: government_is_kehillah instead of government_is_merchant
#      (that flag would switch on the whole merchant-republic code path);
#   3. ai_frequency = 24 instead of vanilla's per-tier block (county = 60).
# Loc, toasts, refusal penalties and AI acceptance are vanilla's own.
# Re-generate it when CK3 changes the vanilla interaction:
#   sh scripts/generate_kehillah_demand_repayment.sh (docs/spec/2026-11-19-trade-dlc-lending-goods-and-districts.md, section 6).
# =====================================================================

HDR
awk 'NR>=3304' "$SRC" | awk '
  BEGIN { d = 0; started = 0; skip = 0 }
  {
    line = $0
    if (!started) { if (line ~ /^demand_repayment_interaction = \{/) started = 1; else next }
    if (line ~ /^\tai_frequency_by_tier = \{/) { skip = 1; print "\tai_frequency = 24"; }
    if (skip) { if (line ~ /^\t\}/) { skip = 0 } ; next }
    sub(/^demand_repayment_interaction = \{/, "kehillah_demand_repayment_interaction = {", line)
    sub(/interaction = demand_repayment_interaction$/, "interaction = kehillah_demand_repayment_interaction", line)
    sub(/government_has_flag = government_is_merchant/, "government_has_flag = government_is_kehillah", line)
    print line
    n = split(line, ch, "")
    for (i = 1; i <= n; i++) { if (ch[i] == "{") d++; else if (ch[i] == "}") d-- }
    if (d == 0) exit
  }'
} > "$OUT"
wc -l "$OUT"
grep -n "kehillah_demand_repayment_interaction\|government_is_\|ai_frequency" "$OUT"
