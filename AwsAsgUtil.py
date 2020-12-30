import boto3

class AwsAsgUtilities:
    
    def basictest(self, m):
        m = "new message"
        return m
     
    """Method to get instances attached to an Autoscaling Group"""
    def get_asginstances(self, profile):
   
        session = boto3.Session(profile_name=profile)
        asginstances = {}
        client = session.client('autoscaling')
        response = client.describe_auto_scaling_instances()
        for i in response["AutoScalingInstances"]:
            print(i["AutoScalingGroupName"], i["InstanceId"])
            asginstances.setdefault(i["AutoScalingGroupName"],[]).append(i["InstanceId"])
        return asginstances
   
    """Method to delete an ASG with a ForceDelete=True"""
    def delete_autoscaling_group(self, asgname, profile):
        session = boto3.Session(profile_name=profile)
        client = session.client('autoscaling')
        response = client.delete_auto_scaling_group(
        AutoScalingGroupName=asgname,
        ForceDelete=True
        )

    """Method to delete a Launch Configuration by name"""
    def delete_launch_configuration(self, lcname, profile):
        session = boto3.Session(profile_name=profile)
        client = session.client('autoscaling')
        response = client.delete_launch_configuration(
        LaunchConfigurationName=lcname,
        )

        

   
           

         

        

