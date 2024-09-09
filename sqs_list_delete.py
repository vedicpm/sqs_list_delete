import boto3

def list_queues(sqs_client, prefix=''):
    response = sqs_client.list_queues(QueueNamePrefix=prefix)
    return response['QueueUrls'] if 'QueueUrls' in response else []

def delete_queue(sqs_client, queue_url):
    try:
        sqs_client.delete_queue(QueueUrl=queue_url)
        print(f"Deleted queue: {queue_url}")
    except Exception as e:
        print(f"Error deleting queue {queue_url}: {str(e)}")

def main():
    session = boto3.Session()
    sqs_client = session.client('sqs')

    while True:
        prefix = input("Enter SQS queue prefix (or 'exit' to quit): ").strip()
        
        if prefix.lower() == 'exit':
            break

        queues = list_queues(sqs_client, prefix)
        
        if not queues:
            print(f"No queues found with the prefix '{prefix}'")
            continue

        print(f"Found {len(queues)} queues with the prefix '{prefix}':")
        for i, queue in enumerate(queues, 1):
            print(f"{i}. {queue}")

        while True:
            action = input("Do you want to delete these queues? (yes/no/select): ").strip().lower()
            if action in ['yes', 'no', 'select']:
                break
            print("Invalid input. Please enter 'yes', 'no', or 'select'.")

        if action == 'no':
            print("Operation cancelled.")
            continue
        elif action == 'yes':
            for queue in queues:
                delete_queue(sqs_client, queue)
        elif action == 'select':
            while True:
                selection = input("Enter the numbers of the queues to delete (comma-separated) or 'all': ").strip().lower()
                if selection == 'all':
                    for queue in queues:
                        delete_queue(sqs_client, queue)
                    break
                else:
                    try:
                        indices = [int(i.strip()) for i in selection.split(',') if i.strip()]
                        if all(1 <= i <= len(queues) for i in indices):
                            for i in indices:
                                delete_queue(sqs_client, queues[i-1])
                            break
                        else:
                            print("Invalid selection. Please enter valid queue numbers.")
                    except ValueError:
                        print("Invalid input. Please enter numbers separated by commas or 'all'.")

        print("Operation completed.")

if __name__ == "__main__":
    main()
