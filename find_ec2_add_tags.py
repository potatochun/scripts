# Create tags based on selected AWS CLI profile
# This script assumes AWS profiles has been setup in your .aws directory
# Then proceed to create tags for all ec2 instances per region
# TODO: Provide input for tags 

from botocore import credentials
import botocore.session
import boto3
import os

class retrieveTags:
    def initiate_session(self, user_input, region):
        
        self.user_input = user_input
        self.region = region

        # Established botocore session with caching ability
        cli_cache = os.path.join(os.path.expanduser('~'),'.aws/cli/cache')

        self.session = botocore.session.Session(profile=self.user_input)
        self.session.get_component('credential_provider').get_provider('assume-role').cache = credentials.JSONFileCache(cli_cache)
        self.session_2 = boto3.Session(botocore_session=self.session, profile_name = self.user_input)

        self.get_all_ec2_id()
        self.create_tags()

    def get_all_ec2_id(self):   
        self.ec2_session = self.session_2.client('ec2')
        self.get_ec2 = self.session_2.resource('ec2', region_name=self.region)
        self.response = self.ec2_session.describe_instances()
   
        self.ec_list=[]

        total_instances = len(self.response['Reservations'])

        # Get a list of instance IDs
        for i in range(0, total_instances):
            ids = self.response['Reservations'][i]['Instances'][0]['InstanceId']
            self.ec_list.append(ids)

    def create_tags(self):
        self.ec2_client = self.session_2.resource('ec2', region_name=self.region)
    
        for z in self.ec_list:
            self.get_instance = self.ec2_client.Instance(z)

            self.get_instance.create_tags(
                Tags:[{'Key': 'Env', 'Value': 'Production'},
                       {'Key': 'Backup', 'Value': 'True'},
                       {'Key': 'RPO', 'Value': '30'}
                    ]
                )
   

if __name__ == "__main__":
    user_input = input('Enter the AWS profile: ')
    region = input('Enter AWS region: ')
    
    r = retrieveTags()
    r.initiate_session(user_input, region)

