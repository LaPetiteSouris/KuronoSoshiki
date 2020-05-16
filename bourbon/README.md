# Bourbon

![Alt text](bourbon.jpg?raw=true "bourbon")


Bourbon is the a Faust (https://github.com/robinhood/faust) worker
Bourbon is the simplified version of a dedicated Data Quality Watchdog
It contains 3 Faust agents:


1. Enforce Data Quality Control on the raw data

2. Sink the message indicating data quality in the new topic

3. Subscribe to the topic contained data quality message and log it out.

![Alt text](bourbon_diag.jpg?raw=true "bourgon")