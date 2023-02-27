import json, boto3

# point the session to training acct
boto3.setup_default_session(profile_name='sbabs-test')

# The model registry account id of the model package group
model_registry_account = "xxxx"

model_training_account = "xxxx"
model_package_group_name = "xgboost-demo-package-group"

region= "us-east-1"
sm_client = boto3.client('sagemaker', region_name=region)

# 1. Create policy to allow the model training account to access the ModelPackageGroup
model_package_group_policy = {
  "Version": "2012-10-17",
  "Statement": [
      {
        "Sid": "AddPermModelPackageVersion",
        "Effect": "Allow",
        "Principal": { "AWS": "arn:aws:iam::{}:root".format(model_training_account) },
        "Action": ["sagemaker:CreateModelPackage", "sagemaker:UpdateModelPackage"],
        "Resource": "arn:aws:sagemaker:{}:{}:model-package/{}/*".format(region, model_registry_account, model_package_group_name)
      }
    ]
  }

# arn:aws:sagemaker:us-east-1:803162095204:model-package-group/xgboost-demo-package-group

# Convert the policy from JSON dict to string
model_package_group_policy = json.dumps(model_package_group_policy)

# Set the new policy
response = sm_client.put_model_package_group_policy(
  ModelPackageGroupName=model_package_group_name,
  ResourcePolicy=model_package_group_policy)

