from boto3 import client,resource
import re
import json
import csv
#tag_client = client('resourcegroupstaggingapi',aws_access_key_id='AKIAYIGLNDQYKR3KRIGE',aws_secret_access_key='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',region_name='us-east-1')
tag_client = client('resourcegroupstaggingapi')
tag_s3_resource =  resource('s3')
def lambda_handler(event,context):
        class ResourceTags:
            
            def __init__(self,ResourceARN,Tags):
                self.arn = ResourceARN
                self._tags = Tags
            
            @classmethod    
            def get_all_resources(cls):
                response = tag_client.get_resources(ResourcesPerPage=100)
                x = response['ResourceTagMappingList']
                tag_count = 0
                while 'PaginationToken' in response and response['PaginationToken']:
                    token = response['PaginationToken']
                    response = tag_client.get_resources(ResourcesPerPage=100, PaginationToken=token)
                    x += response['ResourceTagMappingList']
                
                return sorted(x,key = lambda x: x['ResourceARN'][8:],reverse=False)
                
            
            @classmethod
            def service(cls,service_name,sub_service_name):
                tag_count = 0
                print("sno||service_name||sub_service_name||resource-tag-name||resource-arn||project_id||agency_name||environment_type||alltags")
            
                for service_ref in cls.get_all_resources():
                        tag_count += 1
                        if service_name in service_ref["ResourceARN"] and sub_service_name in service_ref["ResourceARN"]:
                            required_arn = service_ref['ResourceARN']
                            print("{}||{}||{}||{}||{}||{}||{}||{}||{}".format(tag_count,service_name,sub_service_name,cls.get_name(required_arn),service_ref["ResourceARN"],cls.get_project_id(required_arn),cls.get_agency_name(required_arn),cls.get_environment_type(required_arn),cls.tags(required_arn)))
                            
                print("Total Tags count::", tag_count)
                           
            @classmethod
            def tags(cls,required_arn):
                for service_ref in cls.get_all_resources():
                    if service_ref["ResourceARN"] == required_arn:
                       return service_ref['Tags']
            @classmethod
            def get_project_id(cls,required_arn):
                preferred_list=["21","22","23","24"]
                for ref in cls.tags(required_arn):
                    if ref.get('Key') == "project_id" :
                        if ref.get('Value').startswith(tuple(preferred_list)):
                           return ref.get('Value')
                        elif  not ref.get('Value').startswith(tuple(preferred_list)):
                           return f"Wrong Value:{ref.get('Value')}"
                        else:
                           return "Missing"
                return "Missing"    
                    
            @classmethod
            def get_environment_type(cls,required_arn):
                preferred_list=["prod","uat","qa","dev"]
                for ref in cls.tags(required_arn):
                    if ref.get('Key') == "environment-type" :
                        if ref.get('Value').startswith(tuple(preferred_list)):
                           return ref.get('Value')
                        elif  not ref.get('Value').startswith(tuple(preferred_list)):
                           return f"Wrong Value:{ref.get('Value')}" 
                        else:
                           return "Missing"
                return "Missing"    
             
            @classmethod
            def get_agency_name(cls,required_arn):
                preferred_list=["DOH","DLT","EOHHS","DMV","LZ_UTILITY","DOIT","DBR"]
                for ref in cls.tags(required_arn):
                    if ref.get('Key') == "agency-name" :
                        if ref.get('Value').startswith(tuple(preferred_list)):
                           return ref.get('Value')
                        elif  not ref.get('Value').startswith(tuple(preferred_list)):
                           return f"Wrong Value:{ref.get('Value')}"
                        else:
                            return "Missing"
                return "Missing"
                
            @classmethod       
            def get_name(cls,required_arn):
               
                for ref in cls.tags(required_arn):
                    if ref.get('Key') == "Name" :
                        return ref.get('Value')
                return "Missing"
                    
                    
            @staticmethod
            def s3_file_upload(location,bucket,filename):
                tag_s3_resource.meta.client.upload_file(location, bucket,filename)
        
        
        
            @classmethod
            def mandatory_tags_exists(cls,service_name,sub_service_name,tags):
                for service_ref in cls.get_all_resources():
                    if service_name in service_ref['ResourceARN'] and sub_service_name in service_ref['ResourceARN']:
                       all_tags = service_ref['Tags']
                       tag_keys=[]
                       tag_values=[]
                       for tag in all_tags:
                           tag_keys.append(tag["Key"])
                           tag_values.append(tag["Value"])
                           tags_not_present = set(tags) - set(tag_keys)
                           print(service_ref['ResourceARN'],tags_not_present)
               
        all_service_types= [
            ('cloudformation','stack'),('cloudtrail','trail'),('cloudwatch','alarm'), ('config','configrule'), ('dynamodb','table'), ('ec2','dhcpoptions'),
            ('ec2','image'), ('ec2','instance'), ('ec2','internetgateway'), ('ec2','networkacl'), ('ec2','networkinterface'), ('ec2','routetable'), 
            ('ec2','securitygroup'), ('ec2','snapshot'), ('ec2','subnet'), ('ec2','vpc'), ('ec2','volume'), ('events','rule'), ('glue','crawler'), ('kms','key'),
            ('lambda','function'), ('rds','dbinstance'), ('rds','dbparametergroup'), ('rds','dbsecuritygroup'), ('rds','dbsnapshot'), ('rds','dbsubnetgroup'),
            ('rds','eventsubscription'), ('rds','optiongroup'), ('redshift','clustersubnetgroup'), ('s3','bucket'), ('sns','topic'), ('sqs','queue'), 
            ('ssm','parameter'), ('secretsmanager','secret'), ('service','type') ]
        #for k,v in all_service_types:
        #ResourceTags.get_all_resources()
        ResourceTags.service('ec2','instance')
        ResourceTags.service('ec2','subnet')
        ResourceTags.service('s3','aws')
        #return ResourceTags.service('aws','aws')
            
            
        
   
        





