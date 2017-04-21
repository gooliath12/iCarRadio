import boto, sys, time, logger
import json
sys.path.append('../')
from boto import kinesis

KINESIS_STREAM_NAME = 'iCarRadio'
shard_id = 'shardId-000000000000'
auth = {"aws_access_key_id":"AKIAIIPJFPEH4TSOH3WA",
        "aws_secret_access_key":"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"}
conn = kinesis.connect_to_region('us-east-1',**auth)

tries = 0
while tries < 10:
    tries += 1
    time.sleep(1)
    try:
        response = conn.describe_stream(KINESIS_STREAM_NAME)
        if response['StreamDescription']['StreamStatus'] == 'ACTIVE':
            break
    except :
        print 'error while trying to describe kinesis stream'
else:
    raise TimeoutError('Stream is still not active, aborting...')

shard_ids = []
stream_name = None
if response and 'StreamDescription' in response:
    stream_name = response['StreamDescription']['StreamName']
    for shard_id in response['StreamDescription']['Shards']:
         shard_id = shard_id['ShardId']
         shard_iterator = conn.get_shard_iterator(stream_name, shard_id, 'LATEST')
         shard_ids.append({'shard_id' : shard_id ,'shard_iterator' : shard_iterator['ShardIterator'] })

tries = 0
result = []
while tries < 100:
     time.sleep(0.2)
     tries += 1
     response = conn.get_records(shard_iterator = shard_ids[0]['shard_iterator'], limit=2 )
     shard_iterator = response['NextShardIterator']
     if len(response['Records'])> 0:
        #   for res in response['Records']:
        #        result.append(res['Data'])
        #   return result , shard_iterator
        print json.dumps(response, indent=4, sort_keys=True)
        break
     else:
        print 'Empty Records.'
