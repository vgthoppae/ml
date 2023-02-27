from sagemaker import ModelPackage
from time import gmtime, strftime
import boto3

boto3.setup_default_session(profile_name='trep-acpt')

region = boto3.Session().region_name
sm_client = boto3.client('sagemaker', region_name=region)
# role= "arn:aws:iam::xxx:role/default-sagemaker-execution-role"
role= "arn:aws:iam::xxxx:role/default-sagemaker-execution-role"

model_version_arn = "arn:aws:sagemaker:us-east-1:xxx:model-package/xgboost-demo-package-group/1"
model_name = 'xgboost-demo-model-1'
endpoint_config_name = 'xgboost-demo-model-endpoint-config-1'
endpoint_name = 'xgboost-demo-model-endpoint-1'

def create_model():
  container_list = [{'ModelPackageName': model_version_arn}]

  create_model_response = sm_client.create_model(
    ModelName=model_name,
    ExecutionRoleArn=role,
    Containers=container_list
  )
  print("Model arn : {}".format(create_model_response["ModelArn"]))

def create_endpoint_config():
  print(endpoint_config_name)
  create_endpoint_config_response = sm_client.create_endpoint_config(
    EndpointConfigName=endpoint_config_name,
    ProductionVariants=[{
      'InstanceType': 'ml.t2.medium',
      'InitialVariantWeight': 1,
      'InitialInstanceCount': 1,
      'ModelName': model_name,
      'VariantName': 'AllTraffic'}])
  print(create_endpoint_config_response)

def create_endpoint():
  print("EndpointName={}".format(endpoint_name))

  create_endpoint_response = sm_client.create_endpoint(
    EndpointName=endpoint_name,
    EndpointConfigName=endpoint_config_name)
  print(create_endpoint_response['EndpointArn'])

# create_model();
# create_endpoint_config();
create_endpoint();#