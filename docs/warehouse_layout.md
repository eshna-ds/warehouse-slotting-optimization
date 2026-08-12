## Objective

To create a simulated warehouse layout and assign current locations to products.

## Tasks Completed
Created a 5 × 5 warehouse grid with 25 slots.
Assigned (x, y) coordinates to each warehouse slot.
Assigned a current warehouse slot to each product.
Added current x and y coordinates for products.
Defined the packing area as the starting point.
Visualized the warehouse layout.
Saved warehouse and product-location data for further analysis.

## Warehouse Layout
      1    2    3    4    5

A    A1   A2   A3   A4   A5
B    B1   B2   B3   B4   B5
C    C1   C2   C3   C4   C5
D    D1   D2   D3   D4   D5
E    E1   E2   E3   E4   E5

## Each slot has coordinates such as:

A1 → (0,0)
A2 → (0,1)
B1 → (1,0)

## Example

Product: 85099B
Current Slot: A1
Coordinates: (0,0)

## Files Generated
data/processed/
├── warehouse_slots.csv
└── product_locations.csv

## Business Purpose

The warehouse layout provides a physical representation of product locations. This allows the project to calculate actual picking distances in the next stage.