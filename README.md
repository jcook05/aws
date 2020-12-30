# aws


AWS Python Classes for standard AWS services EC2, VPC, Route53 and Autoscaling Groups.  Provided as an example of utility libraries leveraging the 
AWS Python SDK.   Requires configuration of AWS with your Access ID and Secret Access Key.   https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html
Each function supports (and requires) a profile.   Using multiple profiles will allow you to manage assets in several AWS accounts.   See the AWS configuration
link above for proper AWS profile setup. 



<b>AwsEc2Util.py</b>   -   Contains several useful AWS EC2 and VPC utility functions.   Provided as an example of a reusable
utility library.   Obviously this can be much more robust, but these functions do provide a solid baseline.  


<b>AwsAsgUtil.py</b>   -   Contains several useful AWS Autoscaling Group utility functions.   


<b>AWSRoute53.py</b> -  Contains a couple of useful AWS Route53 utility functions.   Particularly useful during CICD of a Webserver mapped to Route53 A Record. 







       
