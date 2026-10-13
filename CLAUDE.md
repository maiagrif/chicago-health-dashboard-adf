# Project Context

## Maia

Maia Griffith has an MPH in Biostatistics and Epidemiology from USC (2022) and a BS in Health and Human Physiology from the University of Iowa.

She was Software Developer at the University of Chicago Institute for Population and Precision Health from January 2023 to August 2026. She was front-end lead for eRMS, a React/TypeScript research-management platform with a Django/PostgreSQL backend, used by 50+ users across 5+ study sites, including the NIH CONNECT cancer study. She led full-stack participant-management, sample-tracking, payment, and automated-reporting features; owned 80% of front-end testing (Cypress and Selenium); trained 20+ clinical and research staff to 100% adoption; and mentored 15+ graduate students building All of Us cohorts with SQL, R, and Python/Jupyter.

Since August 2026, she has been Co-founder and Consulting Engineer at Panaxia Systems, commercializing eRMS through UChicago's Polsky Center. Other experience includes facilitating a Community Memorial Foundation youth-philanthropy program with a $30K fund, serving as a CASA court-appointed advocate, and an MPH practicum analyzing 25+ precision-medicine studies and leading a WCAG 2.1 AA accessibility migration.

Skills include Python, pandas, NumPy, SQL, R, PostgreSQL, React, TypeScript, Django, Git, Docker, AWS, SAS, and SPSS.

## Interview Goal

This is a one-day technical interview project for the selective 12-month UChicago Applied Data Fellowship (adf.uchicago.edu), which places early-career data professionals in local governments and nonprofits. The fellowship emphasizes statistical analysis, visualization, database engineering, ML, LLM integrations, and turning analysis into decisions ("math to mission"). Public-health infrastructure is a project area.

Maia cannot share eRMS code because it is in a licensing negotiation with the Polsky Center. This project demonstrates hands-on analysis and statistics, complementing a resume that reads primarily as software engineering. Be transparent about AI assistance. Maia's framing: "Claude Code did the mechanical work (loading, joins, plotting code). I set the rules in CLAUDE.md, made every analytical decision, and logged what I checked."

## Project Question

Which Cook County census tracts have both high diabetes prevalence and high social vulnerability, and where should a health department focus outreach first?

## Data Sources And Release Years

Join tabular data on the 11-character census tract GEOID/FIPS.

1. CDC PLACES census-tract data: diabetes prevalence, filtered to Cook County, Illinois (county FIPS 17031).
2. CDC/ATSDR Social Vulnerability Index (SVI), Illinois census tracts: overall percentile (`RPL_THEMES`) and four theme percentiles.
3. For the optional map, the Census Bureau cartographic-boundary shapefile for Illinois census tracts, using tract geography compatible with the selected data.

Source check performed 2026-10-12: CDC's current PLACES release notes identify the 2025 release. Diabetes is a BRFSS-based measure; the release uses 2023 BRFSS for most measures and 2019-2023 ACS data across geographic levels. PLACES estimates at tract level use 2020 Census block population geography. The CDC/ATSDR SVI download/documentation page identifies 2022 as the latest documented SVI vintage; the 2022 SVI is based on 2018-2022 ACS, and SVI percentiles rank tracts within a release year. The two releases are not year-matched, but their ACS periods overlap and both use 2020-era tract geography, making them a reasonable cross-sectional pairing with an explicit release-year/data-vintage caveat. Verify dataset metadata, variable names, and tract GEOIDs after download; do not imply the measures refer to exactly the same year.

Official source pages:

- PLACES release notes: https://www.cdc.gov/places/current-release-notes/index.html
- PLACES methodology: https://www.cdc.gov/places/methodology/index.html
- PLACES data portal: https://www.cdc.gov/places/tools/data-portal.html
- PLACES current 2025 release portal search: https://data.cdc.gov/browse?category=500+Cities+%26+Places&q=2025&sortBy=relevance&tags=places
- CDC/ATSDR SVI data and documentation: https://www.atsdr.cdc.gov/place-health/php/svi/svi-data-documentation-download.html
- Census Bureau cartographic boundary files (2019 and later): https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.html

