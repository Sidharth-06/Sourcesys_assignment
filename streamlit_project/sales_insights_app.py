from __future__ import annotations

import re
from datetime import datetime, timedelta
from typing import Iterable, Optional

import pandas as pd
import streamlit as st


st.set_page_config(page_title="Sales Insights Studio", page_icon="📈", layout="wide")

st.markdown(
    """
    <style>
      #MainMenu, footer, header { visibility: hidden; }
      .stApp {
        background:
          radial-gradient(circle at top left, rgba(34, 197, 94, 0.16), transparent 28%),
          radial-gradient(circle at top right, rgba(250, 204, 21, 0.14), transparent 24%),
          linear-gradient(180deg, #07111d 0%, #0b1726 48%, #07111d 100%);
        color: #e7eef7;
      }
      .block-container {
        padding-top: 1.3rem !important;
        padding-bottom: 2rem !important;
        max-width: 1320px;
      }
      .metric-card {
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 18px;
        padding: 1rem 1.05rem;
        background: rgba(11, 22, 36, 0.84);
        box-shadow: 0 18px 40px rgba(0, 0, 0, 0.24);
      }
      div[data-testid="stFileUploader"] {
        background: rgba(11, 22, 36, 0.84);
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 16px;
        padding: 0.5rem 0.75rem;
      }
      div[data-testid="stDataFrame"] {
        background: rgba(11, 22, 36, 0.82);
        border-radius: 16px;
      }
      .insight-card {
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 18px;
        padding: 1rem 1.05rem;
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.95), rgba(11, 18, 32, 0.88));
        min-height: 100%;
      }
      .insight-title {
        color: #f8fafc;
        font-weight: 700;
        font-size: 1.02rem;
        margin-bottom: 0.35rem;
      }
      .insight-text {
        color: #cbd5e1;
        line-height: 1.5;
      }
    </style>
    """,
    unsafe_allow_html=True,
)


def build_sample_data() -> pd.DataFrame:
    base_date = datetime.utcnow().date() - timedelta(days=20)
    regions = ["North", "South", "East", "West"]
    products = ["Starter", "Growth", "Pro", "Enterprise"]
    channels = ["Direct", "Online", "Partner"]

    records = []
    for day in range(21):
        for index, region in enumerate(regions):
            quantity = 8 + day + index
            unit_price = 45 + index * 12 + day * 1.8
            sales = round(quantity * unit_price, 2)
            cost = round(sales * (0.58 - index * 0.03), 2)
            records.append(
                {
                    "order_date": base_date + timedelta(days=day),
                    "region": region,
                    "product": products[(day + index) % len(products)],
                    "channel": channels[(day + index) % len(channels)],
                    "quantity": quantity,
                    "unit_price": round(unit_price, 2),
                    "sales": sales,
                    "cost": cost,
                    "profit": round(sales - cost, 2),
                }
            )

    return pd.DataFrame(records)


def read_uploaded_file(uploaded_file) -> pd.DataFrame:
    file_name = uploaded_file.name.lower()
    if file_name.endswith(".csv"):
        try:
            return pd.read_csv(uploaded_file)
        except UnicodeDecodeError:
            uploaded_file.seek(0)
            return pd.read_csv(uploaded_file, encoding="latin-1")

    return pd.read_excel(uploaded_file)


def clean_column_name(name: str) -> str:
    cleaned = re.sub(r"[^0-9a-zA-Z]+", "_", str(name).strip().lower())
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    return cleaned or "column"


def make_unique(names: Iterable[str]) -> list[str]:
    counts: dict[str, int] = {}
    unique_names: list[str] = []
    for name in names:
        base_name = name
        if base_name not in counts:
            counts[base_name] = 0
            unique_names.append(base_name)
            continue

        counts[base_name] += 1
        unique_names.append(f"{base_name}_{counts[base_name]}")
    return unique_names


