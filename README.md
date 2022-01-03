# Home Inventory Management System (HIMS)
**Assignment Unit:** SWE30011 IoT Programming  
**Language(s):** C++, Python, HTML, CSS, JavaScript
**Description:** The system helps keep track of the quantities of their household consumables using weight sensors and RFID, and sends the data up into the cloud (AWS), which
is then retrieved by a web dashboard that displays all the collected information to the user.

## Features
+ Web dashboard created with Python Flask, Bootstrap CSS
+ Cloud implementation connecting the individual nodes with the cloud and the dashboard
+ Node prototype created using Arduino Uno
+ Historical data of each item displayed in time-series graphs
+ Configurable weight threshold for each item
+ Automatically notifies user when items are running low below the set threshold
