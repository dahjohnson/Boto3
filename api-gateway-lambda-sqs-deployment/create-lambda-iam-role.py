import boto3
import json

lambda_role_name = 'Lambda-SQS-Execution-Role'
lambda_policy_name = 'Lambda-SQS-Execution-Policy'

trust_relationship_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}

permission_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Sid": "CloudWatch",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
                ],
            "Resource": "arn:aws:logs:*"
        },
        {
            "Effect": "Allow",
            "Sid": "SQS",
            "Action": "sqs:SendMessage",
            "Resource": "arn:aws:sqs:*"
        }
    ]
}

iam = boto3.client('iam')

lambda_role = iam.create_role(
  RoleName= lambda_role_name,
  AssumeRolePolicyDocument=json.dumps(trust_relationship_policy)
)

lambda_policy = iam.create_policy(
    PolicyName= lambda_policy_name,
    PolicyDocument=json.dumps(permission_policy)
)

attach_policy = iam.attach_role_policy(
    PolicyArn=lambda_policy['Policy']['Arn'],
    RoleName= lambda_role_name,
)

role_create_date = lambda_role['Role']['CreateDate']

print(f"The Lambda Execution Role \"{lambda_role_name}\" was created on \"{role_create_date}.\"")