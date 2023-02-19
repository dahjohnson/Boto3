import boto3
import urllib.request

imageid = 'ami-0dfcb1ef8550277af' # Amazon Linux Image
keyname = 'ssh_key' # Enter YOUR ssh key name

client = boto3.client('ec2', region_name='us-east-1')
ec2 = boto3.resource('ec2', region_name='us-east-1')

def createVPC():
    vpc = client.create_vpc(
        CidrBlock='10.0.100.0/24',
        TagSpecifications=[
            {
                'ResourceType': 'vpc',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'CICD_Demo_VPC'
                    }
                ]
            }
        ]
    )

    global vpc_id
    vpc_id = vpc['Vpc']['VpcId']

    subnet = client.create_subnet(
        CidrBlock='10.0.100.0/24',
        VpcId=vpc_id,
        TagSpecifications=[
            {
                'ResourceType': 'subnet',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'CICD_Demo_Subnet'
                    }
                ]
            }
        ]    
    )
    
    global subnet_id
    subnet_id = subnet['Subnet']['SubnetId']

    internet_gateway = client.create_internet_gateway(
        TagSpecifications=[
            {
                'ResourceType': 'internet-gateway',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'CICD_Demo_Internet_Gateway'
                    }
                ]
            }
        ]
    )
    
    attach_internet_gateway = client.attach_internet_gateway(
        InternetGatewayId=internet_gateway['InternetGateway']['InternetGatewayId'],
        VpcId=vpc_id
    )
    
    route_table = client.describe_route_tables(
        Filters=[
            {
                'Name': 'vpc-id',
                'Values': [
                    vpc_id,
                ]
            }
        ]
    )
    
    create_internet_route = client.create_route(
        DestinationCidrBlock='0.0.0.0/0',
        GatewayId=internet_gateway['InternetGateway']['InternetGatewayId'],
        RouteTableId=route_table['RouteTables'][0]['RouteTableId']
        )

def createSecurityGroup():
    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    
    security_group = client.create_security_group(
        Description='Jenkins Security Group',
        GroupName='Jenkins-Server-Security-Group',
        VpcId=vpc_id,
        TagSpecifications=[
            {
                'ResourceType': 'security-group',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'Jenkins-Server-Security-Group'
                    }
                ]
            }
        ]
    )
    
    global security_group_id
    security_group_id = security_group['GroupId']
    
    
    ingress_rule = client.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {
                'FromPort': 0,
                'ToPort': 65535,
                'IpProtocol': 'TCP',
                'IpRanges': [
                    {
                        'CidrIp': external_ip + '/32',
                        'Description': 'my_public_ip'
                    }
                ]
            }
        ]
    )

def createEC2():
    ec2_name = 'Jenkins Server'
    
    user_data = """#!/bin/bash
    # Install Jenkins and Java 
    sudo wget -O /etc/yum.repos.d/jenkins.repo \
        https://pkg.jenkins.io/redhat-stable/jenkins.repo
    sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key
    sudo yum upgrade
    # Add required dependencies for the jenkins package
    sudo amazon-linux-extras install -y java-openjdk11
    # sudo yum install -y java-11-openjdk
    sudo yum install -y jenkins
    sudo systemctl daemon-reload
    
    # Start Jenkins
    sudo systemctl enable jenkins
    sudo systemctl start jenkins
    
    # Firewall Rules
    if [[ $(firewall-cmd --state) = 'running' ]]; then
        YOURPORT=8080
        PERM="--permanent"
        SERV="$PERM --service=jenkins"
    
        firewall-cmd $PERM --new-service=jenkins
        firewall-cmd $SERV --set-short="Jenkins ports"
        firewall-cmd $SERV --set-description="Jenkins port exceptions"
        firewall-cmd $SERV --add-port=$YOURPORT/tcp
        firewall-cmd $PERM --add-service=jenkins
        firewall-cmd --zone=public --add-service=http --permanent
        firewall-cmd --reload
    fi
    """
    
    instance = ec2.create_instances(
        ImageId=imageid,
        InstanceType='t2.micro',
        KeyName=keyname,
        MaxCount=1,
        MinCount=1,
        UserData=user_data,
        IamInstanceProfile={
                'Name': 'JenkinsAccess'
            },
        NetworkInterfaces=[
            {
                'AssociatePublicIpAddress': True,
                'DeleteOnTermination': True,
                'DeviceIndex': 0,
                'SubnetId': subnet_id,
                'Groups': [
                    security_group_id
                ]
            }
        ],
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': ec2_name
                    },
                ]
            }
        ]
    )

createVPC()

createSecurityGroup()

createEC2()
