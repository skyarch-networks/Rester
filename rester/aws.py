from logging import getLogger
import boto3
from warrant.aws_srp import AWSSRP
from requests_aws4auth import AWS4Auth


class aws_login:
    logger = getLogger(__name__)

    def cognito_auth(self, region, identity_pool_id):
        boto3.setup_default_session(region_name=region)
        identity = boto3.client('cognito-identity', region_name=region)
        response = identity.get_id(IdentityPoolId=identity_pool_id)
        identity_id = response['IdentityId']

        resp = identity.get_credentials_for_identity(IdentityId=identity_id)

        secretkey = resp['Credentials']['SecretKey']
        accesskey = resp['Credentials']['AccessKeyId']
        session_token = resp['Credentials']['SessionToken']
        service = 'execute-api'
        return AWS4Auth(accesskey, secretkey, region, service, session_token=session_token), session_token

    def cognito_login(self, username, password, pool_id, client_id, region, account_id):
        aws = AWSSRP(username=username, password=password, pool_id=pool_id, client_id=client_id, pool_region=region)
        tokens = aws.authenticate_user()
        id_token = tokens['AuthenticationResult']['IdToken']

        logins = {'cognito-idp.' + region + '.amazonaws.com/' + pool_id: id_token}

        client = boto3.client('cognito-identity', region_name=region)
        cognito_identity_id = client.get_id(
            AccountId=account_id,
            IdentityPoolId=pool_id,
            Logins=logins
        )

        credentials = client.get_credentials_for_identity(
            IdentityId=cognito_identity_id['IdentityId'],
            Logins=logins
        )
        accesskey = credentials['Credentials']['AccessKeyId']
        secretkey = credentials['Credentials']['SecretKey']
        session_token = credentials['Credentials']['SessionToken']
        service = 'execute-api'
        return AWS4Auth(accesskey, secretkey, region, service, session_token=session_token), session_token
