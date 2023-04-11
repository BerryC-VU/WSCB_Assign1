# RESTFUL Service - URL shortening service

**University of Amsterdam Web Services and Cloud-Based System Assignment 1**

In this project, we aim to implement the following functions:

| Path & Method | Functionality                          | Return values                                                                    |   |   |
|---------------|----------------------------------------|----------------------------------------------------------------------------------|---|---|
| /:id & GET    | Return URL corresponds to the given id | 301, if id exists 404, otherwise                                                 |   |   |
| /:id & PUT    | Update URL based on given id           | 200, if id exists and URL valid 400, if id exists and URL invalid 404, otherwise |   |   |
|               |                                        |                                                                                  |   |   |

** Environment requirment **
```bash
conda environment.yml
```bash

* Run the server *
 ```bash
 python3 main.py
 ```bash


** Demo ** 
To test all specifications, run the following code for an example:
```bash
./demos/demo1.sh > ./results/demo1_res.txt
```bash
