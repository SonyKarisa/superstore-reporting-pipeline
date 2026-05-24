# superstore-reporting-pipeline
Business Operations Automation
_______

## Spec: Unprofitable Orders Alert
* Load the Superstore dataset from the local Excel file
* Identify all orders where profit is negative
* Output a clean summary (order ID, customer name, product, sales, profit) into a new Google Sheet tab called "Flagged Orders"
* Send a single SMS via Twilio summarizing how many flagged orders were found (e.g. "Alert: 23 unprofitable orders detected in latest report run")
