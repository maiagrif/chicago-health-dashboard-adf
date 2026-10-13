import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


PROJECT_DIR = Path(__file__).resolve().parent
TRACTS_PATH = PROJECT_DIR / "data" / "processed" / "tracts.csv"
BOUNDARIES_PATH = PROJECT_DIR / "data" / "processed" / "cook_county_tracts.geojson"
THEME_COLUMNS = [
    "svi_theme1_percentile",
    "svi_theme2_percentile",
    "svi_theme3_percentile",
    "svi_theme4_percentile",
]
MEASURE_LABELS = {
    "access2": "No health insurance",
    "arthritis": "Arthritis",
    "binge": "Binge drinking",
    "bphigh": "High blood pressure",
    "bpmed": "Taking blood pressure medication",
    "cancer": "Cancer history",
    "casthma": "Current asthma",
    "chd": "Coronary heart disease",
    "checkup": "Routine checkup",
    "cholscreen": "Cholesterol screening",
    "colon_screen": "Colorectal cancer screening",
    "copd": "COPD",
    "csmoking": "Current smoking",
    "dental": "Dental visit",
    "depression": "Depression",
    "diabetes": "Diabetes prevalence",
    "ghlth": "Fair or poor general health",
    "highchol": "High cholesterol",
    "lpa": "No leisure-time physical activity",
    "mammouse": "Mammography",
    "mhlth": "Frequent mental distress",
    "obesity": "Obesity",
    "phlth": "Frequent physical distress",
    "sleep": "Short sleep duration",
    "stroke": "Stroke",
    "teethlost": "All teeth lost",
    "hearing": "Hearing disability",
    "vision": "Vision disability",
    "cognition": "Cognitive disability",
    "mobility": "Mobility disability",
    "selfcare": "Self-care disability",
    "indeplive": "Independent-living disability",
    "disability": "Any disability",
    "loneliness": "Feelings of loneliness",
    "foodstamp": "Receipt of food stamps",
    "foodinsecu": "Food insecurity",
    "housinsecu": "Housing insecurity",
    "shututility": "Threat of utility shutoff",
    "lacktrpt": "Lack of transportation",
    "emotionspt": "Lack of emotional support",
}
MEASURE_DESCRIPTIONS = {
    "access2": "Estimated share of adults without health insurance.",
    "arthritis": "Estimated share of adults who report having arthritis.",
    "binge": "Estimated share of adults reporting binge drinking.",
    "bphigh": "Estimated share of adults who have been told they have high blood pressure.",
    "bpmed": "Estimated share of adults who report taking medicine for high blood pressure.",
    "cancer": "Estimated share of adults who report having had cancer, excluding skin cancer.",
    "casthma": "Estimated share of adults who currently have asthma.",
    "chd": "Estimated share of adults who report coronary heart disease.",
    "checkup": "Estimated share of adults who had a routine checkup in the past year.",
    "cholscreen": "Estimated share of adults who report having had a cholesterol screening.",
    "colon_screen": "Estimated share of adults who report being up to date with colorectal cancer screening.",
    "copd": "Estimated share of adults who report COPD.",
    "csmoking": "Estimated share of adults who currently smoke.",
    "dental": "Estimated share of adults who visited a dentist or dental clinic in the past year.",
    "depression": "Estimated share of adults who report having a depressive disorder.",
    "diabetes": "Estimated share of adults who report having diabetes, excluding diabetes during pregnancy.",
    "ghlth": "Estimated share of adults who describe their general health as fair or poor.",
    "highchol": "Estimated share of adults who report high cholesterol.",
    "lpa": "Estimated share of adults who report no leisure-time physical activity.",
    "mammouse": "Estimated share of women in the measure's eligible age group who report a recent mammogram.",
    "mhlth": "Estimated share of adults reporting frequent mental distress.",
    "obesity": "Estimated share of adults classified as having obesity based on height and weight.",
    "phlth": "Estimated share of adults reporting frequent physical distress.",
    "sleep": "Estimated share of adults who usually sleep fewer than seven hours in a 24-hour period.",
    "stroke": "Estimated share of adults who report having had a stroke.",
    "teethlost": "Estimated share of adults aged 65 and older who report having lost all natural teeth.",
    "hearing": "Estimated share of adults with a hearing disability.",
    "vision": "Estimated share of adults with a vision disability.",
    "cognition": "Estimated share of adults with a cognitive disability.",
    "mobility": "Estimated share of adults with a mobility disability.",
    "selfcare": "Estimated share of adults with a self-care disability.",
    "indeplive": "Estimated share of adults with an independent-living disability.",
    "disability": "Estimated share of adults reporting at least one disability.",
    "loneliness": "Estimated share of adults reporting feelings of loneliness.",
    "foodstamp": "Estimated share of adults living in households that received food stamps in the past year.",
    "foodinsecu": "Estimated share of adults living in households with food insecurity in the past year.",
    "housinsecu": "Estimated share of adults living in households with housing insecurity in the past year.",
    "shututility": "Estimated share of adults reporting a threat of utility shutoff in the past year.",
    "lacktrpt": "Estimated share of adults who needed transportation for everyday activities but could not get it in the past year.",
    "emotionspt": "Estimated share of adults who needed emotional support but did not get enough in the past year.",
}
THEME_DESCRIPTIONS = {
    "Socioeconomic vulnerability": "Ranks community conditions such as poverty, unemployment, education, and health insurance.",
    "Household characteristics": "Ranks conditions related to age, disability, household structure, and language.",
    "Racial and ethnic minority status": "Ranks the share of residents who identify with racial or ethnic minority groups. This reflects structural conditions, not an inherent health risk.",
    "Housing and transportation": "Ranks housing and transportation conditions such as crowding, group quarters, and access to a vehicle.",
}


