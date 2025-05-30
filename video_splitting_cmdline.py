#__copyright__   = "Copyright 2024, VISA Lab"
#__license__     = "MIT"


import os
import subprocess
import math
import boto3

# bucket information

input_bucket_name = '1225248297-input'
output_bucket_name = '1225248297-stage-1'

# s3 client
s3 = boto3.client('s3')

# function to upload files to bucket
def upload_directory(local_path, bucket_name):

    for root, dirs, files in os.walk(local_path):
        for file in files:
            local_file_path = os.path.join(root, file)
            s3_key = os.path.relpath(local_file_path, local_path)
            s3_path = os.path.join(local_path.split('/')[-1], s3_key)
            s3.upload_file(local_file_path, bucket_name, s3_path)

def video_splitting_cmdline(video_filename):
    # Downloading a csv file  
    # from S3 bucket to local folder 
    local_filename = "/tmp/"+ video_filename
    s3.download_file( 
        Filename=local_filename, 
        Bucket=input_bucket_name, 
        Key=video_filename
    )
    filename = os.path.basename(video_filename)
    outdir = os.path.splitext(filename)[0]
    outdir = os.path.join("/tmp",outdir)
    output_dir = outdir
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    split_cmd = '/opt/bin/ffmpeg -ss 0 -r 1 -i ' +local_filename+ ' -vf fps=1 -start_number 0 -vframes 10 ' + outdir + "/" + 'output-%02d.jpg -y'
    try:
        subprocess.check_call(split_cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print(e.returncode)
        print(e.output)

    fps_cmd = 'ffmpeg -i ' + local_filename + ' 2>&1 | sed -n "s/.*, \\(.*\\) fp.*/\\1/p"'
    fps = subprocess.check_output(fps_cmd, shell=True).decode("utf-8").rstrip("\n")
    fps = math.ceil(float(fps))
    
    upload_directory(outdir, output_bucket_name)

    return outdir