def normalize_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
    cleaned = dataframe.copy()
    cleaned.columns = make_unique(clean_column_name(column) for column in cleaned.columns)

    for column in cleaned.columns:
        if pd.api.types.is_object_dtype(cleaned[column]):
            cleaned[column] = cleaned[column].astype(str).str.strip()

    return cleaned


def detect_date_column(dataframe: pd.DataFrame) -> Optional[str]:
    preferred_names = [
        "order_date",
        "date",
        "transaction_date",
        "invoice_date",
        "created_at",
        "sale_date",
        "ship_date",
    ]
    for name in preferred_names:
        if name in dataframe.columns:
            converted = pd.to_datetime(dataframe[name], errors="coerce")
            if converted.notna().sum() > 0:
                dataframe[name] = converted
                return name

    for column in dataframe.columns:
        if any(token in column for token in ("date", "time", "month", "day")):
            converted = pd.to_datetime(dataframe[column], errors="coerce")
            if converted.notna().sum() > 0:
                dataframe[column] = converted
                return column

    return None


def detect_numeric_columns(dataframe: pd.DataFrame) -> list[str]:
    numeric_columns: list[str] = []
    for column in dataframe.columns:
        if pd.api.types.is_numeric_dtype(dataframe[column]):
            numeric_columns.append(column)
            continue

        coerced = pd.to_numeric(dataframe[column], errors="coerce")
        success_ratio = coerced.notna().mean() if len(coerced) else 0
        if success_ratio >= 0.75:
            dataframe[column] = coerced
            numeric_columns.append(column)

    return numeric_columns


def detect_text_columns(dataframe: pd.DataFrame, numeric_columns: list[str], date_column: Optional[str]) -> list[str]:
    text_columns = []
    for column in dataframe.columns:
        if column in numeric_columns or column == date_column:
            continue
        unique_ratio = dataframe[column].nunique(dropna=True) / max(len(dataframe), 1)
        if dataframe[column].dtype == "object" or unique_ratio <= 0.2:
            text_columns.append(column)
    return text_columns


def choose_metric_column(candidates: list[str], dataframe: pd.DataFrame, fallback: Optional[str] = None) -> Optional[str]:
    for candidate in candidates:
        if candidate in dataframe.columns:
            return candidate
    return fallback


def enrich_sales_data(dataframe: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Optional[str]]]:
    processed = normalize_dataframe(dataframe)
    processed = processed.dropna(how="all").reset_index(drop=True)

    date_column = detect_date_column(processed)
    numeric_columns = detect_numeric_columns(processed)
    text_columns = detect_text_columns(processed, numeric_columns, date_column)

    quantity_column = choose_metric_column(["quantity", "qty", "units", "order_qty", "items"], processed)
    unit_price_column = choose_metric_column(["unit_price", "price", "avg_price", "sale_price"], processed)
    sales_column = choose_metric_column(
        ["sales", "revenue", "amount", "total", "order_total", "net_sales"],
        processed,
    )
    profit_column = choose_metric_column(["profit", "gross_profit", "margin"], processed)
    category_column = choose_metric_column(
        ["product", "category", "region", "channel", "segment", "state", "country"],
        processed,
        fallback=text_columns[0] if text_columns else None,
    )

    if sales_column is None and quantity_column and unit_price_column:
        processed["estimated_sales"] = pd.to_numeric(processed[quantity_column], errors="coerce").fillna(0) * pd.to_numeric(
            processed[unit_price_column], errors="coerce"
        ).fillna(0)
        sales_column = "estimated_sales"
        numeric_columns.append("estimated_sales")

    if date_column:
        processed[date_column] = pd.to_datetime(processed[date_column], errors="coerce")
        processed = processed.sort_values(by=date_column).reset_index(drop=True)
        processed["year"] = processed[date_column].dt.year
        processed["month"] = processed[date_column].dt.strftime("%Y-%m")
        processed["day_name"] = processed[date_column].dt.day_name()

    if sales_column and sales_column in processed.columns:
        processed[sales_column] = pd.to_numeric(processed[sales_column], errors="coerce")
    if profit_column and profit_column in processed.columns:
        processed[profit_column] = pd.to_numeric(processed[profit_column], errors="coerce")

    context = {
        "date_column": date_column,
        "sales_column": sales_column,
        "profit_column": profit_column,
        "quantity_column": quantity_column,
        "unit_price_column": unit_price_column,
        "category_column": category_column,
    }
    return processed, context


