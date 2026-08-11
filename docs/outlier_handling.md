## Objective

Handle extreme values and improve the K-Means clustering results.

## What We Did
Checked extreme values in product features.
Applied log1p() transformation to reduce the effect of extreme values.
Standardized the features using StandardScaler.
Re-ran K-Means with 4 clusters.
Compared the new cluster distribution.

## Final Clusters
Cluster	Products	Business Meaning
0	1,412	Active/Regular Products
1	419	Slow-Moving Products
2	1,224	High-Volume Products ⭐
3	867	Low-Movement Products

## Key Finding

Cluster 2 contains products with the highest:

Order frequency
Total quantity
Average quantity per order
Product affinity

Therefore, these products are high-priority candidates for accessible warehouse locations.

## Output
data/processed/product_clusters_v2.csv

## Key Takeaway

Log transformation reduced the influence of extreme values and produced more balanced, business-meaningful product clusters.