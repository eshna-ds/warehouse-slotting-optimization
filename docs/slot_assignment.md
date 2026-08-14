## Objective

Assign actual warehouse slots to products based on their recommended zones and calculate the optimized picking distance.

## Tasks Completed

Loaded Day 15 slot recommendations.
Loaded the warehouse layout and available slots.
Assigned products to actual warehouse slots.
Added optimized x and y coordinates.
Calculated optimized distance from the packing area.
Calculated the actual distance saved for each product.

## Formula

Optimized Distance = |optimized_x - packing_x|
                   + |optimized_y - packing_y|
Distance Saved = Current Distance - Optimized Distance

## Example

StockCode: 23309
Current Distance: 60
Optimized Distance: 0
Distance Saved: 60

## Output

optimized_slot_recommendations.csv

Important columns:

StockCode
recommended_zone
optimized_slot
optimized_x
optimized_y
current_distance
optimized_distance
actual_distance_saved
Conclusion

converted the zone-level recommendations from Day 15 into actual warehouse slot assignments and calculated the estimated distance saved for each product.
