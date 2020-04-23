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
def create(event, context):
    user_pool_id = event['ResourceProperties']['UserPoolId']
    domain = event['ResourceProperties'].get('Domain', user_pool_id.split('_')[1].lower())
    client.create_user_pool_domain(
        UserPoolId=user_pool_id,
        Domain=domain,
    )
    region = user_pool_id.split('_')[0]
    physical_resource_id = f'{domain}.auth.{region}.amazoncognito.com'
    return physical_resource_id

@helper.update
def update(event, context):
    user_pool_id = event['ResourceProperties']['UserPoolId']
    domain = event['ResourceProperties'].get('Domain', user_pool_id.split('_')[1].lower())
    old_user_pool_id = event['OldResourceProperties']['UserPoolId']
    old_domain = event['OldResourceProperties']['Domain']
    client.delete_user_pool_domain(
        UserPoolId=old_user_pool_id,
        Domain=old_domain,
    )
    client.create_user_pool_domain(
        UserPoolId=user_pool_id,
        Domain=domain,
    )
    region = user_pool_id.split('_')[0]
    physical_resource_id = f'{domain}.auth.{region}.amazoncognito.com'
    return physical_resource_id

@helper.delete
def delete(event, context):
    user_pool_id = event['ResourceProperties']['UserPoolId']
    domain = event['ResourceProperties'].get('Domain', user_pool_id.split('_')[-1].lower())
    try:
        res = client.delete_user_pool_domain(
            UserPoolId=user_pool_id,
            Domain=domain,
        )
        logger.info(res)
    except InvalidParameterException as e:
        logger.info(e)
    except Exception as e:
        logger.error(e)