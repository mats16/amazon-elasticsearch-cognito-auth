from __future__ import print_function
from crhelper import CfnResource
import logging
import json
import boto3

logger = logging.getLogger(__name__)
helper = CfnResource(json_logging=False, log_level='DEBUG', boto_level='CRITICAL')

try:
    client = boto3.client('cognito-idp')
    pass
except Exception as e:
    helper.init_failure(e)

def lambda_handler(event, context):
    print(json.dumps(event))
    helper(event, context)

@helper.create
@helper.update
def enable_provider_token(event, context):
    user_pool_id = event['ResourceProperties']['UserPoolId']
    client_name_prefix = event['ResourceProperties']['ClientNamePrefix']
    user_pool_clients = client.list_user_pool_clients(UserPoolId=user_pool_id)['UserPoolClients']
    for user_pool_client in user_pool_clients:
        client_id = user_pool_client['ClientId']
        client_name = user_pool_client['ClientName']
        if client_name.startswith(client_name_prefix):
            physical_resource_id = client_id
    return physical_resource_id

@helper.delete
def disable_provider_token(event, context):
    return