@st.cache_data
def load_data():
    if not TRACTS_PATH.exists() or not BOUNDARIES_PATH.exists():
        return None, None

    tracts = pd.read_csv(TRACTS_PATH, dtype={"GEOID": "string"})
    boundaries = json.loads(BOUNDARIES_PATH.read_text(encoding="utf-8"))
    return tracts, boundaries


st.set_page_config(page_title="Cook County Health Priorities", layout="wide")
st.title("Cook County Priorities")
st.caption("CDC PLACES 2025 and CDC/ATSDR SVI 2022 | Census tract view")

tracts, boundaries = load_data()
if tracts is None:
    st.error("Processed data files are missing. Run notebooks/analysis.ipynb first.")
    st.stop()

measure_columns = [
    column for column in tracts.columns if column.endswith("_prevalence_pct")
]
measure_choices = {
    MEASURE_LABELS.get(
        column.removesuffix("_prevalence_pct"),
        column.removesuffix("_prevalence_pct").replace("_", " ").title(),
    ): column
    for column in measure_columns
}
measure_labels = list(measure_choices)
default_measure = measure_labels.index("Diabetes prevalence")
svi_default_cutoff = float(tracts["svi_overall_percentile"].quantile(0.75))

with st.expander("How to read this page", expanded=True):
    st.markdown(
        "**Each row or map area is one census tract.** Percentages are CDC estimates for adults in that tract, "
        "not a count of people or a diagnosis for any individual."
    )
    st.markdown(
        "**Overall SVI** is a relative social vulnerability ranking from 0 to 1. Higher values mean a tract is "
        "ranked as more socially vulnerable. For example, 0.84 is about the 84th percentile among Illinois tracts; "
        "it does not mean that 84% of residents are vulnerable."
    )
    st.markdown(
        "**Candidate priority tracts** meet both conditions: diabetes prevalence is in the highest quarter of the "
        "matched Cook County tracts, and overall SVI is at or above the selected cutoff. These are places to "
        "consider for discussion, not a final outreach decision."
    )
    st.markdown(
        "**Scatter plot:** one dot is a tract; farther right means a higher SVI rank, and higher up means a "
        "higher value for the selected health measure. Highlighted dots remain diabetes-based candidates even "
        "when another measure is selected. Association does not show cause and effect."
    )
    st.markdown(
        "**Map:** fill color shows the selected health measure; outlined areas are candidate priority tracts. "
        "The starting SVI cutoff is the 75th percentile within the matched Cook County tracts."
    )

