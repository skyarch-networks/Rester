from logging import getLogger
import boto3
from requests_aws4auth import AWS4Auth


class aws_login:
    logger = getLogger(__name__)

    def cognito_login(self, region, identity_pool_id):
        boto3.setup_default_session(region_name=region)
        identity = boto3.client('cognito-identity', region_name=region)
        response = identity.get_id(IdentityPoolId=identity_pool_id)
        identity_id = response['IdentityId']

        resp = identity.get_credentials_for_identity(IdentityId=identity_id)

        secretKey = resp['Credentials']['SecretKey']
        accessKey = resp['Credentials']['AccessKeyId']
        sessionToken = resp['Credentials']['SessionToken']

        service = 'execute-api'
        return AWS4Auth(accessKey, secretKey, region, service, session_token=sessionToken), sessionToken