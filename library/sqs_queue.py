import boto3


def create_sqs():
    # Get the service resource
    sqs = boto3.resource('sqs')

    # Create the queue. This returns an SQS.Queue instance
    queue = sqs.create_queue(QueueName='test', Attributes={'DelaySeconds': '5'})

    # You can now access identifiers and attributes
    print(queue.url)
    print(queue.attributes.get('DelaySeconds'))

def existing_sqs():
    # Get the service resource
    sqs = boto3.resource('sqs')

    # Get the queue. This returns an SQS.Queue instance
    queue = sqs.get_queue_by_name(QueueName='test')

    # You can now access identifiers and attributes
    print(queue.url)
    print(queue.attributes.get('DelaySeconds'))

def sending_message():
    # Get the service resource
    sqs = boto3.resource('sqs')

    # Get the queue
    queue = sqs.get_queue_by_name(QueueName='test')

    # Create a new message
    #response = queue.send_message(MessageBody='world')
    response = queue.send_message(MessageBody='boto3', MessageAttributes={
        'Author': {
            'StringValue': 'Daniel',
            'DataType': 'String'
        }
    })

    # The response is NOT a resource, but gives you a message ID and MD5
    print(response.get('MessageId'))
    print(response.get('MD5OfMessageBody'))



def getting_message():
    # Get the service resource
    sqs = boto3.resource('sqs')

    # Get the queue
    queue = sqs.get_queue_by_name(QueueName='test')

    # Process messages by printing out body and optional author name
    for message in queue.receive_messages(MessageAttributeNames=['Author']):
        # Get the custom author message attribute if it was set
        author_text = ''
        if message.message_attributes is not None:
            author_name = message.message_attributes.get('Author').get('StringValue')
            if author_name:
                author_text = ' ({0})'.format(author_name)

        # Print out the body and author (if set)
        print('Hello, {0}!{1}'.format(message.body, author_text))

        # Let the queue know that the message is processed
        message.delete()


sending_message()
existing_sqs()
getting_message()