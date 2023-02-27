import json, boto3, sagemaker

model_deployment_account="xxx"
bucket="sbabs-sagemaker-models"

model_package_group_name = "xgboost-demo-package-group"
model_registry_account = "xxxx"

region= "us-east-1"

#apply this policy in training account
def apply_s3_policy():
  # Create a policy for accessing the S3 bucket
  bucket_policy = {
      'Version': '2012-10-17',
      'Statement': [{
          'Sid': 'AddPerm',
          'Effect': 'Allow',
          'Principal': {
              'AWS': 'arn:aws:iam::{}:root'.format(model_deployment_account)
          },
          'Action': 's3:*',
          'Resource': ['arn:aws:s3:::{}'.format(bucket), 'arn:aws:s3:::{}/*'.format(bucket)]
      }]
  }

  # Convert the policy from JSON dict to string
  bucket_policy = json.dumps(bucket_policy)

  # Set the new policy
  s3 = boto3.client('s3')
  response = s3.put_bucket_policy(
      Bucket = bucket,
      Policy = bucket_policy)


#apply this policy in registry account
def apply_model_package_policy():
  boto3.setup_default_session(profile_name='sbabs-test')
  sm_client = boto3.client('sagemaker', region_name=region)
  model_package_group_policy = {
      'Version': '2012-10-17',
      'Statement': [{
          'Sid': 'AddPermModelPackageGroup',
          'Effect': 'Allow',
          'Principal': {
              'AWS': 'arn:aws:iam::{}:root'.format(model_deployment_account)
          },
          'Action': ['sagemaker:DescribeModelPackageGroup'],
          'Resource': 'arn:aws:sagemaker:{}:{}:model-package-group/{}'.format(region, model_registry_account, model_package_group_name)
      },{
          'Sid': 'AddPermModelPackageVersion',
          'Effect': 'Allow',
          'Principal': {
              'AWS': 'arn:aws:iam::{}:root'.format(model_deployment_account)
          },
          'Action': ["sagemaker:DescribeModelPackage",
                     "sagemaker:ListModelPackages",
                     "sagemaker:UpdateModelPackage",
                     "sagemaker:CreateModel"],
          'Resource': 'arn:aws:sagemaker:{}:{}:model-package/{}/*'.format(region, model_registry_account, model_package_group_name)
      }]
  }

  # Convert the policy from JSON dict to string
  model_package_group_policy = json.dumps(model_package_group_policy)

  # Set the policy to the model package group
  response = sm_client.put_model_package_group_policy(
      ModelPackageGroupName = model_package_group_name,
      ResourcePolicy = model_package_group_policy)

  print('ModelPackageGroupArn : {}'.format(response['ModelPackageGroupArn']))

  print("Success! You are all set to proceed for cross-account deployment.")


# apply_s3_policy();
apply_model_package_policy();