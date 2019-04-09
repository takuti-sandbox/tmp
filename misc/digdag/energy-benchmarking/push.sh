#!/bin/bash

project_name=energy_prediction

project_files=(
  "queries/"
  "config.yml"
  "energy_prediction.dig"
)

echo "database: $1" > config.yml

tar -czvf $project_name.tar.gz ${project_files[@]}
td wf upload $project_name.tar.gz $1
