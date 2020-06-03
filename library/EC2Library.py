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

    def start_stop_instance(self,instance_id,action):

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

    def find_running_instance_public_ip(self,instance_id):
        public_ips = []
        response = self.ec2_client.describe_instances()
        for region in response['Reservations']:
            for instance in region['Instances']:
                if instance['InstanceId'] == instance_id:
                    if instance['State']['Name'] == 'running':
                        return instance['PublicDnsName']
        else:
            return None

    def stop_running_instances(self):
        running = self.find_running_instances()
        for key in running:
            self.start_stop_instance(key, "OFF")
            print("stopping ",key)

    def check_if_instance_is_running(self,instance_identifier):
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

    def wait_for_instance_to_be_running(self,instance_identifier,tries=60):
        print("Starting at: ", time.localtime())

        while tries > 0:
            if self.check_if_instance_is_running(instance_identifier):
                print("Running at: ",time.localtime())
                return True
            time.sleep(10)
            tries -= 1
            print("Waiting for :", instance_identifier,"Tries :",tries)
        return False
# create_instance(ec2)

# ec2 = EC2Library()
# ec2.terminate_all_instances()
# print(ec2.find_running_instance_public_ip('i-0bd331f513d4b5261'))

# instance_id = ec2.create_instance()
# ec2.wait_for_instance_to_be_running(instance_id)

#ec2.find_running_instances()
# # ec2.start_stop_instance('i-0aec9a710c29605b9','ON')
# print(ec2.find_running_instances_public_ip())

# response1 = ec2_client.describe_key_pairs()
# response2 = ec2_client.create_key_pair(KeyName='KEY_PAIR_NAME2')
# print(response1)
# stop_running_instances(ec2_client)

