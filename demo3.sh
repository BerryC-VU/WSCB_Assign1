#https://stackoverflow.com/questions/10929453/read-a-file-line-by-line-assigning-the-value-to-a-variable
while IFS= read -r line || [[ -n "$line" ]]; do
    echo "Text read from file: $line"
    curl http://127.0.0.1:5000/ -d "url=$line" -X POST
done < test.txt

curl http://127.0.0.1:5000/ -X GET 