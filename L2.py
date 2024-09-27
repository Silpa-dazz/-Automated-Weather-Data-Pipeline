import json 
import boto3 
from datetime import datetime 
 
s3 = boto3.client('s3') 
 
def lambda_handler(event, context): 
    bucket_name = 'demo-mybuckets'  # Replace with your S3 bucket name 
    timestamp = datetime.utcnow().isoformat() 
 
    try: 
        # Log the entire event for debugging 
        print(f"Received event: {json.dumps(event, indent=2)}") 
        
        # Check if 'Records' key exists in the event 
        if 'Records' in event: 
            for record in event['Records']: 
                if record['eventName'] in ['INSERT', 'MODIFY']: 
                    new_image = record['dynamodb']['NewImage'] 
                    # Convert DynamoDB item to JSON 
                    new_image_json = {k: list(v.values())[0] for k, v in new_image.items()} 
                    
                    # Create a unique file key using timestamp 
                    key = f'dynamodb_record_{timestamp}.json' 
                    
                    # Upload to S3 
                    s3.put_object( 
                        Bucket=bucket_name, 
                        Key=key, 
                        Body=json.dumps(new_image_json, indent=2), 
                        ContentType='application/json' 
                    ) 
                    
                    print(f'Successfully uploaded record: {key} to S3') 
        else: 
            print(f"No 'Records' found in the event: {event}") 
    except Exception as e: 
        print(f'Error uploading data to S3: {e}') 
        raise
