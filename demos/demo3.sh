# Test two demos concurrently, see if the lock works.
# ./demos/demo3.sh > ./results/demo3_res.txt
(sh -x demos/demo1.sh & sh -x demos/demo2.sh) 