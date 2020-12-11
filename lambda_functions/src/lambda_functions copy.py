import boto3
import json
from os import path
from src.utils import utils

LAMDBA_ACCESS_POLICY_ARN = 'arn:aws:iam::495020021683:policy/Lambdas3AccessPolicy'
LAMBDA_ROLE = "Lambda_Execution_Role"
LAMBDA_ROLE_ARN = 'arn:aws:iam::495020021683:role/Lambda_Execution_Role'
LAMBDA_TIMEOUT = 10
LAMBDA_MEMORY = 128
LAMBDA_HANDLER = 'tony_function.handler'
PYTHON_36_RUNTIME = 'python3.6'
NODEJS_810_RUNTIME = 'nodejs12.x'
JAVA_8_RUNTIME = 'java8'
NODEJS_LAMDA_NAME = 'NodeJSLambdaFunction'
PYTHON_LAMBDA_NAME = 'TonyPythonLambdaFunction'
JAVA_LAMBDA_NAME = 'JavaLambdaFunction'

def lambda_client():
    aws_lambda = boto3.client ('lambda', region_name='eu-west-1')
    """ :type : pybotho3.lambda """
    return aws_lambda

def iam_client():
    iam = boto3.client('iam')
    """ :type : pyboto3.iam """
    return iam

def create_access_policy_for_lambda():
    s3_access_policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": [
                    "s3:*",
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents"
                ],
                "Effect": "Allow",
                "Resource": "*"
            }
        ]
    }

    return iam_client().create_policy(
        PolicyName='Lambdas3AccessPolicy',
        PolicyDocument=json.dumps(s3_access_policy_document),
        Description='Allows lambda function to access S3 resources'
     )

def create_execution_role_for_lambda():
    lambda_execution_assumption_role = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }
    return iam_client().create_role(
        RoleName=LAMBDA_ROLE,
        AssumeRolePolicyDocument=json.dumps(lambda_execution_assumption_role),
        Description="Gives necessary permission for lambda to be executed"
    )

def attach_access_policy_to_execution_role():
    return iam_client().attach_role_policy(
        RoleName=LAMBDA_ROLE,
        PolicyArn=LAMDBA_ACCESS_POLICY_ARN
    )

def deploy_lambda_function(function_name, runtime, handler, role_arn, source_folder):

    folder_path = path.join(path.dirname(path.abspath(__file__)), source_folder)

    if runtime is not JAVA_8_RUNTIME:
       zip_file = utils.make_zip_file_bytes(path=folder_path)
    else:
        zip_file = utils.read_jar_file(folder_path)

    return lambda_client().create_function(
        FunctionName=function_name,
        Runtime=runtime,
        Role=role_arn,
        Handler=handler,
        Code={
            'ZipFile': zip_file
        },
        Timeout=LAMBDA_TIMEOUT,
        MemorySize=LAMBDA_MEMORY,
        Publish=False
    )

def invoke_lambda_function (function_name):
    return lambda_client().invoke(FunctionName=function_name)

def add_environment_variables_to_lambda(function_name, variables):
    return  lambda_client().update_function_configuration(
        FunctionName=function_name,
        Environment=variables
    )

def update_lambda_function_code(function_name, source_folder):
    folder_path = path.join(path.dirname(path.abspath(__file__)), source_folder)
    zip_file = utils.make_zip_file_bytes(path=folder_path)

    return lambda_client().update_function_code(
        FunctionName=function_name,
        ZipFile=zip_file
    )

def publish_a_new_version(function_name):
    return lambda_client().publish_version(
        FunctionName=function_name
    )

def create_alias_for_new_version(function_name,alias_name, version):
    return lambda_client().create_alias(
        FunctionName=function_name,
        Name=alias_name,
        FunctionVersion=version,
        Description='This is the ' + alias_name + ' alias for function'
    )

def invoke_lambda_with_alias(function_name, alias_name):
    return lambda_client().invoke(
        FunctionName=function_name,
        Qualifier=alias_name
    )

def get_function(function_name):
    return lambda_client().get_function(FunctionName=function_name)

def get_all_functions():
    return lambda_client().list_functions()

def increase_lambda_execution_memory(function_name, new_memory_size):
    return lambda_client().update_function_configuration (
        FunctionName=function_name,
        MemorySize=new_memory_size
    )
def delete_lambda_function(function_name):
    return lambda_client().delete_function(FunctionName=function_name)


if __name__ == '__main__':
        # print(create_access_policy_for_lambda())
        # print(create_execution_role_for_lambda())
        # print(attach_access_policy_to_execution_role())
        # response = deploy_lambda_function(PYTHON_LAMBDA_NAME, PYTHON_36_RUNTIME, LAMBDA_HANDLER, LAMBDA_ROLE_ARN, 'python_lambda')
        # print (deploy_lambda_function(NODEJS_LAMDA_NAME, NODEJS_810_RUNTIME, LAMBDA_HANDLER, LAMBDA_ROLE_ARN, 'nodejs_lambda'))
        # print (deploy_lambda_function(JAVA_LAMBDA_NAME, JAVA_8_RUNTIME, 'com.amazonaws.lambda.demo.LambdaFunctionHandlerTest::handleRequest', LAMBDA_ROLE_ARN, 'Java_Lambda/dem-1.0.0.jar'))
        #response = invoke_lambda_function(PYTHON_LAMBDA_NAME)
        #print (response['Payload'].read().decode())
        #print(response)

        # env_variables = {
        #     'Variables': {
        #         'ENV_VAR_TEST': 'This is an environment variable!'
        #     }
        # }
        #
        # add_environment_variables_to_lambda(PYTHON_LAMBDA_NAME, env_variables)

        #print(update_lambda_function_code(PYTHON_LAMBDA_NAME, 'python_lambda'))

        #response = invoke_lambda_function(PYTHON_LAMBDA_NAME)
        #print (response['Payload'].read().decode())
        #print(publish_a_new_version(PYTHON_LAMBDA_NAME))
        #create_alias_for_new_version(PYTHON_LAMBDA_NAME, 'PROD', '1')
        #response = (invoke_lambda_with_alias(PYTHON_LAMBDA_NAME,"PROD"))
        #print (response['Payload'].read().decode())
        #print (get_function(PYTHON_LAMBDA_NAME))
        #print (get_all_functions())
        #increase_lambda_execution_memory(PYTHON_LAMBDA_NAME, 256)
        delete_lambda_function(NODEJS_LAMDA_NAME)
        # I messed up again
        


