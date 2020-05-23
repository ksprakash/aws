import boto3
import boto3
import collections
from datetime import datetime
import calendar

client = boto3.client('cloudwatch')
ec = boto3.client('ec2')

env_name="EC2:Dev:"
ec2_sns="arn:aws-us-gov:sns:us-gov-west-1:828541748511:AlertDevEc2"
server_list=['*81*','*80*']

#env_name="EC2:Test:"
#ec2_sns="arn:aws-us-gov:sns:us-gov-west-1:828541748511:AlertTstEc2"
#server_list=['*61*']

#env_name="EC2:PreProd:"
#ec2_sns="arn:aws-us-gov:sns:us-gov-west-1:828541748511:AlertPPrEc"
#server_list=['*41*']

#env_name="EC2:Perf:"
#ec2_sns="arn:aws-us-gov:sns:us-gov-west-1:828541748511:AlertPerEc"
#server_list=['*71*']

#env_name="EC2:Prod:"
#ec2_sns="arn:aws-us-gov:sns:us-gov-west-1:828541748511:AlertPrdEc"
#server_list=['*20*','*21*']

#alert_level="MEDIUM"
#CPU_int="80%"
#CPU_Threshold=80.0
#RAM_int="80%"
#RAM_Threshold=80.0
#DISK_Space="80%"
#DISK_Space_Threshold=80.0

alert_level="HIGH"
CPU_int="90%"
CPU_Threshold=90.0
RAM_int="90%"
RAM_Threshold=90.0
DISK_Space="90%"
DISK_Space_Threshold=90.0

