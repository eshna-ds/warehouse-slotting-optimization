import streamlit as st
import pandas as pd
import os


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Warehouse Slotting Optimization",
    page_icon="📦",
    layout="wide"
)


# ============================================================
# PATHS
# ============================================================

OPTIMIZED_FILE = "data/processed/optimized_slot_recommendations.csv"
BUSINESS_FILE = "data/processed/business_insights.csv"
SUMMARY_FILE = "data/processed/optimization_summary.csv"
WAREHOUSE_FILE = "data/processed/warehouse_slots.csv"


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    optimized = pd.read_csv(OPTIMIZED_FILE)
    business = pd.read_csv(BUSINESS_FILE)
    summary = pd.read_csv(SUMMARY_FILE)
    warehouse = pd.read_csv(WAREHOUSE_FILE)

    return optimized, business, summary, warehouse


# ============================================================
# CHECK FILES
# ============================================================

required_files = [
    OPTIMIZED_FILE,
    BUSINESS_FILE,
    SUMMARY_FILE,
    WAREHOUSE_FILE
]

missing_files = [
    file for file in required_files
    if not os.path.exists(file)
]

if missing_files:

    st.error("The following files are missing:")

    for file in missing_files:
        st.write(f"- `{file}`")

    st.stop()


# ============================================================
# LOAD
# ============================================================

optimized, business, summary, warehouse = load_data()


# ============================================================
# CLEAN DATA
# ============================================================

optimized["StockCode"] = (
    optimized["StockCode"]
    .astype(str)
    .str.strip()
)

business["StockCode"] = (
    business["StockCode"]
    .astype(str)
    .str.strip()
)

warehouse["slot"] = (
    warehouse["slot"]
    .astype(str)
    .str.strip()
)


# ============================================================
# CHECK REQUIRED COLUMNS
# ============================================================

required_optimized_columns = [
    "StockCode",
    "order_frequency",
    "total_quantity",
    "avg_quantity_per_order",
    "related_product_count",
    "cluster_name",
    "recommended_zone",
    "picking_priority",
    "current_distance",
    "optimized_distance",
    "actual_distance_saved"
]

missing_columns = [
    col for col in required_optimized_columns
    if col not in optimized.columns
]

if missing_columns:

    st.error(
        "Missing columns in optimized_slot_recommendations.csv:"
    )

    st.write(missing_columns)

    st.stop()


# ============================================================
# CREATE ZONES FOR WAREHOUSE SLOTS
# ============================================================

def get_zone(x):

    if x <= 1:
        return "Zone A"

    elif x <= 2:
        return "Zone B"

    elif x <= 3:
        return "Zone C"

    else:
        return "Zone D"


if "zone" not in warehouse.columns:

    warehouse["zone"] = warehouse["x"].apply(get_zone)


# ============================================================
# FIND SUMMARY VALUES
# ============================================================

def get_summary_value(metric_name):

    result = summary.loc[
        summary["Metric"] == metric_name,
        "Value"
    ]

    if len(result) > 0:
        return float(result.iloc[0])

    return 0.0


before = get_summary_value(
    "Average Before Distance"
)

after = get_summary_value(
    "Average After Distance"
)

saved = get_summary_value(
    "Average Distance Saved"
)

products = len(optimized)


if before != 0:

    improvement = (
        (before - after) / before
    ) * 100

else:

    improvement = 0


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("📦 Warehouse Optimization")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Overview",
        "🔎 Slot Recommendation",
        "🏭 Warehouse Layout",
        "💼 Business Insights"
    ]
)

st.sidebar.divider()

st.sidebar.info(
    "Enter a StockCode in the Slot Recommendation page "
    "to find the recommended warehouse slot."
)


# ============================================================
# PAGE 1 — OVERVIEW
# ============================================================

if page == "🏠 Overview":

    st.title("📦 Warehouse Slotting Optimization")

    st.write(
        "Data-driven warehouse product placement "
        "and picking-distance optimization."
    )

    st.divider()

    # KPI CARDS

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Products Analyzed",
        f"{products:,}"
    )

    col2.metric(
        "Avg. Distance Before",
        f"{before:.2f}"
    )

    col3.metric(
        "Avg. Distance After",
        f"{after:.2f}"
    )

    col4.metric(
        "Avg. Distance Saved",
        f"{saved:.2f}"
    )

    st.divider()

    # IMPROVEMENT

    st.subheader("📈 Optimization Performance")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Estimated Improvement",
            f"{improvement:.2f}%"
        )

    with col2:

        st.metric(
            "Total Estimated Distance Saved",
            f"{optimized['actual_distance_saved'].sum():,.0f}"
        )

    st.divider()

    # BEFORE VS AFTER

    st.subheader(
        "📊 Picking Distance — Before vs After"
    )

    comparison = pd.DataFrame(
        {
            "Distance": [
                before,
                after
            ]
        },
        index=[
            "Before Optimization",
            "After Optimization"
        ]
    )

    st.bar_chart(comparison)

    st.divider()

    # CLUSTER DISTRIBUTION

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "📦 Product Cluster Distribution"
        )

        cluster_counts = (
            optimized["cluster_name"]
            .value_counts()
        )

        st.bar_chart(cluster_counts)

    with col2:

        st.subheader(
            "📍 Recommended Zone Distribution"
        )

        zone_counts = (
            optimized["recommended_zone"]
            .value_counts()
        )

        st.bar_chart(zone_counts)


