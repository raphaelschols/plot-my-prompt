northwind_db_context = """
         DATABASE SCHEMA CONTEXT

         Tables and Columns:

         1. Categories
            - CategoryID (INTEGER, PRIMARY KEY)
            - CategoryName (TEXT)
            - Description (TEXT)
            - Picture (BLOB)

         2. Products
            - ProductID (INTEGER, PRIMARY KEY)
            - ProductName (TEXT)
            - SupplierID (INTEGER, FOREIGN KEY -> Suppliers.SupplierID)
            - CategoryID (INTEGER, FOREIGN KEY -> Categories.CategoryID)
            - QuantityPerUnit (TEXT)
            - UnitPrice (REAL)
            - UnitsInStock (INTEGER)
            - UnitsOnOrder (INTEGER)
            - ReorderLevel (INTEGER)
            - Discontinued (INTEGER)

         3. Suppliers
            - SupplierID (INTEGER, PRIMARY KEY)
            - CompanyName (TEXT)
            - ContactName (TEXT)
            - ContactTitle (TEXT)
            - Address (TEXT)
            - City (TEXT)
            - Region (TEXT)
            - PostalCode (TEXT)
            - Country (TEXT)
            - Phone (TEXT)
            - Fax (TEXT)
            - Homepage (TEXT)

         4."Order Details"
            - OrderID (INTEGER, FOREIGN KEY -> Orders.OrderID)
            - ProductID (INTEGER, FOREIGN KEY -> Products.ProductID)
            - UnitPrice (REAL)
            - Quantity (INTEGER)
            - Discount (REAL)

         5. Orders
            - OrderID (INTEGER, PRIMARY KEY)
            - CustomerID (TEXT, FOREIGN KEY -> Customers.CustomerID)
            - EmployeeID (INTEGER, FOREIGN KEY -> Employees.EmployeeID)
            - OrderDate (DATE)
            - RequiredDate (DATE)
            - ShippedDate (DATE)
            - ShipVia (INTEGER, FOREIGN KEY -> Shippers.ShipperID)
            - Freight (REAL)
            - ShipName (TEXT)
            - ShipAddress (TEXT)
            - ShipCity (TEXT)
            - ShipRegion (TEXT)
            - ShipPostalCode (TEXT)
            - ShipCountry (TEXT)

         6. Customers
            - CustomerID (TEXT, PRIMARY KEY)
            - CompanyName (TEXT)
            - ContactName (TEXT)
            - ContactTitle (TEXT)
            - Address (TEXT)
            - City (TEXT)
            - Region (TEXT)
            - PostalCode (TEXT)
            - Country (TEXT)
            - Phone (TEXT)
            - Fax (TEXT)

         7. CustomerCustomerDemo
            - CustomerID (TEXT, FOREIGN KEY -> Customers.CustomerID)
            - CustomerTypeID (TEXT, FOREIGN KEY -> CustomerDemographics.CustomerTypeID)

         8. CustomerDemographics
            - CustomerTypeID (TEXT, PRIMARY KEY)
            - CustomerDesc (TEXT)

         9. Employees
            - EmployeeID (INTEGER, PRIMARY KEY)
            - LastName (TEXT)
            - FirstName (TEXT)
            - Title (TEXT)
            - TitleOfCourtesy (TEXT)
            - BirthDate (DATE)
            - HireDate (DATE)
            - Address (TEXT)
            - City (TEXT)
            - Region (TEXT)
            - PostalCode (TEXT)
            - Country (TEXT)
            - HomePhone (TEXT)
            - Extension (TEXT)
            - Notes (TEXT)
            - ReportsTo (INTEGER, FOREIGN KEY -> Employees.EmployeeID)
            - PhotoPath (TEXT)

         10. EmployeeTerritories
            - EmployeeID (INTEGER, FOREIGN KEY -> Employees.EmployeeID)
            - TerritoryID (TEXT, FOREIGN KEY -> Territories.TerritoryID)

         11. Territories
            - TerritoryID (TEXT, PRIMARY KEY)
            - TerritoryDescription (TEXT)
            - RegionID (INTEGER, FOREIGN KEY -> Region.RegionID)

         12. Region
            - RegionID (INTEGER, PRIMARY KEY)
            - RegionDescription (TEXT)

         13. Shippers
            - ShipperID (INTEGER, PRIMARY KEY)
            - CompanyName (TEXT)
            - Phone (TEXT)


         Relationships:
         - Products.CategoryID -> Categories.CategoryID (many-to-one)
         - Products.SupplierID -> Suppliers.SupplierID (many-to-one)
         - "Order Details".OrderID -> Orders.OrderID (many-to-one)
         - "Order Details".ProductID -> Products.ProductID (many-to-one)
         - Orders.CustomerID -> Customers.CustomerID (many-to-one)
         - Orders.EmployeeID -> Employees.EmployeeID (many-to-one)
         - Orders.ShipVia -> Shippers.ShipperID (many-to-one)
         - Employees.ReportsTo -> Employees.EmployeeID (self-join)
         - EmployeeTerritories.EmployeeID -> Employees.EmployeeID (many-to-one)
         - EmployeeTerritories.TerritoryID -> Territories.TerritoryID (many-to-one)
         - Territories.RegionID -> Region.RegionID (many-to-one)
         - CustomerCustomerDemo.CustomerID -> Customers.CustomerID (many-to-one)
         - CustomerCustomerDemo.CustomerTypeID -> CustomerDemographics.CustomerTypeID (many-to-one)

         Usage Notes:
         - "Order Details" links Orders and Products for line items.
         - EmployeeTerritories links Employees to multiple Territories.
         - Some fields (StateRegion, RegionDescription) are descriptive only.
         - Dates are stored as YYYY-MM-DD.
"""