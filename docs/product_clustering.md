## Objective

Group products with similar demand and purchasing behavior using K-Means clustering.

Features Used
order_frequency
total_quantity
avg_quantity_per_order
related_product_count

Features were standardized using StandardScaler before applying K-Means.

## Clustering Results
Cluster	Products	Business Meaning
0	2,192	Active Products
1	1,551	Slow-Moving Products
2	1	Bulk/Outlier Product
3	178	High-Priority Products

## Key Finding

Cluster 3 is especially important because it has:

High order frequency
High total quantity
High product affinity

These products could receive higher-priority warehouse locations.

Cluster 2 contains only one extreme product, so it needs separate outlier handling before final recommendations.

## Output
data/processed/product_clusters.csv
Key Takeaway

K-Means converted individual product features into meaningful business groups that can guide warehouse slotting decisions.
