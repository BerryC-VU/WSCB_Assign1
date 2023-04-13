# ./demos/demo2.sh > ./results/demo2_res.txt

echo "add 1 url"
curl http://127.0.0.1:5000/ -d "url=http://www.youtube.com" -X POST
echo "add existed URL"
curl http://127.0.0.1:5000/ -d "url=http://www.youtube.com" -X POST
echo "add one valid, but non-existed URL"
curl http://127.0.0.1:5000/ -d "url=http://example.com/brother.php" -X POST
echo "add one invalid URL"
curl http://127.0.0.1:5000/ -d "url=http://yahoocom" -X POST
curl http://127.0.0.1:5000/ -X GET 
# echo "delete a url(1)"
# curl http://127.0.0.1:5000/1 -X DELETE
# echo "return all urls"
# curl http://127.0.0.1:5000/ -X GET 
 
#> ./results/demo2_res.txt