with st.sidebar:
    st.header("Choose a view")
    svi_cutoff = st.slider(
        "Minimum overall SVI score",
        min_value=0.0,
        max_value=1.0,
        value=svi_default_cutoff,
        step=0.01,
        format="%.2f",
        help=(
            "SVI is scored from 0 to 1; higher means more vulnerability. The starting value is the 75th-percentile "
            "score among matched Cook County tracts. Lowering it includes more tracts."
        ),
    )
    selected_measure = st.selectbox(
        "Health measure",
        measure_labels,
        index=default_measure,
        help="Choose an estimated adult health measure to show in the table, scatter plot, and map.",
    )

measure_column = measure_choices[selected_measure]
diabetes_cutoff = tracts["diabetes_prevalence_pct"].quantile(0.75)
candidate_mask = (
    tracts["diabetes_prevalence_pct"].ge(diabetes_cutoff)
    & tracts["svi_overall_percentile"].ge(svi_cutoff)
)
candidates = tracts.loc[candidate_mask].copy()

metric_columns = st.columns(3)
metric_columns[0].metric(
    "Tracts with both datasets",
    f"{len(tracts):,}",
    help="Cook County tracts with both a PLACES health estimate and SVI scores.",
)
metric_columns[1].metric(
    "Candidate priority tracts",
    f"{len(candidates):,}",
    help="Tracts meeting both the diabetes top-quarter rule and the selected SVI cutoff.",
)
metric_columns[2].metric(
    "Diabetes top-quarter threshold",
    f"{diabetes_cutoff:.1f}%",
    help="At or above this estimated diabetes prevalence, a tract is in the highest quarter of matched Cook County tracts.",
)

st.subheader("Priority tract table")
st.caption(
    "Sorted by the selected health measure. Select a column heading or hover over it for a definition. "
    "Changing the chart measure does not change the diabetes-based candidate rule."
)
candidate_table = candidates.sort_values(
    [measure_column, "svi_overall_percentile"], ascending=False
)
table_columns = [
    "GEOID",
    "county_name",
    measure_column,
    "svi_overall_percentile",
    *THEME_COLUMNS,
]
display_table = candidate_table[table_columns].rename(
    columns={
        "GEOID": "Census tract ID",
        "county_name": "County",
        measure_column: selected_measure,
        "svi_overall_percentile": "Overall SVI percentile",
        "svi_theme1_percentile": "Socioeconomic vulnerability",
        "svi_theme2_percentile": "Household characteristics",
        "svi_theme3_percentile": "Racial and ethnic minority status",
        "svi_theme4_percentile": "Housing and transportation",
    }
)
st.dataframe(
    display_table,
    hide_index=True,
    width="stretch",
    column_config={
        "Census tract ID": st.column_config.TextColumn(
            help="An 11-digit Census identifier for a small geographic area. It is not a person-level ID."
        ),
        "County": st.column_config.TextColumn(help="County name for the census tract."),
        selected_measure: st.column_config.NumberColumn(
            help=MEASURE_DESCRIPTIONS.get(
                measure_column.removesuffix("_prevalence_pct"),
                "Estimated percentage of adults in the census tract.",
            ),
            format="%.1f",
        ),
        "Overall SVI percentile": st.column_config.NumberColumn(
            help="Overall social vulnerability rank, from 0 (lower relative vulnerability) to 1 (higher relative vulnerability).",
            format="%.3f",
        ),
        **{
            theme_name: st.column_config.NumberColumn(help=description, format="%.3f")
            for theme_name, description in THEME_DESCRIPTIONS.items()
        },
    },
)
st.download_button(
    "Download candidate tracts as CSV",
    data=display_table.to_csv(index=False).encode("utf-8"),
    file_name="cook_county_priority_tracts.csv",
    mime="text/csv",
)

