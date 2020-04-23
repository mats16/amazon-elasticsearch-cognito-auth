from __future__ import print_function
from crhelper import CfnResource
import logging
import json
import boto3
import os
from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch.client import IndicesClient
from elasticsearch.exceptions import NotFoundError
from requests_aws4auth import AWS4Auth

logger = logging.getLogger(__name__)
helper = CfnResource(json_logging=False, log_level='DEBUG', boto_level='CRITICAL')

try:
    region = os.environ['AWS_REGION']
    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
except Exception as e:
    helper.init_failure(e)

def lambda_handler(event, context):
    print(json.dumps(event))
    helper(event, context)

@helper.create
@helper.update
def create(event, context):
    template_name = event['LogicalResourceId'].lower()
    host = event['ResourceProperties']['Host']
    port = int(event['ResourceProperties'].get('Port', 443))
    body = json.loads(event['ResourceProperties']['Body'])
    es = Elasticsearch(
        hosts = [{'host': host, 'port': port}],
        http_auth = awsauth,
        use_ssl = True,
        verify_certs = True,
        connection_class = RequestsHttpConnection
    )
    res = IndicesClient(es).put_template(
        name=template_name,
        body=body,
    )
    logger.info(res)
    physical_resource_id = f'{host}/_template/{template_name}'
    return physical_resource_id

@helper.delete
def delete(event, context):
    template_name = event['LogicalResourceId'].lower()
    host = event['ResourceProperties']['Host']
    port = int(event['ResourceProperties'].get('Port', 443))
    es = Elasticsearch(
        hosts = [{'host': host, 'port': port}],
        http_auth = awsauth,
        use_ssl = True,
        verify_certs = True,
        connection_class = RequestsHttpConnection
    )
    try:
        res = IndicesClient(es).delete_template(
            name=template_name,
        )
        logger.info(res)
    except NotFoundError as e:
        logger.info(e)
    except Exception as e:
        logger.error(e)
