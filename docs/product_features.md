## Objective

Create product-level features for ML clustering.

## Features
order_frequency → How often a product is ordered
total_quantity → Total units sold
avg_quantity_per_order → Average units per order
related_product_count → Number of products frequently purchased with it

## Output
Product
   ↓
Demand + Quantity + Affinity
   ↓
Product Feature Table

## Saved as:

data/processed/product_features.csv

## Key Insight

Each SKU now has a business profile that can be used for K-Means clustering and warehouse slot recommendations.