# ============================================================
# PAGE 2 — SLOT RECOMMENDATION
# ============================================================

elif page == "🔎 Slot Recommendation":

    st.title("🔎 Product Slot Recommendation")

    st.write(
        "Enter a StockCode to find the recommended "
        "warehouse zone and slot."
    )

    st.divider()

    # PRODUCT INPUT

    sku_input = st.text_input(
        "Enter Product StockCode",
        placeholder="Example: 85123A"
    )

    # BUTTON

    search_button = st.button(
        "🔍 Find Best Slot",
        type="primary"
    )

    if search_button:

        sku = sku_input.strip()

        if sku == "":

            st.warning(
                "Please enter a StockCode."
            )

        else:

            product_data = optimized[
                optimized["StockCode"]
                .str.upper()
                == sku.upper()
            ]

            if product_data.empty:

                st.error(
                    f"StockCode `{sku}` was not found."
                )

            else:

                product = product_data.iloc[0]

                st.success(
                    f"Product `{product['StockCode']}` found."
                )

                st.divider()

                # --------------------------------------------
                # PRODUCT INFORMATION
                # --------------------------------------------

                st.subheader(
                    "📦 Product Information"
                )

                col1, col2, col3, col4 = st.columns(4)

                col1.metric(
                    "Cluster",
                    product["cluster_name"]
                )

                col2.metric(
                    "Recommended Zone",
                    product["recommended_zone"]
                )

                col3.metric(
                    "Order Frequency",
                    f"{product['order_frequency']:.2f}"
                )

                col4.metric(
                    "Total Quantity",
                    f"{product['total_quantity']:.0f}"
                )

                # --------------------------------------------
                # PRODUCT DETAILS
                # --------------------------------------------

                st.divider()

                st.subheader(
                    "📊 Product Demand & Affinity"
                )

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Average Quantity / Order",
                    f"{product['avg_quantity_per_order']:.2f}"
                )

                col2.metric(
                    "Related Products",
                    f"{product['related_product_count']:.0f}"
                )

                col3.metric(
                    "Picking Priority",
                    f"{product['picking_priority']:,.0f}"
                )

                # --------------------------------------------
                # FIND BEST SLOT
                # --------------------------------------------

                recommended_zone = (
                    product["recommended_zone"]
                )

                zone_slots = warehouse[
                    warehouse["zone"]
                    == recommended_zone
                ].copy()

                if zone_slots.empty:

                    st.error(
                        f"No warehouse slots found "
                        f"for {recommended_zone}."
                    )

                else:

                    # Calculate distance from packing

                    packing_x = 0
                    packing_y = 0

                    zone_slots["slot_distance"] = (
                        abs(
                            zone_slots["x"]
                            - packing_x
                        )
                        +
                        abs(
                            zone_slots["y"]
                            - packing_y
                        )
                    )

                    # Find nearest slot

                    best_slot = zone_slots.loc[
                        zone_slots[
                            "slot_distance"
                        ].idxmin()
                    ]

                    # ----------------------------------------
                    # RECOMMENDATION
                    # ----------------------------------------

                    st.divider()

                    st.subheader(
                        "⭐ Recommended Slot"
                    )

                    col1, col2, col3 = st.columns(3)

                    col1.metric(
                        "Recommended Slot",
                        best_slot["slot"]
                    )

                    col2.metric(
                        "Recommended Zone",
                        recommended_zone
                    )

                    col3.metric(
                        "Slot Distance",
                        f"{best_slot['slot_distance']:.0f}"
                    )

                    st.success(
                        f"📦 Place **{product['StockCode']}** "
                        f"in **{best_slot['slot']}** "
                        f"({recommended_zone})."
                    )

                    # ----------------------------------------
                    # DISTANCE COMPARISON
                    # ----------------------------------------

                    st.divider()

                    st.subheader(
                        "📏 Distance Comparison"
                    )

                    col1, col2, col3 = st.columns(3)

                    col1.metric(
                        "Current Distance",
                        f"{product['current_distance']:.0f}"
                    )

                    col2.metric(
                        "Optimized Distance",
                        f"{best_slot['slot_distance']:.0f}"
                    )

                    calculated_saved = (
                        product["current_distance"]
                        - best_slot["slot_distance"]
                    )

                    col3.metric(
                        "Estimated Distance Saved",
                        f"{calculated_saved:.0f}"
                    )

                    # ----------------------------------------
                    # BUSINESS RECOMMENDATION
                    # ----------------------------------------

                    st.divider()

                    st.subheader(
                        "💼 Business Recommendation"
                    )

                    if (
                        product["cluster_name"]
                        == "High-Volume Products"
                    ):

                        st.info(
                            "This is a high-volume product. "
                            "Keeping it close to the packing area "
                            "can reduce picker travel."
                        )

                    elif (
                        product["cluster_name"]
                        == "Active/Regular Products"
                    ):

                        st.info(
                            "This product has regular movement. "
                            "An easily accessible warehouse zone "
                            "is recommended."
                        )

                    elif (
                        product["cluster_name"]
                        == "Low-Movement Products"
                    ):

                        st.info(
                            "This product has lower movement. "
                            "It can be stored in a moderate-distance zone."
                        )

                    elif (
                        product["cluster_name"]
                        == "Slow-Moving Products"
                    ):

                        st.info(
                            "This is a slow-moving product. "
                            "It can be placed farther from the packing area."
                        )

                    else:

                        st.info(
                            "Follow the recommended warehouse zone "
                            "based on the product analysis."
                        )

                    # ----------------------------------------
                    # CANDIDATE SLOTS
                    # ----------------------------------------

                    st.divider()

                    st.subheader(
                        "📍 Available Slots in Recommended Zone"
                    )

                    display_slots = zone_slots[
                        [
                            "slot",
                            "x",
                            "y",
                            "slot_distance"
                        ]
                    ].sort_values(
                        "slot_distance"
                    )

                    st.dataframe(
                        display_slots.head(10),
                        use_container_width=True,
                        hide_index=True
                    )


