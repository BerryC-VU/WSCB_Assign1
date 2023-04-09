# Test 1999 generated URLs
# ./demos/demo4.sh > ./results/demo4_res.txt
while IFS= read -r line || [[ -n "$line" ]]; do
    echo "Text read from file: $line"
    curl http://127.0.0.1:5000/ -d "url=$line" -X POST
done < urls.txt

curl http://127.0.0.1:5000/ -X GET 
#https://stackoverflow.com/questions/10929453/read-a-file-line-by-line-assigning-the-value-to-a-variable