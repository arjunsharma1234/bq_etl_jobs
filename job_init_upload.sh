#!/bin/bash

#------------funnel
#/bin/bash /root/workspace/upload_bq.sh /root/workspace/cleaned_orders_order.csv schemas/schema_orders_order.json orders_order bakingo-a1694:analytics_writedb


#!/bin/bash

# Define variables for file paths and table name 

#-----------rewiew rating

DATA_PATH="/root/workspace"
CSV_FILE="cleaned_bakingo_swiggy_rating_feedback.csv"
SCHEMA="bakingo_swiggy_rating_feedback"
SCHEMA_PATH="${DATA_PATH}/schemas/schema_${SCHEMA}.json"
TABLE_NAME="bakingo_swiggy_rating_feedback"
DATASET="bakingo-a1694:analytics_writedb"


/bin/bash /root/workspace/upload_bq.sh "${DATA_PATH}/${CSV_FILE}" "${SCHEMA_PATH}" "${TABLE_NAME}" "${DATASET}"
