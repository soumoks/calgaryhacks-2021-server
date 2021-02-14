import boto3
import json
import logging
import os
from decimal import Decimal
from utils.response import Response

# logger config
logger = logging.getLogger()
logger.setLevel(logging.INFO)



# Global resources for container re-use
runtime = boto3.client('runtime.sagemaker')
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1',
                          endpoint_url="https://dynamodb.us-east-1.amazonaws.com")



class DecimalEncoder(json.JSONEncoder):
    """
    Helper class to convert a DynamoDB item to JSON
    """

    def default(self, obj):
        if isinstance(obj, Decimal):
            if obj % 1 > 0:
                return float(obj)
            else:
                return int(obj)
        return super(DecimalEncoder, self).default(obj)


def lambda_handler(event, context):
    candidate_user_id = str(event['userid'])
    logger.info(f'Received user_id: {candidate_user_id}')
    return get_items()
    """
    response = [
            {
                "id": 1,
                "title": "COVID-19 Equity, Diversity and Inclusion Survey",
                "summary": "COVID-19 has impacted members of our campus community differently. As part of the Office of Equity, Diversity, and Inclusion’s mandate to strengthen the University of Calgary’s efforts to advance equity, diversity, and inclusion, we are conducting a survey to better understand how the COVID-19 pandemic has impacted diverse members of our community"
            },
            {
                "id": 2,
                "title": "New Course Reading List Tool",
                "summary" : "The library has a new tool for easier creation and copyright approval of course reading lists, available under Tools on the top menu within each D2L course. This tool lets instructors create lists that can be reused the next time you teach the course, sends listed items for copyright clearance and tracks student engagement with readings."
            },
            {
                "id": 3,
                "title": "Teaching Continuity Resources",
                "summary" : "As on-campus classes are disrupted, there are a few essential factors to consider: communicating with students, putting lectures online, communication among students and assessing student learning"
            }
        ]

    return response
    """



def get_items():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1',
                              endpoint_url="https://dynamodb.us-east-1.amazonaws.com")
    table_name = 'announcements'
    table = dynamodb.Table(table_name)
    logger.info("Connected to DynamoDB.")
    # return all announcements
    response = table.scan()["Items"]
    return json.loads(json.dumps(response, cls=DecimalEncoder))


def get_user_data(user_id: str, dynamodb=None, table_name='User_Profile_Full'):
    """
    @param: user_id - Accepts a user id
    @param: dynamodb - DynamoDb resource
    @table_name - DynamoDb table name
    @return: Returns user information in the following format

    """
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1',
                                  endpoint_url="https://dynamodb.us-east-1.amazonaws.com")
    if user_id is None:
        logger.info('User ID not passed')
        raise Exception("User ID not passed")

    table = dynamodb.Table(table_name)
    try:
        response = table.get_item(Key={'key_name': user_id})['Item']
    except:
        logger.info(f"User ID {user_id} doesn't exist in db")
        raise Exception(f"User ID {user_id} doesn't exist in db")

    return json.loads(json.dumps(response, cls=DecimalEncoder))