#!/bin/bash


if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <CSV_FILE> <SCHEMA_FILE> <BQ_TABLE> <BQ_PROJECT:DATASET>"
    exit 1
fi


CSV_FILE=$1
SCHEMA_FILE=$2
BQ_TABLE=$3
BQ_PROJECT_DATASET=$4

echo "Preview of CSV file:"
head "$CSV_FILE"


bq load --source_format=CSV  \
        --quote "" \
        --field_delimiter='\t' \
        --allow_jagged_rows \
        --ignore_unknown_values \
        --allow_quoted_newlines \
        --max_bad_records 1 \
        --null_marker="\N" \
        --null_marker="NULL" \
        --null_marker="\\N" \
        --null_marker=NULL \
        --skip_leading_rows=1 \
        --schema=${SCHEMA_FILE} \
        -E UTF-8 \
        "${BQ_PROJECT_DATASET}.${BQ_TABLE}" \
        "$CSV_FILE"


if [ $? -eq 0 ]; then
    echo "Data loaded successfully."
    # Remove the CSV file after successful upload
    #rm "$CSV_FILE"
else
    echo "Failed to load data. Please check the error messages above."
fi

