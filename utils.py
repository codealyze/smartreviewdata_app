import pusher
from google.cloud import storage

pusher_client = pusher.Pusher(
  app_id='646500',
  key='90edd8132c05fc383260',
  secret='e8253d89449627d3d477',
  cluster='ap2',
  ssl=True
)
def publish_message(channel, key, value):
    pusher_client.trigger(channel, 'predictions', {key: value})
    

def make_blob_public(bucket_name, blob_name):
    """Makes a blob publicly accessible."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.make_public()

    #print('Blob {} is publicly accessible at {}'.format(
     #   blob.name, blob.public_url))
    return blob_name, blob.public_url