def safe_sum(series: Optional[pd.Series]) -> float:
    if series is None:
        return 0.0
    return float(pd.to_numeric(series, errors="coerce").fillna(0).sum())


def safe_mean(series: Optional[pd.Series]) -> float:
    if series is None:
        return 0.0
    values = pd.to_numeric(series, errors="coerce").dropna()
    if values.empty:
        return 0.0
    return float(values.mean())


def format_currency(value: float) -> str:
    return f"${value:,.2f}"


st.title("Sales Insights Studio")
st.caption("Upload sales data, clean and analyze it automatically, then download the processed CSV.")

st.subheader("Upload Data")
uploaded_file = st.file_uploader("Choose CSV or Excel file", type=["csv", "xlsx"], label_visibility="collapsed")

if uploaded_file is None:
    st.info("Upload a CSV or Excel file to begin analysis.")
    st.stop()

raw_data = read_uploaded_file(uploaded_file)

if raw_data.empty:
    st.warning("The uploaded dataset is empty.")
    st.stop()

with st.sidebar:
    st.header("View Options")
    max_rows = st.slider("Rows to preview", min_value=50, max_value=5000, value=1000, step=50)

processed_data, context = enrich_sales_data(raw_data)
preview_data = processed_data.head(max_rows).copy()

sales_column = context["sales_column"]
profit_column = context["profit_column"]
date_column = context["date_column"]
category_column = context["category_column"]
quantity_column = context["quantity_column"]

numeric_columns = list(processed_data.select_dtypes(include="number").columns)
if not numeric_columns:
    st.error("No numeric fields were detected after processing. Please upload a sales file with at least one numeric column.")
    st.stop()

total_sales = safe_sum(processed_data[sales_column]) if sales_column and sales_column in processed_data else 0.0
total_profit = safe_sum(processed_data[profit_column]) if profit_column and profit_column in processed_data else 0.0
margin = (total_profit / total_sales * 100) if total_sales else 0.0
avg_sales = safe_mean(processed_data[sales_column]) if sales_column and sales_column in processed_data else 0.0
row_count = len(processed_data)

top_category_label = "N/A"
top_category_value = "N/A"
if category_column and category_column in processed_data.columns and sales_column and sales_column in processed_data.columns:
    grouped = processed_data.groupby(category_column, dropna=False)[sales_column].sum().sort_values(ascending=False)
    if not grouped.empty:
        top_category_label = str(grouped.index[0])
        top_category_value = format_currency(float(grouped.iloc[0]))

date_range = "N/A"
if date_column and date_column in processed_data.columns:
    date_values = pd.to_datetime(processed_data[date_column], errors="coerce").dropna()
    if not date_values.empty:
        date_range = f"{date_values.min().date()} → {date_values.max().date()}"

left_metric, middle_metric, right_metric, fourth_metric = st.columns(4)
with left_metric:
    st.markdown(f"<div class='metric-card'><strong>Total Sales</strong><br>{format_currency(total_sales)}</div>", unsafe_allow_html=True)
with middle_metric:
    st.markdown(f"<div class='metric-card'><strong>Total Profit</strong><br>{format_currency(total_profit)}</div>", unsafe_allow_html=True)
with right_metric:
    st.markdown(f"<div class='metric-card'><strong>Profit Margin</strong><br>{margin:.1f}%</div>", unsafe_allow_html=True)
with fourth_metric:
    st.markdown(f"<div class='metric-card'><strong>Rows Processed</strong><br>{row_count:,}</div>", unsafe_allow_html=True)

