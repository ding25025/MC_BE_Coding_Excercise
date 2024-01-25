# Task API Practice

## api document

http://127.0.0.1:5002/apidocs

## build docker image

```
docker image build -t taskapi_test .

```
 
## run docker image

```
docker run --restart=always -p 5002:5002  --network=host -t taskapi_test

```