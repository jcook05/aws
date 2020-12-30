import boto3

class AwsEc2Utilities:
            
    def basictest(self, m):
        m = "new message"
        return m    

### VPC ###   
    """Method to get all VPCs"""
    def get_vpcs(self, profile):
        session = boto3.Session(profile_name=profile)
        ec2 = boto3.resource("ec2", region_name="us-west-2")     
        my_vpcs = ec2.vpcs.all()
        return my_vpcs

    """Method to describe VPCs """
    def describe_vpcs(self,profile):
        session = boto3.Session(profile_name=profile)
        ec2 = session.client('ec2')
        my_vpcs = ec2.describe_vpcs()
        return my_vpcs

    """ Method to create a VPC with the default tenancy"""
    def create_vpc(self, cidr, profile):
        session = boto3.Session(profile_name=profile)
        ec2 = session.client('ec2')
        vpc = ec2.create_vpc(
        CidrBlock=cidr,
        AmazonProvidedIpv6CidrBlock=False,
        DryRun=False,
        InstanceTenancy='default'
        )

### EC2 ###
    """Method to delete an instance by tag"""
    def getinstancebytag(self, profile, tagkey, tagvalue):
          session = boto3.Session(profile_name=profile)
          ec2 = session.client('ec2')
          ## Get All Reservations
          response = ec2.describe_instances()
          ## Get Instances
          instances = [i for r in response["Reservations"] for i in r["Instances"]]           
          for i in instances:
             tags = i["Tags"]
             ## Get Name
             for x in tags:
                 if x["Key"] == tagkey and x["Value"] == tagvalue:
                     return i

    
    """Boto3 Method to get instances by filters"""
    def get_instancesbyfilter(self, filters, profile):
        session = boto3.Session(profile_name=profile)
        boto3conn = session.resource("ec2", region_name="us-west-2")
        instances = boto3conn.instances.filter(Filters=filters)
        return instances

    """Method to get instances attached to ASGs"""
    def getinstanceinasg(self, profile):
         session = boto3.Session(profile_name=profile)
         ec2 = session.client('autoscaling')
         ## Get All Reservations
         response = ec2.describe_auto_scaling_groups()
         ## Get Instances
         instances = [i for r in response["AutoScalingGroups"] for i in r["Instances"]]            
         for i in instances:  
           print(i["InstanceId"])


    """Sample method that gets some basic information from Instances"""
    def describeinstances(self, profile):
         session = boto3.Session(profile_name=profile)
         ec2 = session.client('ec2')
         ## Get All Reservations
         response = ec2.describe_instances()
         ## Get Instances
         instances = [i for r in response["Reservations"] for i in r["Instances"]]          
         for i in instances:
            tags = i["Tags"]
            print(i["InstanceType"])   
            ## Get Name
            for x in tags:
                if x["Key"] == 'Name':
                    print(x["Value"])
            ## Get Availability Zone
            print(i["Placement"]['AvailabilityZone'])


    
     

  
           

         

        

