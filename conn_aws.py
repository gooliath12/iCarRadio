import boto

# Get Identity Pool and Role information
with open('./utils/aws_identity.txt') as keyfile:
    keys = keyfile.readlines()
    ACCOUNT_ID = keys[0].strip('\n').split()[2]
    IDENTITY_POOL_ID = keys[1].strip('\n').split()[2]
    ROLE_ARN = keys[2].strip('\n').split()[2]

# Use cognito to get an identity & Setup ATA
cognito = boto.connect_cognito_identity()
cognito_id = cognito.get_id(ACCOUNT_ID, IDENTITY_POOL_ID)
oidc = cognito.get_open_id_token(cognito_id['IdentityId'])
sts = boto.connect_sts()
assumedRoleObject = sts.assume_role_with_web_identity(ROLE_ARN, "XX", oidc['Token'])

# Connect to Kinesis
kinesis = boto.connect_kinesis(
    aws_access_key_id=assumedRoleObject.credentials.access_key,
    aws_secret_access_key=assumedRoleObject.credentials.secret_key,
    security_token=assumedRoleObject.credentials.session_token)

# kinesis.put_record()
