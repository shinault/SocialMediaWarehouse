import requests
import bz2
import os
import boto3

def download(src, destination, method="direct"):
    """Downloads data from external source

    Parameters:
    src (string): Specifies where the file (direct) or torrent is located
    destination (string): Specifies the filename to write to
    method (string): 'direct' (might add more later)
    """
    if method == "direct":
        r = requests.get(src)
        with open(destination, 'wb') as f:
            f.write(r.content)


def decompress(compressed_filename, decomp_filename, compression_method):
    """Decompresses a file and delete compressed file
    """
    if compression_method == "bz2":
        with open(decomp_filename, 'a+b') as f, bz2.open(compressed_filename, 'rb') as data:
            for line in data:
                f.write(line)
        os.remove(compressed_filename)        
    

def write_to_S3(filename, destination, bucket_name):
    """Writes file to S3 bucket and deletes copy from EC2 instance
    """
    s3 = boto3.resource('s3')
    with open(filename, 'rb') as data:
        s3.Bucket(bucket_name).put_object(Key=destination, Body=data)
    os.remove(filename)
    
