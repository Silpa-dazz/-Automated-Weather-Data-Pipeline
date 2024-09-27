# Project overview:


This pipeline involves fetching weather data via an API, storing it in DynamoDB via a Lambda function, and processing the DynamoDB stream with a second Lambda to push data to S3.
Snowflake integrates with S3 through an external stage and Snowpipe, ingesting data into a Snowflake weather table.
