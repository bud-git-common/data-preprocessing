import boto3
access_key_id = 'AKIA4CKBAUIL6DB7U3Z4'
secret_access_key = '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'

def download_images_from_s3(bucket_name, folder_path, image_names, local_folder):
    s3_client = boto3.client('s3', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)

    # List objects in the specified folder path
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_path, Delimiter='/')

    # Iterate over objects
    for content in response.get('Contents', []):
        key = content['Key']

        # Check if it's a subfolder
        if content['Size'] == 0 and key.endswith('/'):
            subfolder = key[len(folder_path):].rstrip('/')

            # Recursive call to download_images_from_s3 for the subfolder
            download_images_from_s3(bucket_name, key, image_names, local_folder)

        # Check if it's an image file
        if key in image_names:
            try:
                # Download the image from S3
                s3_client.download_file(bucket_name, key, local_folder + '/' + key.split('/')[-1])
                print(f"Downloaded image: {key}")
            except Exception as e:
                print(f"Error downloading image {key}: {str(e)}")


# Example usage
bucket_name = 'ui-training-set'
folder_path = 'Raw Data Set/mobbin_rerun/'
image_names = ['1Password-May 2023-Adding & Creating-0135aa61-02d2-4365-92e8-7183630cb985.png']
local_folder = '../dataset_folder/mobbin'

download_images_from_s3(bucket_name, folder_path, image_names, local_folder)

