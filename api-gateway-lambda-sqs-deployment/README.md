<h1 align="center">Deploy API Gateway, Lambda, and SQS with Python SDK (Boto3)</h1>

![aws-deployment-cover](https://user-images.githubusercontent.com/116639830/218316337-530189bb-9ed9-470c-8601-671720f41202.png)

- [Medium Blog Walkthrough](https://medium.com/towards-aws/deploy-api-gateway-lambda-and-sqs-with-python-sdk-boto3-69e38985b69e "<deploy-api-gateway-lambda-and-sqs-with-python-sdk-boto3-69e38985b69e> Medium Blog Walkthrough")
  
## Objectives:

### - Create a Standard SQS Queue using Python
### - Create a Lambda function using Python
### - Modify the Lambda to send a message that returns the current time (UTC) to the SQS queue
### - Create an API gateway HTTP API type trigger using Python
### - Test the trigger to verify the message was sent

## Commands

### Install Bobo3
`pip install boto3`

### Create the SQS queue and notate the output for the Queue URL
`python3 create-sqs.py`

### Create Lambda IAM role 
`python3 create-lambda-iam-role.py`

### Add Queue URL to lambda-function.py and zip the file
`zip lambda-function.zip lambda-function.py`

### Create Lambda Function 
`python3 create-lambda.py`

### Create API Gateway and notate the API Endpoint URL
`python3 create-api-gateway.py`

### Verify Lambda trigger 
`curl <API Endpoint URL>`

### Poll SQS queue
`python3 poll-sqs-queue.py`