st.subheader(f"{selected_measure} and social vulnerability")
st.caption(
    MEASURE_DESCRIPTIONS.get(
        measure_column.removesuffix("_prevalence_pct"),
        "Estimated percentage of adults in the census tract.",
    )
    + " Each point represents one tract. Hover over a point for its value and candidate status."
)
scatter_data = tracts.copy()
scatter_data["priority_candidate"] = candidate_mask.to_numpy()
scatter_data["candidate_label"] = scatter_data["priority_candidate"].map(
    {True: "Candidate priority tract", False: "Not flagged by candidate rule"}
)
scatter = px.scatter(
    scatter_data,
    x="svi_overall_percentile",
    y=measure_column,
    color="candidate_label",
    hover_name="GEOID",
    hover_data={
        measure_column: ":.1f",
        "svi_overall_percentile": ":.3f",
        "candidate_label": True,
        "priority_candidate": False,
    },
    labels={
        "svi_overall_percentile": "Overall SVI percentile",
        measure_column: f"{selected_measure} (estimated percent)",
        "candidate_label": "Candidate status",
        "priority_candidate": "Candidate priority tract",
    },
    color_discrete_map={
        "Candidate priority tract": "#C65D49",
        "Not flagged by candidate rule": "#527D78",
    },
)
scatter.update_layout(legend_title_text="")
st.plotly_chart(scatter, width="stretch")

st.subheader("Tract map")
st.caption(
    "Fill color shows the estimate for the selected health measure; outlined areas meet the diabetes-and-SVI candidate rule. "
    "Hover over a tract for its estimate and SVI rank."
)
boundary_ids = [feature["properties"]["GEOID"] for feature in boundaries["features"]]
tract_lookup = tracts.set_index("GEOID")
map_values = [tract_lookup[measure_column].get(geoid) for geoid in boundary_ids]
candidate_ids = set(candidates["GEOID"].tolist())
map_customdata = [
    [
        tract_lookup["svi_overall_percentile"].get(geoid),
        "Candidate" if geoid in candidate_ids else "Not flagged",
    ]
    if geoid in tract_lookup.index
    else [None, "No matching health estimate"]
    for geoid in boundary_ids
]
candidate_features = [
    feature
    for feature in boundaries["features"]
    if feature["properties"]["GEOID"] in candidate_ids
]
candidate_geojson = {"type": "FeatureCollection", "features": candidate_features}

map_figure = go.Figure(
    go.Choroplethmap(
        geojson=boundaries,
        featureidkey="properties.GEOID",
        locations=boundary_ids,
        z=map_values,
        colorscale=[
            [0.0, "#E8EFEC"],
            [0.3, "#BFD3C9"],
            [0.6, "#83B2A4"],
            [0.8, "#D8AE62"],
            [1.0, "#C65D49"],
        ],
        marker={"line": {"color": "white", "width": 0.25}},
        colorbar={"title": "Estimated percent"},
        customdata=map_customdata,
        hovertemplate=(
            "Census tract %{location}<br>Estimated percent: %{z:.1f}%<br>"
            "Overall SVI: %{customdata[0]:.3f}<br>Status: %{customdata[1]}<extra></extra>"
        ),
    )
)
if candidate_ids:
    map_figure.add_trace(
        go.Choroplethmap(
            geojson=candidate_geojson,
            featureidkey="properties.GEOID",
            locations=sorted(candidate_ids),
            z=[1] * len(candidate_ids),
            colorscale=[[0, "rgba(0,0,0,0)"], [1, "rgba(0,0,0,0)"]],
            zmin=0,
            zmax=1,
            marker={"line": {"color": "#74392F", "width": 1.5}, "opacity": 0.01},
            showscale=False,
            hoverinfo="skip",
        )
    )
map_figure.update_layout(
    map={"style": "carto-positron", "center": {"lat": 41.83, "lon": -87.75}, "zoom": 7.2},
    margin={"l": 0, "r": 0, "t": 0, "b": 0},
    height=560,
)
st.plotly_chart(map_figure, width="stretch")

st.info(
    "Sources: CDC PLACES 2025 and CDC/ATSDR SVI 2022. PLACES estimates are model-based and partly use demographic inputs, "
    "so some association with SVI is built in. This is an ecological tract-level analysis, not an individual-level comparison. "
    "The releases have different reference periods. SVI rankings are relative to Illinois tracts. Candidate tracts are a screening aid, not a final outreach decision. "
    "[CDC PLACES methodology](https://www.cdc.gov/places/methodology/index.html) · "
    "[SVI data and documentation](https://www.atsdr.cdc.gov/place-health/php/svi/svi-data-documentation-download.html)"
)