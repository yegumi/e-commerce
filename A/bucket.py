import boto3
from django.conf import settings
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

class Bucket:
    '''
    CDN bucket manager

    init method creates connection.
    Note:
        none of these objs are asyn. use publicck inteface in tasks.py module instead
    '''

    def __init__(self):
        session=boto3.session.Session()
        self.conn=session.client(service_name=settings.AWS_SERVICE_NAME,
                                 aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                 aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                 endpoint_url=settings.AWS_S3_ENDPOINT_URL)



    def get_objects(self):
        result=self.conn.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
        if result['KeyCount']:
            return result['Contents']
        return None

    def delete_object(self, key):
        try:

            self.conn.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
            logger.info(f"Attempting to delete object with ID: {key}")
        except Exception as e:
            logger.error(f"Failed to delete object with ID: {key}. Error: {e}")
        return True
    def download_object(self, key):
        with open(settings.AWS_LOCAL_STORAGE + key, 'wb') as f :
            self.conn.download_fileobj(settings.AWS_STORAGE_BUCKET_NAME, key, f)


    def upload_object(self, key):
        self.conn.upload_file(settings.AWS_UPLOAD_STORAGE, settings.AWS_STORAGE_BUCKET_NAME, key)



bucket=Bucket()
