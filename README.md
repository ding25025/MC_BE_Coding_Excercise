# Take Home API Practice
- Implement a Restful task list API
  - Create
  - Retrieve
  - Update
  - Delete
  
## How to open api document

http://127.0.0.1:5002/apidocs

## How to run task api
```
python3 app.py

```
## How to build docker image

```
docker image build -t taskapi_test .

```
 
## How to run docker image

```
docker run --restart=always -p 5002:5002  --network=host -t taskapi_test

```

## Improve
- This not for production enviroment. You need to fix the Dockerfile. 

