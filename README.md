# RESTFUL Service - URL shortening service

**University of Amsterdam Web Services and Cloud-Based System Assignment 1**

The following functions are implemented in this project:

| Path & Method | Functionality                          | Return values                                                                    |
|---------------|----------------------------------------|----------------------------------------------------------------------------------|
| /:id & GET    | Return URL corresponds to the given id | 301, if id exists; 404, if id does not exist|
| /:id & PUT    | Update URL based on the given id       | 200, if id exists and URL valid; 400, if id exists and URL invalid; 404, if id does not exist| 
| /:id & DELETE | Delete URL based on the given id       | 204, delete the (id, URL) from the dict; 404, if id does not exist|
| / & GET | Return all existing (id, URL) pairs          | 200, return all (id, URL) pairs|
| / & POST | Create a new (id,URL) pair in the dict      | 201, if URL is valid and not existed in the dict, generate id; 400, if URL is valid but existed, return corresponding id; 404, if URL is invalid|
| / & DELETE| /       | 404, no operation is allowed|


**Create Environment**

Before starting the server, run the following code to configure the environment:
```
conda env create -f environment.yml
conda avtivate web1
```

**Run the server**

 ```
 python3 main.py
 ```


**Run the Demo** 

There are four demo files under the [demos](https://github.com/BerryC-VU/WSCB_Assign1/tree/main/demos) folder. Users can test what they want using existing `demo*.sh` or create some new requests. The results of the demos can be found in the [results](https://github.com/BerryC-VU/WSCB_Assign1/tree/main/results) folder.
To test all specifications, run the following code in the PATH  for an example:
```
./demos/demo*.sh > ./results/demo*_res.txt
```

**Reference**
1. [Regular expression to check URL format](https://www.makeuseof.com/regular-expressions-validate-url/)  
2. [Check URL existence](https://stackoverflow.com/questions/16778435/python-check-if-website-exists)
3. [Min-heap structure of ID_POOL](https://docs.python.org/3/library/heapq.html)
4. [Base62 converter](https://stackoverflow.com/questions/742013/how-do-i-create-a-url-shortener)
