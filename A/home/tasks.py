from bucket import bucket
from celery import  shared_task

# todo can be async?
def all_bucket_objects_tasks():
    result=bucket.get_objects()
    return result

@shared_task
def delete_object_task(key):
    print(f"delete_object_task called with key: {key}")
    bucket.delete_object(key)

@shared_task
def download_object_task(key):
    bucket.download_object(key)

def upload_object_task(key):
    bucket.upload_object(key)