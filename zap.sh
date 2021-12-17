#!/bin/bash
VERSION=$(date +%Y%m%d)
case $1 in
    download ) 
        python3 -m src.runner $2
    ;;
    upload )
        location=US
        dataset=$2
        VERSION=${3:-$VERSION}
        tablename=$dataset.$VERSION
        FILEPATH=gs://zap-crm-export/datasets/$dataset/$VERSION/$dataset.csv
        gsutil cp .output/$dataset/$dataset.csv $FILEPATH
        bq show $dataset || bq mk --location=$location --dataset $dataset
        bq show $tablename || bq mk $tablename
        bq load \
            --location=$location\
            --source_format=CSV\
            --quote '"' \
            --skip_leading_rows 1\
            --replace\
            --allow_quoted_newlines\
            $tablename \
            $FILEPATH \
            schemas/$dataset.json
    ;;
    upload_do )
        FILENAME=$2
        DATE=$(date "+%Y-%m-%d")
        SPACES='? asked Amanda, gotta figure this out'
        mc cp --atr acl=privte -r output $SPACES/$DATE


esac