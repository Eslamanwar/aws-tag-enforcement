# aws-tag-enforcement

## How it works
1. Enable CloudTrail in the current Region or all Regions you work with ,as it will trigger the Cloudwatch
2. Case (1) --> If you insert new Tag Json file in the specific S3 Bucket , it will trigger the Cloudwatch Event that Run the Lambda function which Auto tag all ECR repos that exist in all Regions
3. case (2) --> if you Create new ECR repo , it will trigger the Cloudwatch Event that run the Lambda that will force apply tags to this new ECR Repo
4. case (3) --> if an image is pushed to any repo , it will trigger the Cloudwatch Event that run the Lambda that will query the docker image labels and verify if they match the expected AWS tags
5. Main CloudFormation Stack 
    - Lambda Function 1 --> for new created ECR repo 
    - Lambda Function 2 --> when put new Tag Json file , to apply to already existing ECR repos
    - Lambda Function 3 --> when docker image pushed , compare the image labels with the repo AWS tag
    - IAM Role to give Lambda access permissions on other resources like 'ECR'

## Diagram
### Aws Tag Enforcement
![alt text](https://github.com/Eslamanwar/aws-tag-enforcement/blob/master/images/Auto-Tag-Diagram.png?raw=true)




# case 3 lambda
- This function will get the Docker image Labels and AWS repo tags
- it must have Role permission on ECR to read AWS Repositories tags
![alt text](https://github.com/Eslamanwar/aws-tag-enforcement/blob/master/images/tag.png?raw=true)
![alt text](https://github.com/Eslamanwar/aws-tag-enforcement/blob/master/images/screenshot.png?raw=true)


## Prerequisites

- CloudTrail must be Enabled in the specific region





## How to put/get image labels

### Dockerfile:

```
FROM amazonlinux:latest
LABEL version="1.0" maintainer="Eslam Mohammed <eslam.anwar96@gmail.com>"


url=$(aws ecr get-download-url-for-layer --registry-id 011974135172 --repository-name amazonlinux --layer-digest sha256:95481a8e9b7fcae0f5bea89d5b35ec1029303910033fa1a20f083970ec97ee28 | jq -r .downloadUrl)

curl -s --connect-timeout 5 $url | jq .config.Labels
```




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








### Enforce Tagging accross multi Account
![alt text](https://github.com/Eslamanwar/aws-tag-enforcement/blob/master/images/Auto-Tag-Diagram-multi-Account.png?raw=true)

## Referances

- https://aws.amazon.com/ar/blogs/apn/enforce-centralized-tag-compliance-using-aws-service-catalog-amazon-dynamodb-aws-lambda-and-amazon-cloudwatch-events/
- https://aws.amazon.com/ar/blogs/mt/monitor-tag-changes-on-aws-resources-with-serverless-workflows-and-amazon-cloudwatch-events/
- https://aws.amazon.com/ar/blogs/security/how-to-automatically-tag-amazon-ec2-resources-in-response-to-api-events/
- https://github.com/aws-samples/aws-tag-enforcement-service-catalog























