from __future__ import print_function
from crhelper import CfnResource
import logging
import json
import boto3

logger = logging.getLogger(__name__)
helper = CfnResource(json_logging=False, log_level='DEBUG', boto_level='CRITICAL')

try:
    client = boto3.client('cognito-identity')
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
    identity_pool_id = event['ResourceProperties']['IdentityPoolId']

    identity_pool = client.describe_identity_pool(IdentityPoolId=identity_pool_id)
    identity_pool_roles = client.get_identity_pool_roles(IdentityPoolId=identity_pool_id)
    roles = identity_pool_roles.get('Roles', {})
    role_mappings = identity_pool_roles.get('RoleMappings', {})

    for i in identity_pool.get('CognitoIdentityProviders', []):
        if i['ProviderName'].split('/')[1] == user_pool_id:
            identity_provider = f"{i['ProviderName']}:{i['ClientId']}"
            role_mappings[identity_provider] = {
                'Type': 'Token',
                'AmbiguousRoleResolution': 'AuthenticatedRole'
            }
    if len(role_mappings) > 0:
        res = client.set_identity_pool_roles(
            IdentityPoolId=identity_pool_id,
            Roles=roles,
            RoleMappings=role_mappings
        )
        logger.info(res)
    physical_resource_id = f'{identity_pool_id}/{user_pool_id}'
    return physical_resource_id

@helper.delete
def disable_provider_token(event, context):
    user_pool_id = event['ResourceProperties']['UserPoolId']
    identity_pool_id = event['ResourceProperties']['IdentityPoolId']

    #identity_pool = client.describe_identity_pool(IdentityPoolId=identity_pool_id)
    identity_pool_roles = client.get_identity_pool_roles(IdentityPoolId=identity_pool_id)
    roles = identity_pool_roles.get('Roles', {})
    role_mappings = identity_pool_roles.get('RoleMappings', {})
    new_role_mappings = {}
    for identity_provider in role_mappings:
        if identity_provider.split('/')[-1].split(':')[0] == user_pool_id:
            pass
        else:
            new_role_mappings[identity_provider] = role_mappings[identity_provider]
    try:
        res = client.set_identity_pool_roles(
            IdentityPoolId=identity_pool_id,
            Roles=roles,
            RoleMappings=new_role_mappings
        )
        logger.info(res)
    except Exception as e:
        logger.error(e)
    return