Do not guess direct download URLs. Direct Maia to the official pages and describe the required selections and file types when a direct link is not verified. For PLACES, choose the 2025 census-tract dataset and CSV export. For SVI, choose year 2022, Illinois, census tracts, and the CSV table. For the map, choose the Illinois census-tract cartographic-boundary shapefile from an appropriate 2020-era geography. Save the downloaded originals under `data/raw/`; use clear local names such as `places_2025_census_tract.csv`, `svi_2022_illinois_tract.csv`, and the census boundary ZIP/shapefile files. Do not load or process data until Maia confirms the files are ready.

## Analysis

- Keep all analysis in `notebooks/analysis.ipynb`; the notebook must run top to bottom.
- Load, filter, and join the three tabular sources as appropriate. Report matched and unmatched tract counts.
- Explore distributions, correlations, summary statistics by SVI quartile, and data quality.
- Fit a simple linear regression of diabetes prevalence on the four SVI theme scores and report coefficients with 95% confidence intervals. Present the proposed model and analytical choices to Maia; Maia chooses the final model.
- Flag candidate priority tracts as the top quartile for both diabetes prevalence and overall SVI, but Maia must confirm this priority rule before it is applied or represented as final.
- Clearly state limitations: PLACES values are model-based estimates partly derived from demographic data, so some correlation with SVI is built in; the analysis is ecological and tract patterns do not describe individuals; data release/reference years differ.

## Dashboard

Build a one-page Streamlit app in `app.py` that reads `data/processed/tracts.csv`.

- Sidebar: SVI percentile cutoff slider and a health-measure selector.
- Priority table: sortable, with CSV download.
- Plotly scatter plot: diabetes prevalence against SVI percentile, highlighting priority tracts.
- Choropleth of Cook County tracts with priority tracts outlined. Build this last; if it is not working by mid-afternoon, drop it and keep the table and scatter plot usable.
- Short notes box with sources and limitations.
- No logins, multiple pages, or custom styling.
- Deploy to Streamlit Community Cloud from a public GitHub repository and test the live link.

## Repository Deliverables

- Public GitHub repository and README covering the question, data, main finding, limitations, what Maia would do next with a real partner, and how she used Claude Code.
- `notebooks/analysis.ipynb`
- `data/processed/tracts.csv`
- `app.py`
- `requirements.txt`
- `CLAUDE.md`
- `VERIFICATION.md`
- `MEMO.md`: Maia writes the half-page memo for a health-department program manager. Give feedback only; do not write or rewrite the memo.
- Live Streamlit link.

## Working Rules

- Never modify files in `data/raw/`. Write cleaned data to `data/processed/`.
- Treat tract codes (`GEOID`/FIPS) as 11-character strings, never numbers; preserve leading zeros.
- After every join, print row counts before and after and list unmatched tracts.
- Ask Maia before dropping rows, imputing values, changing the priority rule, or choosing a model. If missingness or a data-quality issue would require one of those choices, stop and ask.
- Keep analysis in `notebooks/analysis.ipynb`, running top to bottom.
- Keep code simple and commented enough for Maia to explain every line in the interview.
- Maintain `VERIFICATION.md`: one dated line for each check Maia made or correction to assistant output. When Maia corrects the assistant, add a dated line describing the correction. Do not claim Maia performed a check unless she did; distinguish assistant source checks from Maia verification.
- Do not fabricate findings, data checks, or deployment status.

## One-Day Schedule (About 8 Hours)

- 0:00-0:30: repository setup and `CLAUDE.md`
- 0:30-2:00: load, clean, and join in the notebook
- 2:00-3:00: explore and model in the notebook
- 3:00-5:00: build `app.py`, table and scatter first, then map
- 5:00-5:45: deploy and test the link
- 5:45-6:45: README and memo
- 6:45-8:00: rehearse a 3-minute walkthrough: live dashboard, notebook, then `CLAUDE.md` and `VERIFICATION.md`
