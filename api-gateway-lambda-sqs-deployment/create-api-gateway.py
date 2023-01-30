import boto3
import random
import string

lambda_function_name = 'api_sqs_sns_function'
api_gateway_name = 'demo-api-gateway-luit-2023'

id_num = ''.join(random.choices(string.digits, k=7))

api_gateway = boto3.client('apigatewayv2')
lambda_function = boto3.client('lambda')

lambda_function_get = lambda_function.get_function(
    FunctionName=lambda_function_name
)

api_gateway_create = api_gateway.create_api(
    Name=api_gateway_name,
    ProtocolType='HTTP',
    Version='1.0',
    RouteKey='ANY /',
    Target=lambda_function_get['Configuration']['FunctionArn']
)

api_gateway_permissions = lambda_function.add_permission(
    FunctionName=lambda_function_name,
    StatementId='api-gateway-permission-statement-'+id_num,
    Action='lambda:InvokeFunction',
    Principal='apigateway.amazonaws.com',
)

print("API Endpoint:", api_gateway_create['ApiEndpoint'])