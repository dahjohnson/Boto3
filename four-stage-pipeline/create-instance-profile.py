import boto3
import json

iam = boto3.client('iam')

def createInstanceProfile():
    ec2_jenkins_role_name = 'JenkinsAccess'
    ec2_jenkins_policy_name = 'AWSCodePipelineCustomActionAccess'
    
    assume_role_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "sts:AssumeRole"
                ],
                "Principal": {
                    "Service": [
                        "ec2.amazonaws.com"
                    ]
                }
            }
        ]
    }
    
    try:
        ec2_role = iam.create_role(
            RoleName=ec2_jenkins_role_name,
            AssumeRolePolicyDocument=json.dumps(assume_role_policy)
        )
    
        ec2_role_permissions = iam.attach_role_policy(
            RoleName=ec2_jenkins_role_name,
            PolicyArn='arn:aws:iam::aws:policy/AWSCodePipelineCustomActionAccess'
        )
    except Exception as e:
        print(e)
    else:
        return(f"The role \"{ec2_role['Role']['RoleName']}\" has successfully been created.")
        
print(createInstanceProfile())
