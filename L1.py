import json 
import urllib.request 
from urllib.error import HTTPError 
import boto3 
from botocore.exceptions import ClientError 
from datetime import datetime 
import os 
from decimal import Decimal 
import uuid  # Import the uuid module 
 
# Get API key from environment variable 
API_KEY = os.environ.get("OPENWEATHERMAP_API_KEY", "022febae84cab5e86145bc72b9c7dc9a")  # Change to environment variable 
# Get location from environment variable or use a default 
LOCATION = os.environ.get('WEATHER_LOCATION', 'London')  # Default location if not specified 
# Replace with your DynamoDB table name 
DYNAMODB_TABLE_NAME = os.environ.get('DYNAMODB_TABLE_NAME', 'second-lambda')  # Change to environment variable 
 
# Initialize a DynamoDB resource 
dynamodb = boto3.resource('dynamodb') 
table = dynamodb.Table(DYNAMODB_TABLE_NAME)  # Get the DynamoDB table resource 
 
def lambda_handler(event, context): 
    try: 
        # API endpoint for OpenWeatherMap 
        url = f"http://api.openweathermap.org/data/2.5/weather?q={LOCATION}&appid={API_KEY}&units=metric" 
        
        # Make a GET request to the API 
        with urllib.request.urlopen(url) as response: 
            if response.status == 200: 
                # Read and decode the response 
                weather_data = json.loads(response.read().decode()) 
                
                # Store data in DynamoDB 
                store_data_in_dynamodb(weather_data) 
                
                return { 
                    'statusCode': 200, 
                    'body': json.dumps("Weather data successfully fetched and stored in DynamoDB") 
                } 
            else: 
                return { 
                    'statusCode': response.status, 
                    'body': json.dumps(f"Failed to get data: {response.status}") 
                } 
    except HTTPError as e: 
        return { 
            'statusCode': e.code, 
            'body': json.dumps(f"HTTP Error: {e.code}") 
        } 
    except Exception as e: 
        return { 
            'statusCode': 500, 
            'body': json.dumps(f"Error: {str(e)}") 
        } 
def store_data_in_dynamodb(data): 
    try: 
        # Generate a unique ID for the item 
        item_id = str(uuid.uuid4()) 
        
        # Prepare the data for DynamoDB 
        item = { 
            'id': item_id,  # Add the UUID field 
            'city': data['name'],  # Assuming 'city' is your primary key 
            'location': data['name'], 
            'weather': data['weather'][0]['description'], 
            'temperature': Decimal(str(data['main']['temp'])),  # Convert to Decimal for DynamoDB 
            'humidity': Decimal(str(data['main']['humidity'])),  # Convert to Decimal for DynamoDB 
            'timestamp': datetime.utcnow().isoformat(),  # Store the current timestamp 
            'time': datetime.utcnow().isoformat()  # Include the 'time' attribute 
        } 
        
        # Log the item to check its structure before putting it into DynamoDB 
        print(f"Attempting to insert the following item into DynamoDB: {item}") 
        
        # Put the item in DynamoDB 
        table.put_item(Item=item)  # Use the DynamoDB table object 
    except ClientError as e: 
        print(f"Failed to insert data into DynamoDB: {e.response['Error']['Message']}") 
        raise 
    except KeyError as e: 
        print(f"Missing expected key in weather data: {str(e)}") 
        raise 
    except Exception as e: 
        print(f"Error storing data in DynamoDB: {str(e)}") 
        raise
