import json, boto3


# The model registry account id of the model package group
# model_registry_account = "xxx"

# The model training account id where training happens
model_training_account = "xx"
kms_key_id =  "mrk-xx"
# bucket = "sbabs-sagemaker-models"

# 1. Create a policy for access to the ECR repository
# in the model training account for the model registry account model package group
# ecr_repository_policy = {"Version": "2012-10-17",
#     "Statement": [{"Sid": "AddPerm",
#         "Effect": "Allow",
#         "Principal": {
#           "AWS": "arn:aws:iam::{}:root".format(model_registry_account)
#         },
#         "Action": [
#           "ecr:BatchGetImage",
#           "ecr:Describe*"
#         ]
#     }]
# }
#
# # Convert the ECR policy from JSON dict to string
# ecr_repository_policy = json.dumps(ecr_repository_policy)
#
# # Set the new ECR policy
# ecr = boto3.client('ecr')
#
# response = ecr.set_repository_policy(
#     registryId = model_training_account,
#     repositoryName = "xgboost-demo-repo",
#     policyText = ecr_repository_policy
# )

# 2. Create a policy in the model training account for access to the S3 bucket
# bucket_policy = {"Version": "2012-10-17",
#     "Statement": [{"Sid": "AddPermBucket",
#         "Effect": "Allow",
#         "Principal": {"AWS": "arn:aws:iam::{}:root".format(model_registry_account)
#         },
#         "Action": [
#           "s3:GetBucketAcl"
#         ],
#         "Resource": "arn:aws:s3:::{}".format(bucket)
#     },{"Sid": "AddPermObject",
#         "Effect": "Allow",
#         "Principal": {"AWS": "arn:aws:iam::{}:root".format(model_registry_account)
#         },
#         "Action": [
#           "s3:GetObject",
#           "s3:GetObjectAcl"
#         ],
#         "Resource": "arn:aws:s3:::{}/*".format(bucket)
#     }]
# }

# Convert the S3 policy from JSON dict to string
# bucket_policy = json.dumps(bucket_policy)
#
# # Set the new bucket policy
# s3 = boto3.client("s3")
# response = s3.put_bucket_policy(
#     Bucket = bucket,
#     Policy = bucket_policy)

# 3. Create the KMS grant for the key used during training for encryption
# in the model training account to the model registry account model package group
# client = boto3.client("kms")
#
# response = client.create_grant(
#     GranteePrincipal=model_registry_account,
#     KeyId=kms_key_id
#     Operations=[
#         "Decrypt",
#         "GenerateDataKey",
#     ],
# )

client = boto3.client('kms')

response = client.create_grant(
    GranteePrincipal= "arn:aws:iam::{}:root".format(model_training_account),
    KeyId= kms_key_id,
    Operations=[
        'Decrypt',
        'GenerateDataKey',
    ]
);
