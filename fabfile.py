
from fabric.api import run,env, put, get, local, settings
import os
from os import path
import time
from fabric.colors import green as _green, yellow as _yellow
import boto
import boto3
import boto.ec2
import boto.ec2.autoscale
from botocore.exceptions import ClientError

from datetime import datetime, timedelta
from pprint import pprint
from AwsEc2Util import AwsEc2Utilities
from AwsRoute53Util import AwsRoute53Utilities
from AwsAsgUtil import AwsAsgUtilities

awsutil = AwsEc2Utilities()
route53 = AwsRoute53Utilities()
asg = AwsAsgUtilities()



## VPC ##
    
"""Method to get all VPCs via Resource"""
def get_vpcs(profile):

    vpcs = awsutil.get_vpcs(profile)
    
    for vpc in vpcs:
       
        print(dir(vpc))
        print("VPC_ID: " + vpc.vpc_id)

"""Method to describle VPCs via Client"""
def describe_vpcs(profile):

    vpcs = awsutil.describe_vpcs(profile)
    
    for k, v in vpcs.iteritems():
        print(k, v)

"""Method to create a VPC"""
def create_vpc(cidr, profile):
    

    awsutil.create_vpc(cidr, profile)
    


## EC2 ##

"""Method to get an instance by tag"""
"""Usage:  fab get_instancebytag:Name,DevBox2,default """
def get_instancebytag(tagkey, tagvalue, profile):
    
    instance = awsutil.getinstancebytag(profile, tagkey, tagvalue)
   
    tags = instance["Tags"]
           
    print(instance["InstanceType"])   
     
    for x in tags:
        if x["Key"] == 'Name':
            print(x["Value"])
     
         
    print(instance["Placement"]['AvailabilityZone'])

"""Method to start an instance by tag"""
"""Usage: fab start_instance:Name,DevBox2,default""" 
def start_instance(tagkey, tagvalue, profile, region):
       
    session = boto3.Session(profile_name=profile)
    boto3client =  session.client('ec2', region)
 
    instance = awsutil.getinstancebytag(profile, tagkey, tagvalue)


    # Do a dryrun first to verify permissions
    try:
        boto3client.start_instances(InstanceIds=[instance["InstanceId"]], DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, run start_instances without dryrun
    try:
        response = boto3client.start_instances(InstanceIds=[instance["InstanceId"]], DryRun=False)
        print(response)
    except ClientError as e:
        print(e)


"""Method to stop an instance by tag"""
"""Usage: fab stop_instance:Name,DevBox2,default""" 
def stop_instance(tagkey, tagvalue, profile, region):

    
    session = boto3.Session(profile_name=profile)
    boto3client =  session.client('ec2', region)
 

    instance = awsutil.getinstancebytag(profile, tagkey, tagvalue)


    # Do a dryrun first to verify permissions
    try:
        boto3client.stop_instances(InstanceIds=[instance["InstanceId"]], DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, run start_instances without dryrun
    try:
        response = boto3client.stop_instances(InstanceIds=[instance["InstanceId"]], DryRun=False)
        print(response)
    except ClientError as e:
        print(e)


"""Method to stop an instance by tag"""
"""Usage: fab stop_instance:Name,DevBox2,default""" 
def stop_instances(tagkey, tagvalue, profile, region):
    

    session = boto3.Session(profile_name=profile)
    boto3client =  session.client('ec2', region)

    instancefilters = [{'Name':"tag:"+tagkey, 'Values':[tagvalue]} ]
 
    ## Getting Instance info by tag
    instances = awsutil.get_instancesbyfilter(instancefilters, profile)


    for i in instances:
        
       
        for x in i.tags:
            if x["Key"] == "Name":
                print(x["Value"])


        # Do a dryrun first to verify permissions
        try:
            boto3client.stop_instances(InstanceIds=[i.instance_id], DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise

        # Dry run succeeded, run start_instances without dryrun
        try:
            response = boto3client.stop_instances(InstanceIds=[i.instance_id], DryRun=False)
            print(response)
        except ClientError as e:
            print(e)



## Route53  ##

"""Method to update the IP Address of a Hosted Zone Recordset"""
def updaterecordsetip(hostedzonename, recordsetname, ipaddress, profile):  
    
    hostedzoneid = route53.gethostedzoneid(hostedzonename, profile) 

    print(hostedzoneid)

    route53.updateArecordset(hostedzoneid, recordsetname, ipaddress, profile)

"""Method to get Hosted Zone ID"""
def gethostedzoneid(hostedzonename, profile):

    zid = route53.gethostedzoneid(hostedzonename, profile)
    print(zid)


## ASG ###

"""Method to get list all ASGs and the instances they contain"""
def get_asgs(profile):
    
    asg.get_asginstances(profile)
    

"""Method to delete an Autoscaling Group by name with ForceDelete = True"""
def delete_asg(asgname, profile):
    asg.delete_autoscaling_group(asgname, profile)

"""Method to delete a Launch Configuration by Name"""
def delete_launchconfig(lcname, profile):
    asg.delete_launch_configuration(lcname, profile)



