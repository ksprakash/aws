import boto3
import csv
ec2=boto3.resource('ec2',aws_access_key_id='',aws_secret_access_key='')
rds=boto3.client('rds',aws_access_key_id='',aws_secret_access_key='')
ec2_client =boto3.client('ec2',aws_access_key_id='',aws_secret_access_key='')
response = rds.describe_db_instances()
sg_response = ec2_client.describe_security_groups()
vpc_list = [ vpc.id for vpc in ec2.vpcs.all() ]
fields = ['VPC_ID', 'INSTANCE_NAME', 'INSTANCE_ID', 'STATE', 'TYPE', 'SUBNET' , 'PRIVATE_IP', 'PUBLIC_IP','KEY_NAME','LAUNCH_TIME','VOLUMES','SECURITY'] 
filename = 'ec2_resources.csv'
with open(filename, 'w',newline='') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile) 
        
    # writing the fields 
    csvwriter.writerow(fields)
    set_ec2=[]
    for vpc in vpc_list:
        for instance in ec2.instances.all():
            if instance.vpc_id == vpc:
                name = list(filter(lambda x: x.get('Key') == 'Name',instance.tags))
                security=[]
                for sg in instance.security_groups:
                    security.append((sg.get('GroupName'),sg.get('GroupId')))
                volumes=[]
                for volume in instance.block_device_mappings:
                    volumes.append((volume.get('DeviceName'),volume.get('Ebs').get('VolumeId')))
                    volumes.append(volume)
                set_ec2.append([instance.vpc_id,name,instance.id,instance.state.get('Name'),instance.instance_type,instance.subnet_id,instance.private_ip_address,instance.public_ip_address,instance.key_name,instance.launch_time,volumes,security])
        csvwriter.writerows(set_ec2)  
        print(set_ec2)    
        for r in response['DBInstances']:
            if r['DBSubnetGroup']['VpcId'] == vpc:
                print(r['DBSubnetGroup']['VpcId'],r['DBInstanceIdentifier'],r['DBInstanceClass'],r['AllocatedStorage'],r['Endpoint'].get('Address'),r['AvailabilityZone'],r['Iops'],r['ListenerEndpoint']['Port'],r['Engine'],r['MasterUsername'],r['VpcSecurityGroups'],r['DBSubnetGroup']['Subnets'])
        for sg in sg_response['SecurityGroups']:
            if sg.get('VpcId') == vpc:
                print(sg.get('VpcId'),sg.get('GroupId'),sg.get('GroupName'))    

