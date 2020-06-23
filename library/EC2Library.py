import time
import boto3
from botocore.exceptions import ClientError


class EC2Library:

    def __init__(self):
        ec2_resource = boto3.resource('ec2')
        ec2_client = boto3.client('ec2')
        self.ec2_resource = ec2_resource
        self.ec2_client = ec2_client

    # create a new EC2 instance
    def create_instance(self):
        instances = self.ec2_resource.create_instances(
            ImageId='ami-0e84e211558a022c0',
            KeyName='aws',
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro',
        )
        return instances[0].id

    def start_stop_instance(self, instance_id, action):

        if action == 'ON':
            # Do a dryrun first to verify permissions
            try:
                response = self.ec2_client.start_instances(InstanceIds=[instance_id], DryRun=True)
            except ClientError as e:
                if 'DryRunOperation' not in str(e):
                    raise
                print(response)
            # Dry run succeeded, run start_instances without dryrun
            try:
                response = self.ec2_client.start_instances(InstanceIds=[instance_id], DryRun=False)

            except ClientError as e:
                print(e)
        else:
            # Do a dryrun first to verify permissions
            try:
                self.ec2_client.stop_instances(InstanceIds=[instance_id], DryRun=True)
            except ClientError as e:
                if 'DryRunOperation' not in str(e):
                    raise

            # Dry run succeeded, call stop_instances without dryrun
            try:
                response = self.ec2_client.stop_instances(InstanceIds=[instance_id], DryRun=False)
                print(response)
            except ClientError as e:
                print(e)

    def find_instances(self):
        instance_list = []
        response = self.ec2_client.describe_instances()
        for region in response['Reservations']:
            for instance in region['Instances']:
                instance_list.append(instance['InstanceId'])
        return instance_list

    def terminate_all_instances(self):
        self.stop_running_instances()
        all_instances = self.find_instances()
        self.ec2_client.terminate_instances(InstanceIds=all_instances)

    def find_running_instances(self):
        running = []
        response = self.ec2_client.describe_instances()
        for region in response['Reservations']:
            for instance in region['Instances']:
                if instance['State']['Name'] == 'running':
                    running.append(instance['InstanceId'])
        return running

    def find_running_instance_public_ip(self, instance_id):
        response = self.ec2_client.describe_instances()
        for region in response['Reservations']:
            for instance in region['Instances']:
                if instance['InstanceId'] == instance_id:
                    if instance['State']['Name'] == 'running':
                        return instance['PublicDnsName']
        return None

    def stop_running_instances(self):
        running = self.find_running_instances()
        for key in running:
            self.start_stop_instance(key, "OFF")
            print("stopping ", key)

    def check_if_instance_is_running(self, instance_identifier):
        try:
            response = self.ec2_client.describe_instances()
            print(response)
        except Exception as error:
            print("Got exception: ", error)
            error
        for reservation in response["Reservations"]:
            for instance in reservation['Instances']:
                try:
                    if instance["InstanceId"] == instance_identifier and instance["State"]["Name"] == 'running':
                        return True
                except Exception as error:
                    print("Session has no: ", error)
                    pass
        return False

    def wait_for_instance_to_be_running(self, instance_identifier, tries=60):
        print("Starting at: ", time.localtime())

        while tries > 0:
            if self.check_if_instance_is_running(instance_identifier):
                print("Running at: ", time.localtime())
                return True
            time.sleep(10)
            tries -= 1
            print("Waiting for :", instance_identifier, "Tries :", tries)
        return False


def main():
    ec2 = EC2Library()
    ec2.terminate_all_instances()
    # print(ec2.find_running_instance_public_ip('i-0bd331f513d4b5261'))

    # instance_id = ec2.create_instance()
    # ec2.wait_for_instance_to_be_running(instance_id)

    # ec2.find_running_instances()
    # # ec2.start_stop_instance('i-0aec9a710c29605b9','ON')
    # print(ec2.find_running_instances_public_ip())

    # response1 = ec2_client.describe_key_pairs()
    # response2 = ec2_client.create_key_pair(KeyName='KEY_PAIR_NAME2')
    # print(response1)
    # stop_running_instances(ec2_client)


if __name__ == '__main__':
    main()
