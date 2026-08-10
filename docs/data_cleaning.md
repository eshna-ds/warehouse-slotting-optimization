The raw dataset contained transaction records that could include cancelled orders, invalid quantities, invalid prices, duplicate records, and missing customer information.

Since the goal of this project is warehouse inventory slotting optimization, the cleaned dataset needs to represent valid product-order transactions that can be used to analyze:

Product demand
Order frequency
Product relationships
Picking patterns
Warehouse slotting decisions

## Raw Dataset

The original dataset contained:

Metric	Value
Rows	541,909
Columns	8
Unique Products	4,070
Unique Orders	25,900
Unique Customers	4,372

The main columns were:

InvoiceNo
StockCode
Description
Quantity
InvoiceDate
UnitPrice
CustomerID
Country
