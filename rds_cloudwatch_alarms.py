EC2 PROD Dash Board:
https://console.amazonaws-us-gov.com/cloudwatch/home?region=us-gov-west-1#dashboards:name=EC2-PROD-Dashboard;accountId=828541748511



import boto3
import collections
from datetime import datetime
import calendar

rds_name="vac10dbspas210"
#server_type="OLTP:"
#server_type="OLAP:"
server_type="Mule:"


#env_name="RDS:Dev:"
#rds_sns="arn:aws-us-gov:sns:us-gov-west-1:828541748511:AlertDevRDS"

#env_name="RDS:Test:"
#rds_sns="arn:aws-us-gov:sns:us-gov-west-1:828541748511:AlertTstRD"

#env_name="EC2:PreProd:"
#rds_sns="arn:aws-us-gov:sns:us-gov-west-1:828541748511:AlertPPrRD"

#env_name="EC2:Perf:"
#rds_sns="arn:aws-us-gov:sns:us-gov-west-1:828541748511:AlertPerRD"

env_name="EC2:Prod:"
rds_sns="arn:aws-us-gov:sns:us-gov-west-1:828541748511:AlertPrdRD"

client = boto3.client('cloudwatch')
rds = boto3.client('rds')

response = rds.describe_db_instances()

def lambda_handler(event, context):
	for r in response['DBInstances']:

			rds_id = r['DBInstanceIdentifier']
			if rds_id == rds_name :
							cpu_alarm80 = client.put_metric_alarm(
							AlarmName='MEDIUM-' + env_name + server_type + rds_id + '-CPU Utilization >=80%',
							AlarmDescription= 'MEDIUM-' + env_name + server_type + rds_id + '-CPU Utilization >=80%',
							MetricName='CPUUtilization',
							Namespace='AWS/RDS',
							Statistic='Average',
							ComparisonOperator='GreaterThanOrEqualToThreshold',
							Threshold=80.0,
							Period=300,
							EvaluationPeriods=2,
							Dimensions=[
								{
									'Name': 'DBInstanceIdentifier',
									'Value': rds_id
								}
							],
							Unit='Percent',
							ActionsEnabled=True,
							AlarmActions=[
								rds_sns 
							]
							)
							
							cpu_alarm90 = client.put_metric_alarm(
							AlarmName='HIGH-' + env_name + server_type + rds_id + '-CPU Utilization >=90%',
							AlarmDescription= 'HIGH-' + env_name + server_type + rds_id + '-CPU Utilization >=90%',
							MetricName='CPUUtilization',
							Namespace='AWS/RDS',
							Statistic='Average',
							ComparisonOperator='GreaterThanOrEqualToThreshold',
							Threshold=90.0,
							Period=300,
							EvaluationPeriods=2,
							Dimensions=[
								{
									'Name': 'DBInstanceIdentifier',
									'Value': rds_id
								}
							],
							Unit='Percent',
							ActionsEnabled=True,
							AlarmActions=[
								rds_sns 
							]
							)
							
							mem_usage1=client.put_metric_alarm(
							AlarmName='MEDIUM-' + env_name + server_type + rds_id + '-Memory(RAM) Available<10GB' ,
							AlarmDescription='MEDIUM-' + env_name + server_type + rds_id + '-Memory(RAM) Available<10GB' ,
							ActionsEnabled=True,
							AlarmActions=[
										rds_sns
							],
							MetricName='FreeableMemory',
							Namespace='AWS/RDS',
							Statistic='Average',
							Dimensions=[
									   {
										 'Name': 'DBInstanceIdentifier',
										 'Value': rds_id
									   }
									  ],
							Period=300,
							EvaluationPeriods=2,
							Threshold=10485760000.0,
							ComparisonOperator='LessThanOrEqualToThreshold'
							)
							
							mem_usage2=client.put_metric_alarm(
							AlarmName='HIGH-' + env_name + server_type + rds_id + '-Memory(RAM) Available<5GB' ,
							AlarmDescription='HIGH-' + env_name + server_type + rds_id + '-Memory(RAM) Available<5GB' ,
							ActionsEnabled=True,
							AlarmActions=[
										rds_sns
							],
							MetricName='FreeableMemory',
							Namespace='AWS/RDS',
							Statistic='Average',
							Dimensions=[
									   {
										 'Name': 'DBInstanceIdentifier',
										 'Value': rds_id
									   }
									  ],
							Period=300,
							EvaluationPeriods=2,
							Threshold=5242880000.0,
							ComparisonOperator='LessThanOrEqualToThreshold'
							)
							
							disk_usage300=client.put_metric_alarm(
							AlarmName='LOW-' + env_name + server_type + rds_id + '-Free Disk Space <=300GB' ,
							AlarmDescription='LOW-' + env_name + server_type + rds_id + '-Free Disk Space <=300GB' ,
							ActionsEnabled=True,
							AlarmActions=[
										rds_sns
							],
							MetricName='FreeStorageSpace',
							Namespace='AWS/RDS',
							Statistic='Average',
							Dimensions=[
									   {
										 'Name': 'DBInstanceIdentifier',
										 'Value': rds_id
									   }
									  ],
							Period=300,
							EvaluationPeriods=2,
							Threshold=314572800.0,
							ComparisonOperator='LessThanOrEqualToThreshold'
							)
							
							disk_usage200=client.put_metric_alarm(
							AlarmName='MEDIUM-' + env_name + server_type + rds_id + '-Free Disk Space <=200GB' ,
							AlarmDescription='MEDIUM-' + env_name + server_type + rds_id + '-Free Disk Space <=200GB' ,
							ActionsEnabled=True,
							AlarmActions=[
										rds_sns
							],
							MetricName='FreeStorageSpace',
							Namespace='AWS/RDS',
							Statistic='Average',
							Dimensions=[
									   {
										 'Name': 'DBInstanceIdentifier',
										 'Value': rds_id
									   }
									  ],
							Period=300,
							EvaluationPeriods=2,
							Threshold=209715200.0,
							ComparisonOperator='LessThanOrEqualToThreshold'
							)
							
							disk_usage100=client.put_metric_alarm(
							AlarmName='HIGH-' + env_name + server_type + rds_id + '-Free Disk Space <=100GB' ,
							AlarmDescription='HIGH-' + env_name + server_type + rds_id + '-Free Disk Space <=100GB' ,
							ActionsEnabled=True,
							AlarmActions=[
										rds_sns
							],
							MetricName='FreeStorageSpace',
							Namespace='AWS/RDS',
							Statistic='Average',
							Dimensions=[
									   {
										 'Name': 'DBInstanceIdentifier',
										 'Value': rds_id
									   }
									  ],
							Period=300,
							EvaluationPeriods=2,
							Threshold=104857600.0,
							ComparisonOperator='LessThanOrEqualToThreshold'
							)
							