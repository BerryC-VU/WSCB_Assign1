# RESTFUL Service - URL shortening service

**University of Amsterdam Web Services and Cloud-Based System Assignment 1**

In this project, we aim to implement the following functions:

| Path & Method | Functionality                          | Return values                                                                    |   |   |
|---------------|----------------------------------------|----------------------------------------------------------------------------------|---|---|
| /:id & GET    | Return URL corresponds to the given id | 301, if id exists 404, otherwise                                                 |   |   |
| /:id & PUT    | Update URL based on given id           | 200, if id exists and URL valid 400, if id exists and URL invalid 404, otherwise |   |   |
|               |                                        |                                                                                  |   |   |

**Create Environment**

Run the following code to configure the environment:
```
conda env create -f environment.yml
conda avtivate web1
```

**Run the server**

 ```
 python3 main.py
 ```


**Run the Demo** 

There are four demo files under the demos folder. Users can test what they want using existing `demo*.sh` or create some new requests
To test all specifications, run the following code in the PATH  for an example:
```
./demos/demo*.sh > ./results/demo*_res.txt
```
