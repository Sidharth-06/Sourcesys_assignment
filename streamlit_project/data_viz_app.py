from __future__ import annotations

from datetime import datetime, timedelta

import pandas as pd
import streamlit as st


st.set_page_config(page_title="Data Visualization Dashboard", page_icon="📊", layout="wide")

st.markdown(
    """
    <style>
      #MainMenu, footer, header { visibility: hidden; }
      .stApp {
        background:
          radial-gradient(circle at top left, rgba(59, 130, 246, 0.18), transparent 30%),
          radial-gradient(circle at top right, rgba(16, 185, 129, 0.14), transparent 28%),
          linear-gradient(180deg, #08111f 0%, #0d1728 55%, #08111f 100%);
        color: #e5eefb;
      }
      .block-container {
        padding-top: 1.4rem !important;
        padding-bottom: 2rem !important;
        max-width: 1280px;
      }
      .metric-card {
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 18px;
        padding: 1rem 1.1rem;
        background: rgba(9, 16, 29, 0.78);
        box-shadow: 0 18px 40px rgba(0, 0, 0, 0.22);
      }
      div[data-testid="stFileUploader"] {
        background: rgba(9, 16, 29, 0.78);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 16px;
        padding: 0.5rem 0.75rem;
      }
    </style>
    """,
    unsafe_allow_html=True,
)


def build_sample_data() -> pd.DataFrame:
    base_date = datetime.utcnow().date() - timedelta(days=13)
    records = []
    categories = ["North", "South", "East", "West"]
    products = ["Basic", "Pro", "Enterprise"]

    for day in range(14):
        for index, category in enumerate(categories):
            records.append(
                {
                    "date": base_date + timedelta(days=day),
                    "region": category,
                    "product": products[(day + index) % len(products)],
                    "sales": 1200 + day * 130 + index * 210,
                    "profit": 260 + day * 18 + index * 42,
                    "orders": 18 + day * 2 + index,
                }
            )

    return pd.DataFrame(records)


def load_data(uploaded_file) -> pd.DataFrame:
    if uploaded_file is None:
        return build_sample_data()

    if uploaded_file.name.lower().endswith(".csv"):
        return pd.read_csv(uploaded_file)

    return pd.read_excel(uploaded_file)


st.title("Data Visualization Dashboard")
st.caption("Upload a CSV or Excel file, or use the included sample dataset, then explore the data with Streamlit charts.")

with st.sidebar:
    st.header("Data Source")
    uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])
    use_sample = st.checkbox("Use sample dataset", value=uploaded_file is None)

    st.divider()
    st.header("Chart Options")
    max_rows = st.slider("Rows to display", min_value=50, max_value=5000, value=500, step=50)

if uploaded_file is not None and not use_sample:
    dataframe = load_data(uploaded_file)
else:
    dataframe = build_sample_data()

if dataframe.empty:
    st.warning("The selected dataset is empty.")
    st.stop()

dataframe = dataframe.head(max_rows).copy()

st.subheader("Preview")
st.dataframe(dataframe, use_container_width=True, height=260)

numeric_columns = list(dataframe.select_dtypes(include="number").columns)
date_columns = list(dataframe.select_dtypes(include=["datetime64[ns]", "datetime64[ns, UTC]"]).columns)
text_columns = [column for column in dataframe.columns if column not in numeric_columns and column not in date_columns]

if not numeric_columns:
    st.error("Please upload a dataset with at least one numeric column to chart.")
    st.stop()

if not date_columns:
    for column in dataframe.columns:
        if "date" in column.lower() or "time" in column.lower():
            try:
                dataframe[column] = pd.to_datetime(dataframe[column])
                date_columns.append(column)
                break
            except Exception:
                continue

top_left, top_middle, top_right = st.columns(3)
with top_left:
    st.markdown(
        "<div class='metric-card'><strong>Rows</strong><br>{}</div>".format(len(dataframe)),
        unsafe_allow_html=True,
    )
with top_middle:
    st.markdown(
        "<div class='metric-card'><strong>Columns</strong><br>{}</div>".format(len(dataframe.columns)),
        unsafe_allow_html=True,
    )
with top_right:
    st.markdown(
        "<div class='metric-card'><strong>Numeric Fields</strong><br>{}</div>".format(len(numeric_columns)),
        unsafe_allow_html=True,
    )

st.divider()

if date_columns:
    date_column = st.selectbox("Date column", options=date_columns, index=0)
    measure_column = st.selectbox("Measure column", options=numeric_columns, index=0)
    dated_frame = dataframe.copy()
    dated_frame[date_column] = pd.to_datetime(dated_frame[date_column])
    aggregated = (
        dated_frame.groupby(dated_frame[date_column].dt.date, as_index=False)[measure_column]
        .sum()
        .sort_values(by=date_column)
    )
    st.subheader("Trend Over Time")
    st.line_chart(aggregated.set_index(date_column)[measure_column])
else:
    st.info("No date column detected. Add a date/time field to enable a trend chart.")

first_numeric = numeric_columns[0]
second_numeric = numeric_columns[1] if len(numeric_columns) > 1 else numeric_columns[0]

left_panel, right_panel = st.columns(2)
with left_panel:
    st.subheader("Distribution")
    if text_columns:
        bar_data = dataframe.groupby(text_columns[0], dropna=False)[first_numeric].sum()
        st.bar_chart(bar_data)
    else:
        st.bar_chart(dataframe[[first_numeric]])

with right_panel:
    st.subheader("Relationship")
    scatter_source = dataframe[[first_numeric, second_numeric]].dropna()
    if len(scatter_source.columns) == 2:
        st.scatter_chart(scatter_source, x=first_numeric, y=second_numeric)
    else:
        st.info("Need at least two numeric columns for a scatter chart.")

st.subheader("Area View")
if date_columns:
    st.area_chart(aggregated.set_index(date_column)[measure_column])
else:
    st.area_chart(dataframe[numeric_columns])

st.subheader("Summary Statistics")
st.dataframe(dataframe[numeric_columns].describe().transpose(), use_container_width=True)
