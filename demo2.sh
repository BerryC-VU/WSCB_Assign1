echo "add 3 urls"
curl http://127.0.0.1:5000/ -d "url=http://www.youtube.com" -X POST
curl http://127.0.0.1:5000/ -d "url=http://www.instagram.com" -X POST
curl http://127.0.0.1:5000/ -d "url=http://www.yahoo.com" -X POST
curl http://127.0.0.1:5000/ -X GET 
# echo "delete a url(1)"
# curl http://127.0.0.1:5000/1 -X DELETE
# echo "return all urls"
# curl http://127.0.0.1:5000/ -X GET 
 