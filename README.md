# Redis-Pub-Sub

For run this project use this command

uvicorn SNS.api.topic:app --port 8200

For kill process where port 

sudo kill -9 $(sudo lsof -t -i:8200)

