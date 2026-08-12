## Objective

To recommend warehouse zones for products and estimate potential picking-distance savings.

## Tasks Completed

Rebuilt product-level features with correct StockCode.
Calculated order frequency and product affinity.
Applied K-Means clustering to group products.
Assigned business names to clusters based on their characteristics.
Recommended warehouse zones based on product movement.
Calculated picking priority.
Simulated distance from the packing area.
Estimated potential travel-distance savings.

## Cluster Groups

Cluster	Business Name
0	Active/Regular Products
1	Slow-Moving Products
2	Bulk/Exceptional Products
3	High-Volume Products

## Zone Strategy

High-Volume Products → Zone A → 10 m
Active/Regular        → Zone B → 25 m
Slow-Moving           → Zone C → 40 m
Bulk/Exceptional      → Special Handling

## Key Output

For example, 85099B was identified as a high-volume product and recommended for Zone A, resulting in a simulated distance saving of 50 m compared with the assumed 60 m baseline.

## Business Impact

The system helps warehouses:

Place frequently picked products closer to the packing area, prioritize important SKUs, and pot
entially reduce worker travel during order picking.
