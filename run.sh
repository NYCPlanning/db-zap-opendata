#!/bin/bash
VERSION=$(date +%Y%m%d)
case $1 in
    download ) 
        python3 -m src.runner $2
    ;;
    upload )
        location=US
        dataset=$2
        tablename=$dataset.$VERSION
        bq mk --location=$location --dataset $dataset
        bq mk --location=$location --dataset zap
        bq mk $tablename
        bq load \
            --location=$location\
            --source_format=CSV\
            --quote '"' \
            --skip_leading_rows 1\
            --replace\
            --allow_quoted_newlines\
            $tablename .output/$dataset/$dataset.csv schemas/$dataset.json
        bq mk zap.$dataset
        bq query \
            --location=$location\
            --replace\
            --destination_table zap.$dataset \
            --use_legacy_sql=false "SELECT * FROM \`$tablename\`;"
    ;;
esac