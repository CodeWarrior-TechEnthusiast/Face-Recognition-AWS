<h2>Build instructions</h2>

<h3>Building docker container image and pushing to AWS</h3>

<h4>Build docker container image</h4>

```bash
docker build -t cse546/face_recognition:0.1 .
```

<h4>Run container locally for testing</h4>

```bash
docker run -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} -e AWS_DEFAULT_REGION=us-east-1 --env-file=src/captureFrames/mq.env -p 9000:8080 cse546/face_recognition:0.1
```

<h4>Tag the container</h4>
```bash
docker tag 2f89879c6908 601153112733.dkr.ecr.us-east-1.amazonaws.com/cse546/face_recognition:0.1
```

<h4>Push the container image to ECR</h4>
```bash
docker push 601153112733.dkr.ecr.us-east-1.amazonaws.com/cse546/face_recognition:0.1
```

<h3>Running video recording on Raspberry PI</h3>

<h4>Export Environment variables
```bash
cd captureFrames
source env.sh
export STORE_TO_S3=1
```

<h4>Record video from raspberry PI camera</h4>
```bash
python3 captureFrames.py
```