st.divider()

overview_col, insight_col = st.columns([1.35, 1])
with overview_col:
    st.subheader("Processed Data Preview")
    st.dataframe(processed_data, use_container_width=True, height=360)

with insight_col:
    st.subheader("Smart Insights")
    st.markdown(
        f"""
        <div class='insight-card'>
          <div class='insight-title'>What stands out</div>
          <div class='insight-text'>
            • Best performing category: <strong>{top_category_label}</strong> with <strong>{top_category_value}</strong> in sales.<br><br>
            • Average order value: <strong>{format_currency(avg_sales)}</strong><br><br>
            • Date coverage: <strong>{date_range}</strong><br><br>
            • Detected sales column: <strong>{sales_column or 'None'}</strong><br>
            • Detected quantity column: <strong>{quantity_column or 'None'}</strong>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

tab_overview, tab_charts, tab_download = st.tabs(["Overview", "Charts", "Download"])

with tab_overview:
    st.subheader("Data Quality Summary")
    quality_left, quality_middle, quality_right = st.columns(3)
    with quality_left:
        st.markdown(
            f"<div class='metric-card'><strong>Columns</strong><br>{len(processed_data.columns)}</div>",
            unsafe_allow_html=True,
        )
    with quality_middle:
        st.markdown(
            f"<div class='metric-card'><strong>Numeric Fields</strong><br>{len(numeric_columns)}</div>",
            unsafe_allow_html=True,
        )
    with quality_right:
        st.markdown(
            f"<div class='metric-card'><strong>Detected Date Column</strong><br>{date_column or 'None'}</div>",
            unsafe_allow_html=True,
        )

    st.markdown("### Top Rows")
    st.dataframe(processed_data.head(20), use_container_width=True, height=260)

with tab_charts:
    chart_left, chart_right = st.columns(2)
    with chart_left:
        st.subheader("Sales by Category")
        if category_column and sales_column and category_column in processed_data.columns and sales_column in processed_data.columns:
            category_chart = processed_data.groupby(category_column, dropna=False)[sales_column].sum().sort_values(ascending=False).head(12)
            st.bar_chart(category_chart)
        else:
            st.info("No category column was detected for a category chart.")

    with chart_right:
        st.subheader("Sales vs Profit")
        if sales_column and profit_column and sales_column in processed_data.columns and profit_column in processed_data.columns:
            scatter_source = processed_data[[sales_column, profit_column]].dropna()
            if not scatter_source.empty:
                st.scatter_chart(scatter_source, x=sales_column, y=profit_column)
            else:
                st.info("Not enough complete sales and profit rows for a scatter chart.")
        else:
            st.info("Need both sales and profit columns to show this view.")

    st.subheader("Trend Over Time")
    if date_column and sales_column and date_column in processed_data.columns and sales_column in processed_data.columns:
        trend = processed_data.copy()
        trend[date_column] = pd.to_datetime(trend[date_column], errors="coerce").dt.date
        trend = trend.dropna(subset=[date_column])
        if not trend.empty:
            trend_grouped = trend.groupby(date_column, as_index=False)[sales_column].sum().sort_values(by=date_column)
            st.line_chart(trend_grouped.set_index(date_column)[sales_column])
        else:
            st.info("The detected date column could not be converted into dates.")
    else:
        st.info("No date column was detected, so the trend chart is unavailable.")

with tab_download:
    st.subheader("Download Processed CSV")
    st.write("The processed file includes cleaned column names, parsed dates, numeric conversions, and helpful derived fields.")

    csv_bytes = processed_data.to_csv(index=False).encode("utf-8")
    download_name = "processed_sales_data.csv"
    st.download_button(
        label="Download processed CSV",
        data=csv_bytes,
        file_name=download_name,
        mime="text/csv",
        use_container_width=False,
    )

    st.markdown("### Processed Columns")
    st.write(", ".join(processed_data.columns))
