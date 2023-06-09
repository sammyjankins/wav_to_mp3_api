# wav_to_mp3_api

Instructions for building and launching the service.

1. Clone the repository:
```
git clone https://github.com/sammyjankins/wav_to_mp3_api.git
```
2. Go to the project directory:

```
cd your-repo
```
3. Fill the .env file with actual data if necessary.

4. Build and start the containers:

```
docker-compose up -d
```
Console messages example:

![image](https://github.com/sammyjankins/wav_to_mp3_api/assets/26933434/59d374cc-098b-400d-a464-456b31a5edb9)

5. Check that the containers are running:

```
docker ps
```
Console messages example:

![image](https://github.com/sammyjankins/wav_to_mp3_api/assets/26933434/04b5d4b9-0fa1-4387-8f13-9b3ec57ed678)

6. To create a user send a POST request to the address http://localhost:8000/users specifying the username.

Example Curl command:
```
curl -X 'POST' \
  'http://localhost:8000/users' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "TestUser"
}'
```
Response body contains user ID and access token:
```
{
  "user_id": "2772f6ae-9ef8-4853-9dc6-80db856f0825",
  "access_token": "25d17eea-3b7f-435e-835f-b40ac82a6d66"
}
```

7. To save an audio record send a POST request to the address http://localhost:8000/records specifying the user ID, access token and a record file.

Example Curl command (used data from response body above):
```
curl -X 'POST' \
  'http://localhost:8000/record?user_id=2772f6ae-9ef8-4853-9dc6-80db856f0825&access_token=25d17eea-3b7f-435e-835f-b40ac82a6d66' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'audio_file=@file_example_WAV_1MG.wav;type=audio/wav'
```
Response body contains download URL which contains record ID and user ID as parameters:
```
{
  "download_url": "http://localhost:8000/record?record_id=c8d8ebf1-c9a6-413e-9267-8dd922090c78&user_id=2772f6ae-9ef8-4853-9dc6-80db856f0825"
}
```

8. To download converted MP3 audio record use the link received in the response body from the previous step (example from above):

```
http://localhost:8000/record?record_id=c8d8ebf1-c9a6-413e-9267-8dd922090c78&user_id=2772f6ae-9ef8-4853-9dc6-80db856f0825
```


To **connect to the database** type:
```
docker ps
```
then copy the name of the database container (for example "**wav_to_mp3_api-database-1**") and type:
```
docker exec -it <container_name> psql -U <your_db_user> -d <your_db_name>
```
