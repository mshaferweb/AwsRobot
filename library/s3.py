import boto3
import uuid

def create_bucket_name(bucket_prefix):
    # The generated bucket name must be between 3 and 63 chars long
    return ''.join([bucket_prefix, str(uuid.uuid4())])

def create_bucket(bucket_prefix, s3_connection):
    session = boto3.session.Session()
    current_region = session.region_name
    bucket_name = create_bucket_name(bucket_prefix)
    bucket_response = s3_connection.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
        'LocationConstraint': current_region})
    print(bucket_name, current_region)
    return bucket_name, bucket_response

def create_temp_file(size, file_name, file_content):
    random_file_name = ''.join([str(uuid.uuid4().hex[:6]), file_name])
    with open(random_file_name, 'w') as f:
        f.write(str(file_content) * size)
    return random_file_name


def copy_to_bucket(bucket_from_name, bucket_to_name, file_name):
    copy_source = {
        'Bucket': bucket_from_name,
        'Key': file_name
    }
    s3_resource.Object(bucket_to_name, file_name).copy(copy_source)

s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')


# first_bucket_name, first_response = create_bucket(bucket_prefix='firstpythonbucket', s3_connection=s3_resource.meta.client)
# print(first_bucket_name, first_response)
# firstpythonbucket9830ffa4-c186-4a50-b7d9-1f94374571e0 us-east-2
# firstpythonbucket9830ffa4-c186-4a50-b7d9-1f94374571e0 {'ResponseMetadata': {'RequestId': 'B4C26AE3DA9DCFB1', 'HostId': 'wyWQQCDG/AErRpnrFsWix6682ytvvtnXnckWaWDolM8QCGJHNbVYfhvkgHOmrlhUwgXCIYaRyi4=', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amz-id-2': 'wyWQQCDG/AErRpnrFsWix6682ytvvtnXnckWaWDolM8QCGJHNbVYfhvkgHOmrlhUwgXCIYaRyi4=', 'x-amz-request-id': 'B4C26AE3DA9DCFB1', 'date': 'Sun, 24 May 2020 22:08:25 GMT', 'location': 'http://firstpythonbucket9830ffa4-c186-4a50-b7d9-1f94374571e0.s3.amazonaws.com/', 'content-length': '0', 'server': 'AmazonS3'}, 'RetryAttempts': 0}, 'Location': 'http://firstpythonbucket9830ffa4-c186-4a50-b7d9-1f94374571e0.s3.amazonaws.com/'}



# second_bucket_name, second_response = create_bucket(bucket_prefix='secondpythonbucket', s3_connection=s3_resource)
# print(second_bucket_name, second_response)

# secondpythonbucket30ba76f8-7fb9-4eb2-8cdf-7989493a5597 us-east-2
# secondpythonbucket30ba76f8-7fb9-4eb2-8cdf-7989493a5597 s3.Bucket(name='secondpythonbucket30ba76f8-7fb9-4eb2-8cdf-7989493a5597')

first_file_name = create_temp_file(300, 'firstfile.txt', 'f')

first_bucket_name = "firstpythonbucket9830ffa4-c186-4a50-b7d9-1f94374571e0"
second_bucket_name = "secondpythonbucket30ba76f8-7fb9-4eb2-8cdf-7989493a5597"

first_bucket = s3_resource.Bucket(name=first_bucket_name)
first_object = s3_resource.Object(
    bucket_name=first_bucket_name, key=first_file_name)

# UPLOAD FILES (All these do the same thing)
s3_resource.Object(first_bucket_name, first_file_name).upload_file(
    Filename=first_file_name)
first_object.upload_file(first_file_name)
s3_resource.Bucket(first_bucket_name).upload_file(
    Filename=first_file_name, Key=first_file_name)
s3_resource.meta.client.upload_file(
    Filename=first_file_name, Bucket=first_bucket_name,
    Key=first_file_name)

#DOWNLOAD
s3_resource.Object(first_bucket_name, first_file_name).download_file(f'/tmp/{first_file_name}')

# Copy between buckets
copy_to_bucket(first_bucket_name, second_bucket_name, first_file_name)

# Delete
s3_resource.Object(second_bucket_name, first_file_name).delete()