# start_stop_instance(ec2_client,'i-0aec9a710c29605b9','ON')
#
# {'Reservations': [{'Groups': [], 'Instances': [{'AmiLaunchIndex': 1, 'ImageId': 'ami-0e84e211558a022c0', 'InstanceId': 'i-01a7a6bfe9341d746', 'InstanceType': 't2.micro', 'LaunchTime': datetime.datetime(2020, 5, 24, 23, 6, 24, tzinfo=tzutc()), 'Monitoring': {'State': 'disabled'}, 'Placement': {'AvailabilityZone': 'us-east-2c', 'GroupName': '', 'Tenancy': 'default'}, 'PrivateDnsName': 'ip-172-31-33-157.us-east-2.compute.internal', 'PrivateIpAddress': '172.31.33.157', 'ProductCodes': [], 'PublicDnsName': 'ec2-52-15-171-9.us-east-2.compute.amazonaws.com', 'PublicIpAddress': '52.15.171.9', 'State': {'Code': 16, 'Name': 'running'}, 'StateTransitionReason': '', 'SubnetId': 'subnet-b5385cf9', 'VpcId': 'vpc-38fc2353', 'Architecture': 'x86_64', 'BlockDeviceMappings': [{'DeviceName': '/dev/sda1', 'Ebs': {'AttachTime': datetime.datetime(2020, 5, 24, 23, 6, 24, tzinfo=tzutc()), 'DeleteOnTermination': True, 'Status': 'attached', 'VolumeId': 'vol-0b78c6fbb1d7c93b0'}}], 'ClientToken': '2c5c91a4-ddde-48da-a311-812b41a99d8e', 'EbsOptimized': False, 'EnaSupport': True, 'Hypervisor': 'xen', 'NetworkInterfaces': [{'Association': {'IpOwnerId': 'amazon', 'PublicDnsName': 'ec2-52-15-171-9.us-east-2.compute.amazonaws.com', 'PublicIp': '52.15.171.9'}, 'Attachment': {'AttachTime': datetime.datetime(2020, 5, 24, 23, 6, 24, tzinfo=tzutc()), 'AttachmentId': 'eni-attach-0296c73ca222cbe8e', 'DeleteOnTermination': True, 'DeviceIndex': 0, 'Status': 'attached'}, 'Description': '', 'Groups': [{'GroupName': 'default', 'GroupId': 'sg-70bb590b'}], 'Ipv6Addresses': [], 'MacAddress': '0a:c9:0f:1c:f4:84', 'NetworkInterfaceId': 'eni-091f8d4307659ff2f', 'OwnerId': '725116012558', 'PrivateDnsName': 'ip-172-31-33-157.us-east-2.compute.internal', 'PrivateIpAddress': '172.31.33.157', 'PrivateIpAddresses': [{'Association': {'IpOwnerId': 'amazon', 'PublicDnsName': 'ec2-52-15-171-9.us-east-2.compute.amazonaws.com', 'PublicIp': '52.15.171.9'}, 'Primary': True, 'PrivateDnsName': 'ip-172-31-33-157.us-east-2.compute.internal', 'PrivateIpAddress': '172.31.33.157'}], 'SourceDestCheck': True, 'Status': 'in-use', 'SubnetId': 'subnet-b5385cf9', 'VpcId': 'vpc-38fc2353', 'InterfaceType': 'interface'}], 'RootDeviceName': '/dev/sda1', 'RootDeviceType': 'ebs', 'SecurityGroups': [{'GroupName': 'default', 'GroupId': 'sg-70bb590b'}], 'SourceDestCheck': True, 'VirtualizationType': 'hvm', 'CpuOptions': {'CoreCount': 1, 'ThreadsPerCore': 1}, 'CapacityReservationSpecification': {'CapacityReservationPreference': 'open'}, 'HibernationOptions': {'Configured': False}, 'MetadataOptions': {'State': 'applied', 'HttpTokens': 'optional', 'HttpPutResponseHopLimit': 1, 'HttpEndpoint': 'enabled'}}, {'AmiLaunchIndex': 0, 'ImageId': 'ami-0e84e211558a022c0', 'InstanceId': 'i-071004a8acd712307', 'InstanceType': 't2.micro', 'LaunchTime': datetime.datetime(2020, 5, 24, 23, 6, 24, tzinfo=tzutc()), 'Monitoring': {'State': 'disabled'}, 'Placement': {'AvailabilityZone': 'us-east-2c', 'GroupName': '', 'Tenancy': 'default'}, 'PrivateDnsName': 'ip-172-31-40-50.us-east-2.compute.internal', 'PrivateIpAddress': '172.31.40.50', 'ProductCodes': [], 'PublicDnsName': '', 'State': {'Code': 80, 'Name': 'stopped'}, 'StateTransitionReason': 'User initiated (2020-05-24 23:07:11 GMT)', 'SubnetId': 'subnet-b5385cf9', 'VpcId': 'vpc-38fc2353', 'Architecture': 'x86_64', 'BlockDeviceMappings': [{'DeviceName': '/dev/sda1', 'Ebs': {'AttachTime': datetime.datetime(2020, 5, 24, 23, 6, 24, tzinfo=tzutc()), 'DeleteOnTermination': True, 'Status': 'attached', 'VolumeId': 'vol-084b779a73975bc1b'}}], 'ClientToken': '2c5c91a4-ddde-48da-a311-812b41a99d8e', 'EbsOptimized': False, 'EnaSupport': True, 'Hypervisor': 'xen', 'NetworkInterfaces': [{'Attachment': {'AttachTime': datetime.datetime(2020, 5, 24, 23, 6, 24, tzinfo=tzutc()), 'AttachmentId': 'eni-attach-0201d4b00f52542cf', 'DeleteOnTermination': True, 'DeviceIndex': 0, 'Status': 'attached'}, 'Description': '', 'Groups': [{'GroupName': 'default', 'GroupId': 'sg-70bb590b'}], 'Ipv6Addresses': [], 'MacAddress': '0a:30:36:16:a0:94', 'NetworkInterfaceId': 'eni-0bdc46d44e87c4184', 'OwnerId': '725116012558', 'PrivateDnsName': 'ip-172-31-40-50.us-east-2.compute.internal', 'PrivateIpAddress': '172.31.40.50', 'PrivateIpAddresses': [{'Primary': True, 'PrivateDnsName': 'ip-172-31-40-50.us-east-2.compute.internal', 'PrivateIpAddress': '172.31.40.50'}], 'SourceDestCheck': True, 'Status': 'in-use', 'SubnetId': 'subnet-b5385cf9', 'VpcId': 'vpc-38fc2353', 'InterfaceType': 'interface'}], 'RootDeviceName': '/dev/sda1', 'RootDeviceType': 'ebs', 'SecurityGroups': [{'GroupName': 'default', 'GroupId': 'sg-70bb590b'}], 'SourceDestCheck': True, 'StateReason': {'Code': 'Client.UserInitiatedShutdown', 'Message': 'Client.UserInitiatedShutdown: User initiated shutdown'}, 'VirtualizationType': 'hvm', 'CpuOptions': {'CoreCount': 1, 'ThreadsPerCore': 1}, 'CapacityReservationSpecification': {'CapacityReservationPreference': 'open'}, 'HibernationOptions': {'Configured': False}, 'MetadataOptions': {'State': 'applied', 'HttpTokens': 'optional', 'HttpPutResponseHopLimit': 1, 'HttpEndpoint': 'enabled'}}], 'OwnerId': '725116012558', 'ReservationId': 'r-0c94f569f58210f57'}], 'ResponseMetadata': {'RequestId': '2caa871e-916e-42f3-af4a-8f3eb01ee636', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '2caa871e-916e-42f3-af4a-8f3eb01ee636', 'content-type': 'text/xml;charset=UTF-8', 'transfer-encoding': 'chunked', 'vary': 'accept-encoding', 'date': 'Sun, 24 May 2020 23:30:12 GMT', 'server': 'AmazonEC2'}, 'RetryAttempts': 0}}


