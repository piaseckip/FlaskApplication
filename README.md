
<h2 align="center">Piotr Piasecki Portfolio</h2>

---
<p align="center"> Application where you can show tech stack that you are using.
    <br> 
</p>

## Demo view

![Demo view](demo.png?raw=true "Demo view")

##  About 

Simple 3-tier python based application in Flask, storing data in mongoDB and using Nginx as HTTP server.

##  Getting Started 
 To download a project

```
git clone <repo>
```

### Prerequisites

To run the project u will need:

```
1. docker
2. docker-compose
```

### Installing

To run application locally, just type command in terminal:

```
docker-compose --build -d
```

##  Running the tests 

Tests are checking basic endpoints of the app - home, adding and deleting.

```
docker exec flask python e2e_test.py
```

##  Usage 

In the application u can add,edit and delete informationa about your tech stack.

##  Built Using 
-  Nginx - HTTP server
-  Flask - Python Application
-  MongoDB - Database

##  Authors 

- [@Piotr_Piasecki](https://github.com/piaseckip) 


##  Acknowledgements 

- Build as the develeap Portfolio
