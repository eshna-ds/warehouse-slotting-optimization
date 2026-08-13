## Objective

Calculate the current picking distance for warehouse orders using the simulated warehouse locations.

## Tasks Completed

Loaded warehouse slots and product information.
Mapped products to their current warehouse coordinates.
Connected products with customer orders.
Used Manhattan distance to calculate travel distance.
Calculated total picking distance for each order.
Calculated the average picking distance as the baseline.
Created a distribution plot of order picking distances.

## Formula
Distance = |x1 - x2| + |y1 - y2|

## Result

The picking-distance distribution is right-skewed, meaning most orders have relatively lower distances while a smaller number of orders require substantially longer travel.

## Output

current_order_distances.csv

## Business Purpose

This provides the baseline warehouse performance. Later, after optimization, we can compare:

Current Average Distance
          ↓
   Optimization
          ↓
Optimized Average Distance
          ↓
Distance Reduction %
