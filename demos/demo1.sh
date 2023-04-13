# Test all specifications
# ./demos/demo1.sh > ./results/demo1_res.txt

echo "return all urls"
curl http://127.0.0.1:5000/ -X GET
echo "add 3 urls"
curl http://127.0.0.1:5000/ -d "url=http://www.baidu.com" -X POST
curl http://127.0.0.1:5000/ -d "url=http://www.facebook.com" -X POST
curl http://127.0.0.1:5000/ -d "url=http://www.twitter.com" -X POST
curl http://127.0.0.1:5000/ -X GET 
echo "update (1:http://www.baidu.com) to (1:http://www.taobao.com)"
curl http://127.0.0.1:5000/1 -d "url=http://www.taobao.com" -X PUT 
curl http://127.0.0.1:5000/ -X GET 
echo "delete a url(1)"
curl http://127.0.0.1:5000/1 -X DELETE
echo "return all urls"
curl http://127.0.0.1:5000/ -X GET 
echo "add a new url"
curl http://127.0.0.1:5000/ -d "url=http://www.openai.com" -X POST
echo "return all urls"
curl http://127.0.0.1:5000/ -X GET 
echo "GET non-existing ID @#"
curl http://127.0.0.1:5000/@# -X GET 
echo "GET ID 1"
curl http://127.0.0.1:5000/1 -X GET 
echo "DELETE ALL IDs"
curl http://127.0.0.1:5000/ -X DELETE
 
#> ./results/demo1_res.txt