# 📦 Warehouse Slotting Optimization

> **Data-driven warehouse product placement and picking-distance optimization**

An end-to-end Data Science project that analyzes product demand, purchasing patterns, product affinity, and warehouse locations to recommend the most suitable **warehouse zone and slot** for each product.

The project also includes an interactive **Streamlit application** where a user can enter a product StockCode and instantly receive its recommended warehouse slot, zone, distance, and estimated travel savings.

---

## 🚀 Live Demo

🔗 **Streamlit App:**

https://warehouse-slotting-optimization-ijvsgk7ghxsc3ctzc9jgpd.streamlit.app/

---

## 🎯 Project Objective

Warehouse layout and product placement have a direct impact on order-picking efficiency.

Frequently ordered products placed far away from the packing area can result in:

- Increased picker travel
- Longer order fulfillment time
- Higher operational effort
- Inefficient warehouse space utilization

### Goal

Build a data-driven system that answers:

> **"Where should a product be placed in the warehouse to minimize picking distance while considering its demand and purchasing behavior?"**

---

## 💡 Solution

The project uses historical retail transaction data to:

1. Clean and preprocess transaction data
2. Analyze product demand
3. Calculate product-level features
4. Identify product purchasing affinities
5. Cluster products according to demand behavior
6. Assign products to recommended warehouse zones
7. Generate warehouse slots
8. Optimize product-slot assignments
9. Calculate current and optimized picking distances
10. Generate business recommendations
11. Deploy the final recommendation system using Streamlit

---

# 🔄 Project Workflow


Online Retail Dataset
        ↓
Data Cleaning & Preprocessing
        ↓
Product Demand Analysis
        ↓
Product Affinity Analysis
        ↓
Feature Engineering
        ↓
Product Clustering
        ↓
Outlier Handling
        ↓
Zone Recommendation
        ↓
Warehouse Layout
        ↓
Picking Distance Calculation
        ↓
Slot Optimization
        ↓
Before vs After Evaluation
        ↓
Business Insights
        ↓
Streamlit Application
        ↓
Live Deployment
