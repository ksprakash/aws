import boto3
from termcolor import colored

ec2=boto3.resource('ec2')
vpc_list = [ vpc.id for vpc in ec2.vpcs.all() ]
for vpc in vpc_list:
    for instance in ec2.instances.all():
        if instance.vpc.id == vpc:
            security=[]
            for sg in instance.security_groups:
                security.append((sg.get('GroupName'),sg.get('GroupId')))
            volumes=[]
            for volume in instance.block_device_mappings:
                volumes.append((volume.get('DeviceName'),volume.get('Ebs').get('VolumeId')))
                #volumes.append(volume)
            print(instance.vpc.id,instance.id,instance.state.get('Name'),instance.instance_type,instance.subnet_id,instance.private_ip_address,instance.public_ip_address,instance.key_name,instance.launch_time,volumes,security)
            
    
