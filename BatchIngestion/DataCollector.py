import os
import subprocess
import boto3

def download(src, destination, method="direct"):
    """Downloads data from external source

    Parameters:
    src (string): Specifies where the file (direct) or torrent is located
    destination (string): Specifies the filename to write to
    method (string): 'direct' (might add more later)
    """
    if method == "direct":
        subprocess.run(["wget", "-O", destination, src])


def decompress(compressed_filename, compression_method, extract_name="temp"):
    """Decompresses a file and delete compressed file
    """
    if compression_method == "bz2":
        subprocess.run(["bunzip2", compressed_filename])
    elif compression_method == "7z":
        subprocess.run(["7z", "x", compressed_filename, "-o" + extract_name])
        os.remove(compressed_filename)
    elif compression_method == "xz":
        subprocess.run(["xz", "--decompress", compressed_filename])

def write_to_S3(filename, destination, bucket_name):
    """Writes file to S3 bucket and deletes copy from EC2 instance
    """
    session = boto3.Session()
    s3 = session.client('s3')
    transfer_config = boto3.s3.transfer.TransferConfig(multipart_threshold=838860800,
                                                       multipart_chunksize=838860800)
    transfer = boto3.s3.transfer.S3Transfer(client=s3, config=transfer_config)
    transfer.upload_file(filename, bucket_name, destination)

def write_folder_to_S3(folder_name, s3_folder, bucket_name):
    for filename in os.listdir(folder_name):
        write_to_S3(folder_name + "/" + filename,
                    s3_folder + folder_name + "/" + filename,
                    bucket_name)
