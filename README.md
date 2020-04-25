# Amazon Elasticsearch Service with Amazon Cognito Auth

## Get Started

Deploy the sample template from the AWS Serverless Application Repository:

[![cloudformation-launch-button](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://serverlessrepo.aws.amazon.com/applications/arn:aws:serverlessrepo:us-east-1:345513370492:applications~amazon-elasticsearch-cognito-auth)

## How to Buid & Deploy with AWS SAM

```bash
sam build --use-container --skip-pull-image
sam deploy --guided
```

## How to modify mapping templates

This template has the custome resource to modify  mapping templates.
`ModifyTemplateArn` in the Outputs is Lambda Function for custome resource.

```yaml
Resources:
  Elasticsearch:
    Type: AWS::Serverless::Application
    Properties:
      Location:
        ApplicationId: arn:aws:serverlessrepo:us-east-1:345513370492:applications/amazon-elasticsearch-cognito-auth
        SemanticVersion: 0.3.0
      Parameters:
        ElasticsearchVersion: 7.4
        CognitoAllowedEmailDomains: '*'

  TweetsTemplate:
    Type: Custom::ElasticsearchTemplate
    Version: 1.0
    Properties:
      ServiceToken: !GetAtt Elasticsearch.Outputs.ModifyTemplateArn
      Host: !GetAtt Elasticsearch.Outputs.Endpoint
      Body: '
        {
          "index_patterns": ["index-*"],
          "settings": {
            "number_of_shards": 4,
            "number_of_replicas": 1
          },
          "mappings": {
            "_source": {
              "enabled": true
            },
            "properties": {
              "text": {
                "type": "text"
              }
            }
          }
        }'
```