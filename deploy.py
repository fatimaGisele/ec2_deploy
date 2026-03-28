import boto3
import argparse
from datetime import datetime

REGION = "us-east-1"

ec2 = boto3.resource("ec2", region_name = REGION)
ec2_client = boto3.client("ec2", region_name = REGION)

def get_args():
    parser = argparse.ArgumentParser(description='ec2 basic config')
    parser.add_argument("--type", default='t3.micro', help="tipo de instancia")
    parser.add_argument("--name", required=True, help="nombre de la instancia")
    args = parser.parse_args()
    return args


def user_data_script(name): 
    time = datetime.now().strftime("%Y-%m-%d")
    return f"""#!/bin/bash
    yum update -y
    yum install httpd -y
    systemctl start httpd
    systemctl enable httpd
    echo "servidor iniciando correctamente"> /var/www/html/index.html
    echo "nombre de la instancia: {name}"> /var/www/html/index.html
    echo "fecha de creacion: {time}"> /var/www/html/index.html
    """

# def create_security_group():
#     response = ec2.create_security_group(
#         Description = "New security group",
#         GroupName = "hola que tal",
#         VpcId="vpc-xxxxxxxxxx"
#     )
#     sg = response['GroupId']
#     return sg

def get_security_groups_for_vpc():
    response = ec2_client.get_security_groups_for_vpc(
        VpcId="vpc-xxxxxxxx",
        Filters=[
            {"Name": "group-name", "Values": ["hola que tal"]}  
        ]
    )
    hola = response['SecurityGroupForVpcs']
    chau = hola[0]['GroupId']
    return chau

def create_instance(sg_id,type,name):
    user_data = user_data_script(name)
    nueva_instancia = ec2.create_instances(
        ImageId = 'ami-xxxxxxxx',
        MinCount = 1,
        MaxCount = 1,
        InstanceType = type,
        SecurityGroupIds= [sg_id],
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [{'Key': 'Name', 'Value': name}]
            },
        ],
        UserData = user_data
    )
    return nueva_instancia[0]


def wait_instance(instance):
    instance.wait_until_running()
    


def main():
    args = get_args()
    name = args.name
    tipo = args.type

    print("[INFO] Security group...")
    sg_id = get_security_groups_for_vpc()
    print(sg_id)

    print("[INFO] Creando instancia...")
    instance = create_instance(sg_id,tipo, name)

    print("[INFO] Esperando instancia...")
    wait_instance(instance)

    print("[INFO] Obteniendo IP...")
    instance.reload()
    print("IP pública:", instance.public_ip_address)


if __name__ == "__main__":
    main()