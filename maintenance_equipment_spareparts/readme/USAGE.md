Equipment Spare Parts
=====================

To manage spare parts for an equipment:

* Go to *Maintenance > Equipments* and open an equipment form
* Click on the *Spare Parts* tab
* Click *Add a line* to add a new spare part
* Select a *Product* from the catalog
* Enter the *Installed Quantity* (quantity used by the equipment)
* Enter the *Recommended Spare Quantity* (minimum quantity to keep in stock)
* Save the record

The system will automatically calculate and display:
* Available quantity in stock
* Alert indicator when stock falls below recommended spare quantity

Adding Spare Parts During Maintenance
======================================

When performing maintenance:

* Create or open a maintenance request for an equipment
* Go to the *Spare Parts* section
* If you identify a spare part that is not yet registered, you can add it directly from the request
* The spare part will be automatically added to the equipment's spare parts list

Consuming Spare Parts
=====================

During maintenance, you can consume spare parts:

* In a maintenance request, click *Consume Spare Parts*
* A wizard will open showing all spare parts for the equipment
* Enter the quantity needed for each spare part
* Click *Consume*

The system will:
* If stock is available: automatically create a stock picking and movement
* If stock is not available: automatically create a purchase request with the needed quantity

Purchase Requisition Integration
=================================

When creating a purchase requisition for equipment spare parts:

* Select the equipment in the purchase requisition form
* The product selection will be restricted to only spare parts registered for that equipment
* You cannot add products that are not registered as spare parts for the selected equipment
* If you try to add a non-registered product, the system will prevent it and inform you that the product must be registered as a spare part first

Stock Alerts
============

The system monitors spare parts stock levels:

* When the available quantity falls below the recommended spare quantity, an alert indicator is shown
* You can use the *Create Purchase Request* button to automatically generate a purchase request for all parts needing replenishment
