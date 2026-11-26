"use strict";
(() => {
  const normalize = value => value.normalize("NFKD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
  const search = document.querySelector("#wiki-search");
  const results = document.querySelector("#search-results");
  const status = document.querySelector("#search-status");
  const index = JSON.parse(document.querySelector("#wiki-index").textContent).map(entry => ({...entry, haystack: normalize(entry.title + " " + entry.summary + " " + entry.text)}));
  search.addEventListener("input", () => {
    results.replaceChildren();
    const terms = normalize(search.value.trim()).split(/\s+/).filter(Boolean);
    if (!terms.length) { status.textContent = ""; return; }
    const matches = index.filter(entry => terms.every(term => entry.haystack.includes(term)))
      .sort((a, b) => Number(terms.every(t => normalize(b.title).includes(t))) - Number(terms.every(t => normalize(a.title).includes(t))));
    status.textContent = matches.length ? `${matches.length} results; showing up to 12.` : "No results. Try a shorter name or a discipline.";
    matches.slice(0, 12).forEach(entry => {
      const link = document.createElement("a");
      link.href = entry.url;
      link.textContent = entry.title;
      const description = document.createElement("small");
      description.textContent = entry.summary;
      link.append(description);
      results.append(link);
    });
  });
  const filter = document.querySelector("#reference-filter");
  if (filter) {
    const rows = [...document.querySelectorAll("#reference-table tbody tr")];
    const update = () => {
      const terms = normalize(filter.value).split(/\s+/).filter(Boolean);
      let visible = 0;
      rows.forEach(row => {
        row.hidden = !terms.every(term => normalize(row.textContent).includes(term));
        if (!row.hidden) visible++;
      });
      document.querySelector("#filter-count").textContent = `${visible} of ${rows.length} entries`;
    };
    filter.addEventListener("input", update);
    update();
  }
})();
