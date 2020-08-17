Once installed, first you should enable consumptions for a certain equipment
and filling a default warehouse for the picking operations:

.. figure:: ../static/description/equipment.png
   :alt: Kanban view
   :width: 600 px

Then, for every mainteance request of this equipment, *Picking List* button
allows us to make consumptions, that will be picking documents with their own 
sequence:

.. figure:: ../static/description/request-1.png
   :alt: Kanban view
   :width: 600 px

.. figure:: ../static/description/pick-1.png
   :alt: Kanban view
   :width: 600 px

By default, the origin location for this operations will be the stock location
for the default warehouse, and destination a new *Consumptions* location, that
will not compute for stock inventory, like e.g. partner locations:

.. figure:: ../static/description/move-line.png
   :alt: Kanban view
   :width: 600 px

From both request and equipment forms these stock operations and *Product Moves*
are available.

Return operations are also enabled, and will be linked to the request and 
equipment as well:

.. figure:: ../static/description/pick-2.png
   :alt: Kanban view
   :width: 600 px
