# Amazon Elasticsearch Service with Amazon Cognito Auth

## How to Buid & Deploy

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
        SemanticVersion: 0.2.2
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