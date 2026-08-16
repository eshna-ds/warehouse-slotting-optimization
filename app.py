import streamlit as st
import pandas as pd
from pathlib import Path

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Warehouse Slotting Optimization",
    page_icon="📦",
    layout="wide"
)

# ============================================================
# FILE PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "processed"

RECOMMENDATION_FILE = DATA_DIR / "final_slot_recommendations.csv"
WAREHOUSE_FILE = DATA_DIR / "warehouse_slots.csv"

# ============================================================
# LOAD FINAL RECOMMENDATIONS
# ============================================================

@st.cache_data
def load_recommendations():
    if not RECOMMENDATION_FILE.exists():
        raise FileNotFoundError(
            f"File not found:\n{RECOMMENDATION_FILE}\n\n"
            "Run the final slot-assignment notebook first."
        )

    df = pd.read_csv(RECOMMENDATION_FILE)

    required_columns = [
        "StockCode",
        "order_frequency",
        "total_quantity",
        "avg_quantity_per_order",
        "related_product_count",
        "cluster_name",
        "recommended_zone",
        "optimized_slot",
        "picking_priority",
        "current_distance",
        "optimized_distance",
        "actual_distance_saved",
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "The final CSV is missing these columns:\n"
            + ", ".join(missing_columns)
        )

    df["StockCode"] = (
        df["StockCode"]
        .astype(str)
        .str.strip()
    )

    return df


@st.cache_data
def load_warehouse():
    if not WAREHOUSE_FILE.exists():
        return pd.DataFrame()

    warehouse = pd.read_csv(WAREHOUSE_FILE)

    if "slot" not in warehouse.columns:
        return pd.DataFrame()

    warehouse["slot"] = (
        warehouse["slot"]
        .astype(str)
        .str.strip()
    )

    if "zone" not in warehouse.columns:
        zone_map = {
            "A": "Zone A",
            "B": "Zone B",
            "C": "Zone C",
            "D": "Zone D",
            "E": "Zone E",
        }

        warehouse["zone"] = (
            warehouse["slot"]
            .str[0]
            .str.upper()
            .map(zone_map)
        )

    return warehouse


# ============================================================
# LOAD DATA
# ============================================================

try:
    products = load_recommendations()
    warehouse = load_warehouse()
except Exception as error:
    st.error("Unable to load the project data.")
    st.code(str(error))
    st.stop()


# ============================================================
# TITLE
# ============================================================

st.title("🔎 Product Slot Recommendation")

st.write(
    "Enter a StockCode to find the recommended warehouse "
    "zone and slot."
)

# ============================================================
# PRODUCT INPUT
# ============================================================

stock_codes = sorted(
    products["StockCode"].dropna().unique().tolist()
)

stock_code = st.selectbox(
    "Enter Product StockCode",
    options=stock_codes,
    index=None,
    placeholder="Select or type a StockCode..."
)

# ============================================================
# PRODUCT SEARCH
# ============================================================

if stock_code is None:
    st.info("Select a StockCode to see its slot recommendation.")
    st.stop()

stock_code = str(stock_code).strip()

matched = products[
    products["StockCode"] == stock_code
]

if matched.empty:
    st.error(f"Product `{stock_code}` was not found.")
    st.stop()

# There should be exactly one row per StockCode because
# Notebook 15 validates duplicate StockCodes.
product = matched.iloc[0]

st.success(f"Product `{stock_code}` found.")

# ============================================================
# PRODUCT INFORMATION
# ============================================================

st.subheader("📦 Product Information")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Cluster",
        str(product["cluster_name"])
    )

with col2:
    st.metric(
        "Recommended Zone",
        str(product["recommended_zone"])
    )

with col3:
    st.metric(
        "Order Frequency",
        f"{float(product['order_frequency']):,.2f}"
    )

with col4:
    st.metric(
        "Total Quantity",
        f"{float(product['total_quantity']):,.0f}"
    )


# ============================================================
# DEMAND AND AFFINITY
# ============================================================

st.subheader("📊 Product Demand & Affinity")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Average Quantity / Order",
        f"{float(product['avg_quantity_per_order']):,.2f}"
    )

with col2:
    st.metric(
        "Related Products",
        f"{float(product['related_product_count']):,.0f}"
    )

with col3:
    st.metric(
        "Picking Priority",
        f"{float(product['picking_priority']):,.0f}"
    )

with col4:
    st.metric(
        "Current Distance",
        f"{float(product['current_distance']):,.0f}"
    )


# ============================================================
# RECOMMENDED SLOT
# ============================================================

recommended_slot = str(product["optimized_slot"]).strip()
recommended_zone = str(product["recommended_zone"]).strip()
optimized_distance = float(product["optimized_distance"])
current_distance = float(product["current_distance"])
distance_saved = float(product["actual_distance_saved"])

st.subheader("⭐ Recommended Slot")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Recommended Slot",
        recommended_slot
    )

with col2:
    st.metric(
        "Recommended Zone",
        recommended_zone
    )

with col3:
    st.metric(
        "Slot Distance",
        f"{optimized_distance:,.0f}"
    )

st.info(
    f"📦 Place **{stock_code}** in **{recommended_slot}** "
    f"({recommended_zone})."
)


# ============================================================
# DISTANCE COMPARISON
# ============================================================

st.subheader("📏 Distance Comparison")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Current Distance",
        f"{current_distance:,.0f}"
    )

with col2:
    st.metric(
        "Optimized Distance",
        f"{optimized_distance:,.0f}"
    )

with col3:
    st.metric(
        "Estimated Distance Saved",
        f"{distance_saved:,.0f}"
    )


# ============================================================
# BUSINESS RECOMMENDATION
# ============================================================

st.subheader("💼 Business Recommendation")

cluster = str(product["cluster_name"]).lower()

if "high-volume" in cluster:
    recommendation = (
        "This is a high-volume product. Keeping it close "
        "to the packing area can reduce picker travel."
    )
elif "slow-moving" in cluster or "low-movement" in cluster:
    recommendation = (
        "This is a low-demand product. It can be placed "
        "farther from the packing area to reserve prime "
        "locations for frequently picked products."
    )
elif "active" in cluster or "regular" in cluster:
    recommendation = (
        "This product has regular demand. Its recommended "
        "zone balances accessibility and warehouse space."
    )
else:
    recommendation = (
        "The recommended slot is selected according to the "
        "product's demand profile and assigned warehouse zone."
    )

st.write(recommendation)


# ============================================================
# AVAILABLE SLOTS IN RECOMMENDED ZONE
# ============================================================

st.subheader("📍 Available Slots in Recommended Zone")

if not warehouse.empty:
    zone_slots = warehouse[
        warehouse["zone"].astype(str).str.strip()
        == recommended_zone
    ].copy()

    if not zone_slots.empty:
        display_columns = [
            column
            for column in [
                "slot",
                "x",
                "y",
                "zone"
            ]
            if column in zone_slots.columns
        ]

        st.dataframe(
            zone_slots[display_columns],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info(
            f"No warehouse slot information was found for "
            f"{recommended_zone}."
        )
else:
    st.info(
        "warehouse_slots.csv is not available, so the "
        "recommendation is shown without the slot list."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Warehouse Slotting Optimization | "
    "Data-driven product placement and picking-distance optimization"
)