# ============================================================
# PAGE 3 — WAREHOUSE LAYOUT
# ============================================================

elif page == "🏭 Warehouse Layout":

    st.title("🏭 Warehouse Layout")

    st.write(
        "Explore warehouse slots by zone."
    )

    st.divider()

    selected_zone = st.selectbox(
        "Select Zone",
        [
            "All Zones",
            "Zone A",
            "Zone B",
            "Zone C",
            "Zone D"
        ]
    )

    if selected_zone == "All Zones":

        layout = warehouse.copy()

    else:

        layout = warehouse[
            warehouse["zone"]
            == selected_zone
        ].copy()

    # --------------------------------------------
    # LAYOUT
    # --------------------------------------------

    st.subheader("📍 Warehouse Coordinates")

    st.scatter_chart(
        layout,
        x="x",
        y="y"
    )

    # --------------------------------------------
    # SLOT TABLE
    # --------------------------------------------

    st.subheader("📋 Warehouse Slots")

    st.dataframe(
        layout[
            [
                "slot",
                "x",
                "y",
                "zone"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# PAGE 4 — BUSINESS INSIGHTS
# ============================================================

elif page == "💼 Business Insights":

    st.title("💼 Business Insights")

    st.write(
        "Business recommendations generated from "
        "warehouse product analysis."
    )

    st.divider()

    # TOP PRIORITY PRODUCTS

    st.subheader(
        "🔥 Top Priority Products"
    )

    top_priority = optimized.sort_values(
        "picking_priority",
        ascending=False
    ).head(20)

    priority_columns = [
        "StockCode",
        "cluster_name",
        "recommended_zone",
        "picking_priority",
        "actual_distance_saved"
    ]

    st.dataframe(
        top_priority[priority_columns],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # TOP DISTANCE SAVINGS

    st.subheader(
        "📏 Products with Highest Estimated Distance Savings"
    )

    top_savings = optimized.sort_values(
        "actual_distance_saved",
        ascending=False
    ).head(20)

    savings_columns = [
        "StockCode",
        "cluster_name",
        "recommended_zone",
        "current_distance",
        "optimized_distance",
        "actual_distance_saved"
    ]

    st.dataframe(
        top_savings[savings_columns],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # CLUSTER INSIGHTS

    st.subheader(
        "📦 Cluster Analysis"
    )

    cluster_analysis = optimized.groupby(
        "cluster_name"
    ).agg(
        product_count=(
            "StockCode",
            "count"
        ),
        avg_priority=(
            "picking_priority",
            "mean"
        ),
        avg_distance_saved=(
            "actual_distance_saved",
            "mean"
        )
    ).reset_index()

    st.dataframe(
        cluster_analysis,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.success(
        "High-volume products are prioritized for "
        "closer warehouse placement because they "
        "are expected to generate more picking activity."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Warehouse Slotting Optimization | "
    "Data-driven product placement and "
    "picking-distance optimization"
)