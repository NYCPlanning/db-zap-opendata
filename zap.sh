#!/bin/bash
VERSION=$(date +%Y%m%d)
case $1 in
    download ) 
        python3 -m src.runner $2
    ;;
    upload_bq )
        # only archives CRM and recoded version, not the subest for Open Data
        dataset=$2
        VERSION=${3:-$VERSION}
        location=US

        # crm version
        FILEPATH=gs://zap-crm-export/datasets/$dataset/$VERSION/$dataset.csv
        tablename=$dataset.$VERSION
        echo "Archving non-visible version ${dataset} ${VERSION} to ${tablename}..."

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
        
        # recoded version
        recoded_filename="${dataset}_after_recode.csv"
        FILEPATH=gs://zap-crm-export/datasets/$dataset/$VERSION/${dataset}_recoded.csv
        VERSION_RECODED="${VERSION}_recoded"
        tablename=$dataset.$VERSION_RECODED
        echo "Archving recoded version ${dataset} ${VERSION_RECODED} to ${tablename}..."

        gsutil cp .cache/$dataset/$recoded_filename $FILEPATH
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
        dataset=$2
        VERSION=$3
        SPACES="spaces/edm-publishing/db-zap"
        visible_filename="${dataset}_visible.csv"
        mc cp .output/$dataset/$visible_filename $SPACES/$VERSION/$dataset/$dataset.csv
        mc cp .output/$dataset/$visible_filename $SPACES/latest/$dataset/$dataset.csv


esac