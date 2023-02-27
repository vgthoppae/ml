import time
import os
from sagemaker import get_execution_role, session
import boto3

# boto3.setup_default_session(profile_name='sbabs-test')

region = boto3.Session().region_name
sm_client = boto3.client('sagemaker', region_name=region)
model_package_group_name = "arn:aws:sagemaker:us-east-1:xxx:model-package-group/xgboost-demo-package-group"
model_url = "s3://sbabs-sagemaker-models/sagemaker/DEMO-xgboost-dm/output/xgboost-2023-02-26-01-23-46-812/output/model.tar.gz"

def create_model_package_group():
  model_package_group_input_dict = {
   "ModelPackageGroupName" : model_package_group_name,
   "ModelPackageGroupDescription" : "Sample model package group"
  }
  create_model_package_group_response = sm_client.create_model_package_group(**model_package_group_input_dict)
  print('ModelPackageGroup Arn : {}'.format(create_model_package_group_response['ModelPackageGroupArn']))
#   arn:aws:sagemaker:us-east-1:803162095204:model-package-group/xgboost-demo-package-group

def register_model_version():
  model_package_inference_specification = {
    "InferenceSpecification": {
      "Containers": [
        {
          "Image": '811284229777.dkr.ecr.us-east-1.amazonaws.com/xgboost:latest',
          "ModelDataUrl": model_url
        }
      ],
      "SupportedContentTypes": ["text/csv"],
      "SupportedResponseMIMETypes": ["text/csv"],
    }
  }

  create_model_package_input_dict = {
    "ModelPackageGroupName": model_package_group_name,
    "ModelPackageDescription": "Model to detect 3 different types of irises (Setosa, Versicolour, and Virginica)",
    "ModelApprovalStatus": "PendingManualApproval"
  }
  create_model_package_input_dict.update(model_package_inference_specification)

  print(create_model_package_input_dict)

  create_model_package_response = sm_client.create_model_package(**create_model_package_input_dict)
  model_package_arn = create_model_package_response["ModelPackageArn"]
  print('ModelPackage Version ARN : {}'.format(model_package_arn))
  return model_package_arn


def approve_model_package():
  model_package_arn= "arn:aws:sagemaker:us-east-1:xxx:model-package/xgboost-demo-package-group/1"

  model_package_update_input_dict = {
    "ModelPackageArn": model_package_arn,
    "ModelApprovalStatus": "Approved"
  }
  model_package_update_response = sm_client.update_model_package(**model_package_update_input_dict)
  print(model_package_update_response)

# create_model_package_group();
# model_package_arn = register_model_version();
approve_model_package();