region='aws-us-gov'
def lambda_handler(event, context):
    reservations = ec.describe_instances(Filters=[
            {
                'Name': 'tag:Name',
                'Values': server_list
            }
        ])
    for r in reservations['Reservations']:
             for i in r['Instances']:
                 instance_id = i['InstanceId']
                 for t in i['Tags']:
                    if t['Key'] == 'Name':
                        iname = t['Value']
                        cpu_alarm = client.put_metric_alarm(
                        AlarmName=alert_level + '-' + env_name + iname + '-CPU Utilization >=' + CPU_int ,
						AlarmDescription=alert_level + '-' + env_name + iname + '-CPU Utilization >=' + CPU_int ,
                        MetricName='CPUUtilization',
                        Namespace='AWS/EC2',
                        Statistic='Average',
                        ComparisonOperator='GreaterThanOrEqualToThreshold',
                        Threshold=CPU_Threshold,
                        Period=300,
                        EvaluationPeriods=2,
                        Dimensions=[
                            {
                                'Name': 'InstanceId',
                                'Value': instance_id
                            }
                        ],
                        Unit='Percent',
                        ActionsEnabled=True,
                        AlarmActions=[
                            ec2_sns 
                        ]
						)
                        system_status_alarm=client.put_metric_alarm(
                        AlarmName='HIGH-' + env_name + iname +"-System Check Failed",
                        AlarmDescription='HIGH-' + env_name + iname +"-System Check Failed",
                        ActionsEnabled=True,
                        AlarmActions=[
                                    ec2_sns
                                      ],
                        MetricName='StatusCheckFailed_System',
                        Namespace='AWS/EC2',
                        Statistic='Average',
                        Dimensions=[
                                   {
                                     'Name': 'InstanceId',
                                     'Value': instance_id
                                   },
                                   ],
                        Period=300,
                        EvaluationPeriods=2,
                        Threshold=1.0,
                        ComparisonOperator='GreaterThanOrEqualToThreshold'
                        )
                        instance_status_alarm = client.put_metric_alarm(
                        AlarmName='HIGH-' + env_name + iname +"-Instance Check Failed",
                        AlarmDescription='HIGH-' + env_name + iname +"-Instance Check Failed",
                        ActionsEnabled=True,
                        AlarmActions=[
                                    ec2_sns
                        ],
                        MetricName='StatusCheckFailed_Instance',
                        Namespace='AWS/EC2',
                        Statistic='Average',
                        Dimensions=[
                                   {
                                     'Name': 'InstanceId',
                                     'Value': instance_id
                                   },
                                   ],
                        Period=300,
                        EvaluationPeriods=2,
                        Threshold=1.0,
                        ComparisonOperator='GreaterThanOrEqualToThreshold'
                        )  
                        disk_space_root_alarm = client.put_metric_alarm(
                        AlarmName=alert_level + '-' + env_name + iname + '-Root-Disk Space>=' + DISK_Space,
                        AlarmDescription=alert_level + '-' + env_name + iname + '-Root-Disk Space>=' + DISK_Space,
                        ActionsEnabled=True,
                        AlarmActions=[
                                    ec2_sns
                        ],
                        MetricName='DiskSpaceUtilization',
                        Namespace='System/Linux',
                        Statistic='Average',
                        Dimensions=[
                                   {
                                     'Name': 'InstanceId',
                                     'Value': instance_id
                                   },
                                   {
                                        'Name': 'MountPath',
                                        'Value': '/'
                                       
                                   },
                                   {
                                     'Name': 'Filesystem',
                                     'Value': '/dev/xvda2'
                                   }
                                   ],
						Unit='Percent',
						Period=300,
                        EvaluationPeriods=2,
                        Threshold=DISK_Space_Threshold,
                        ComparisonOperator='GreaterThanOrEqualToThreshold'
                        )
                        disk_space_xvdc_alarm = client.put_metric_alarm(
                        AlarmName=alert_level + '-' + env_name + iname +  '-Disk2-xvdc1-Disk Space>=' + DISK_Space,
                        AlarmDescription=alert_level + '-' + env_name + iname +  '-Disk2-xvdc1-Disk Space>=' + DISK_Space,
                        ActionsEnabled=True,
                        AlarmActions=[
                                    ec2_sns
                        ],
                        MetricName='DiskSpaceUtilization',
                        Namespace='System/Linux',
                        Statistic='Average',
                        Dimensions=[
                                   {
                                     'Name': 'InstanceId',
                                     'Value': instance_id
                                   },
                                   {
                                        'Name': 'MountPath',
                                        'Value': '/u01'
                                       
                                   },
                                   {
                                     'Name': 'Filesystem',
                                     'Value': '/dev/xvdc1'
                                   }
                                   ],
                        Unit='Percent',
						Period=300,
                        EvaluationPeriods=2,
                        Threshold=DISK_Space_Threshold,
                        ComparisonOperator='GreaterThanOrEqualToThreshold'
                        )
                        disk_space_xvdb_alarm = client.put_metric_alarm(
                        AlarmName=alert_level + '-' + env_name + iname +  '-Disk3-xvdb-Disk Space>=' + DISK_Space,
                        AlarmDescription=alert_level + '-' + env_name + iname +  '-Disk3-xvdb-Disk Space>=' + DISK_Space,
                        ActionsEnabled=True,
                        AlarmActions=[
                                    ec2_sns
                        ],
                        MetricName='DiskSpaceUtilization',
                        Namespace='System/Linux',
                        Statistic='Average',
                        Dimensions=[
                                   {
                                     'Name': 'InstanceId',
                                     'Value': instance_id
                                   },
                                   {
                                        'Name': 'MountPath',
                                        'Value': '/opt'
                                       
                                   },
                                   {
                                     'Name': 'Filesystem',
                                     'Value': '/dev/xvdb'
                                   }
                                   ],
                        Unit='Percent',
						Period=300,
                        EvaluationPeriods=2,
                        Threshold=DISK_Space_Threshold,
                        ComparisonOperator='GreaterThanOrEqualToThreshold'
                        )
                        mem_usage=client.put_metric_alarm(
                        AlarmName=alert_level + '-' + env_name + iname +  '-Memory Utilization(RAM) >=' + DISK_Space,
                        AlarmDescription=alert_level + '-' + env_name + iname +  '-Memory Utilization(RAM) >=' + DISK_Space,
                        ActionsEnabled=True,
                        AlarmActions=[
                                    ec2_sns
                        ],
                        MetricName='MemoryUtilization',
                        Namespace='System/Linux',
                        Statistic='Average',
                        Dimensions=[
                                   {
                                     'Name': 'InstanceId',
                                     'Value': instance_id
                                   }
                                  ],
                        Period=300,
                        EvaluationPeriods=2,
                        Threshold=DISK_Space_Threshold,
                        ComparisonOperator='GreaterThanOrEqualToThreshold'
                        )