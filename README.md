# aws-tag-enforcement

## Architecture design questions

- What AWS ECR service can we attach Tag?
    - we can attach tag to the ECR repository
    - we can NOT attach AWS tag to the image inside the repository


- Tagging solution for AWS ECR repositories   
Tags suggestions :   
    - static tagging , example   
```
{
  "Confidentiality" : ""
  "Compliance" : ""
  "AutoTag_ManagedBy": "Site Reliability Engineering"
}
```
    - Security Tags suggestions:
```
{
  "Confidentiality" : ""
  "Compliance" : ""
}
```

    - Dynamic Based tags , examples
```
{
  "AutoTag_UserIdentityType": "userIdentity.type",
  "AutoTag_UserName": "userName",
  "AutoTag_ClientInfo": "SourceIP: $event.sourceIPAddress, UserAgent: $event.userAgent",
}
```

- Where to store pre-defined static tagging or custom tagging?
    - Json file
        - pros:
            - easy to create with no cost
        - cons:
            - More difficult to implement Trigger based on changes on such file
    - DynamoDB 
        - pros:
            - easy to Migrate to already made solution as it will be part of it
            - you can make use of trigger lambda based on inserting newly-added tags to DynamoDB
        - cons:
            - consume cost



- Which service will trigger the Lambda tagging function?
    - As normally CI/CD pipeline not involved in creating the Repository itself so, NOT recommended to enforce Tag based on CI/CD
    - CloudWatch Events rule targets a Lambda function that auto tag the Repositories (must enable CloudTrail to trigger cloudwatch)


- Do we need to enforce tagging in multi Regions /Account?


- who will decide if this repo sensitivity is high or low as it will be automated? 
    - Is it will be static tagging on all repositories
    - or based upon CloudTrail event fields like user who created the repo ,we can use this feature to restrict policy like delete the repo that other user created



## How it works
1. Enable CloudTrail in the current Region ,as it will trigger the Cloudwatch
2. Cloudwatch will Trigger a Lambda function anytime a new ECR repository resource is created
3. Main CloudFormation Stack 
    - Lambda Function
    - IAM Role for the tag enforcement and sync Lambda functions.


## Prerequisites

- CloudTrail must be Enabled in the specific region

## Installation

## Resources 

- S3 bucket for lambda code
- S3 bucket to store Json file contains Tag information /Or Using DynamoDB
- Amazon CloudWatch
- Lambda Function
- IAM Role for the tag enforcement and sync Lambda functions.

## Diagram
### Aws Tag Enforcement
![alt text](https://github.com/Eslamanwar/aws-tag-enforcement/blob/master/images/Auto-Tag-Diagram.png?raw=true)
   


### Enforce Tagging accross multi Account
![alt text](https://github.com/Eslamanwar/aws-tag-enforcement/blob/master/images/Auto-Tag-Diagram-multi-Account.png?raw=true)

## Referances

- https://aws.amazon.com/ar/blogs/apn/enforce-centralized-tag-compliance-using-aws-service-catalog-amazon-dynamodb-aws-lambda-and-amazon-cloudwatch-events/
- https://aws.amazon.com/ar/blogs/mt/monitor-tag-changes-on-aws-resources-with-serverless-workflows-and-amazon-cloudwatch-events/
- https://aws.amazon.com/ar/blogs/security/how-to-automatically-tag-amazon-ec2-resources-in-response-to-api-events/
- https://github.com/aws-samples/aws-tag-enforcement-service-catalog























