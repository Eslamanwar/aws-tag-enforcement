import json
import boto3
import botocore
import json
import urllib.request

client = boto3.client('ecr')
response_tag = client.list_tags_for_resource(
    resourceArn='arn:aws:ecr:us-east-1:616188222277:repository/amazonlinux'
    )

print(response_tag["tags"])



response_get_url = client.get_download_url_for_layer(
    registryId='616188222277',
    repositoryName='amazonlinux',
    layerDigest='sha256:fde8b9de1022b76e8b1be44fce7bf1b00df38983dc8f42b9e625cd4f2f595919'
)

with urllib.request.urlopen(response_get_url["downloadUrl"]) as response:
   html = response.read().decode('utf-8')
   html_json_obj = json.loads(html)

print(html_json_obj['config']['Labels'])
