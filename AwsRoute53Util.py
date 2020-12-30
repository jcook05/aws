import boto3

class AwsRoute53Utilities:
      
    def basictest(self, m):
        m = "new message"
        return m
    """Method to get Hosted Zone ID"""
    def gethostedzoneid(self, domainname, profile):
        ## Setup boto3 client with route53
        session = boto3.Session(profile_name=profile)
        boto3client =  session.client('route53')
        zones = boto3client.list_hosted_zones()
        for x in zones["HostedZones"]:
            if x["Name"] == domainname:
                ## May want to refactor
                zid = x["Id"].split('/')[2]
        print(zid)
        return zid
      
    """ Method to Update IP Address of a recordset""" 
    def updateArecordset(self, hostedzoneid, record_name, ipaddress, profile):
        session = boto3.Session(profile_name=profile)
        ## Setup boto3 client with route53
        boto3client =  session.client('route53') 
        ## Perform UPSERT Action
        response = boto3client.change_resource_record_sets(
        HostedZoneId=hostedzoneid,
        ChangeBatch={
        "Comment": "Automatic DNS update",
        "Changes": [
            {
                "Action": "UPSERT",
                "ResourceRecordSet": {
                    "Name": record_name,
                    "Type": "A",
                    "TTL": 300,
                    "ResourceRecords": [
                        {
                            "Value": ipaddress
                        },
                    ],
                }
            },
        ]
                     }
                )
        print(response)