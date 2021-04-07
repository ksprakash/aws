#!/bin/bash
source_bucket="cloudcabinet-backup-pre-purge-02-17-2021-oregon-region"
destination_bucket="CyberCabinet"

FILES=("66747/clients/829225/client information/koenig brothers vitals 2021.xlsx")
for ((i = 0; i < ${#FILES[@]}; i++))
do
    echo "s3://$source_bucket/prod/${FILES[$i]}"
    aws s3 cp "s3://$source_bucket/prod/${FILES[$i]}" "s3://$destination_bucket/${FILES[$i]}" --profile master
done
