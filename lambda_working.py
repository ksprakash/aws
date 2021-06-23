from boto3 import client,resource
import re
import json
import csv
#tag_client = client('resourcegroupstaggingapi',aws_access_key_id='*************',aws_secret_access_key='******************',region_name='us-east-1')
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
                new_response=[]
                while 'PaginationToken' in response and response['PaginationToken']:
                    token = response['PaginationToken']
                    response = tag_client.get_resources(ResourcesPerPage=100, PaginationToken=token)
                    new_response += response['ResourceTagMappingList']
                return new_response
                
            
            @classmethod
            def service(cls,service_name,sub_service_name):
                for service_ref in cls.get_all_resources():
                        if service_name in service_ref["ResourceARN"] and sub_service_name in service_ref["ResourceARN"]:
                            required_arn = service_ref['ResourceARN']
                            print("{}||{}||{}||{}||{}||{}||{}||{}".format(service_name,sub_service_name,cls.get_name(required_arn),service_ref["ResourceARN"],cls.get_project_id(required_arn),cls.get_agency_name(required_arn),cls.get_environment_type(required_arn),cls.tags(required_arn)))
                           
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
                           return "Wrong Value"
                        else:
                           return "Missing"
                    
                    
            @classmethod
            def get_environment_type(cls,required_arn):
                preferred_list=["prod","uat","qa","dev"]
                for ref in cls.tags(required_arn):
                    if ref.get('Key') == "environment-type" :
                        if ref.get('Value').startswith(tuple(preferred_list)):
                           return ref.get('Value')
                        elif  not ref.get('Value').startswith(tuple(preferred_list)):
                           return "Wrong Value"
                        else:
                           return "Missing"
                    
             
            @classmethod
            def get_agency_name(cls,required_arn):
                preferred_list=["DOH","DLT","EOHHS","DMV","LZ_UTILITY","DOIT","DBR"]
                for ref in cls.tags(required_arn):
                    if ref.get('Key') == "agency-name" :
                        if ref.get('Value').startswith(tuple(preferred_list)):
                           return ref.get('Value')
                        elif  not ref.get('Value').startswith(tuple(preferred_list)):
                           return "Wrong Value"
                        else:
                            return "Missing"
            @classmethod       
            def get_name(cls,required_arn):
               
                for ref in cls.tags(required_arn):
                    if ref.get('Key') == "Name" :
                        return ref.get('Value')
                    
                    
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
               
        return ResourceTags.service('ec2','instance')
            
            
        
   
        





