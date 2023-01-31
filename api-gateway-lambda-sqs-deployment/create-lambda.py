import boto3

lambda_role_name = 'Lambda-SQS-Execution-Role'
lambda_function_name = 'api_sqs_sns_function'

lambda_function = boto3.client('lambda')
iam = boto3.client('iam')

lambda_execution_role = iam.get_role(
    RoleName=lambda_role_name
)

create_lambda = lambda_function.create_function(
    FunctionName=lambda_function_name,
    Runtime='python3.9',
    Role=lambda_execution_role['Role']['Arn'],
    Handler='lambda-function.lambda_handler',
    Code={'ZipFile': open('lambda-function.zip', 'rb').read()},
    Publish=True,
    PackageType='Zip'
)

print(f"Lambda function: {lambda_function_name}")
print('State: ' + create_lambda['State'])
print('Reason: ' + create_lambda['StateReason'])