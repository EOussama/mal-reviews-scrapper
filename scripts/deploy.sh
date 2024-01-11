#! /bin/bash

mkdir -p build/assets

cp public/* build
cp out/**/*.json build/assets

file_array=()

for file in build/assets/*.json; do
    if [ -f "$file" ]; then
        file_array+=("$file")
    fi
done

json_array=$(printf "%s," "${file_array[@]}" | sed 's/$//')
echo "$json_array" > "build/assets/reviews.csv"