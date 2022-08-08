"""
File utility functions.

Handles file related operations such as
download and upload.
"""
import datetime
import hashlib
import os
from typing import List, Tuple

import boto3

from src.common.utils import extract_s3_path, is_s3_file
from src.config import get_config


def download_from_s3(s3_path: str) -> str:
    """
    Downloads s3 file and returns the local path.

    Parameters
    ----------
    s3_path : s3 url

    Returns
    -------
    filename: local file path
    """
    bucket_name, full_path, name = extract_s3_path(s3_path)
    config = get_config()

    if not os.path.isdir(config.temp_folder):
        os.mkdir(config.temp_folder)

    file_name = os.path.join(config.temp_folder, name)

    s3 = boto3.client("s3")

    s3.download_file(bucket_name, full_path, file_name)

    return file_name


def delete_local_file(path: str):
    """
    Deletes local s3 save file.

    :param path:
    :return:
    """
    os.remove(path)


# def upload_to_s3(file_path: str) -> str:
#     """
#     Upload a file to s3 location.
#
#     :param file_path:
#     :return:
#     """
#     s3 = boto3.resource('s3')
#     _, filename = os.path.split(file_path)
#     s3.meta.client.upload_file(file_path, bucket, filename)
#     delete_local_file(file_path)
#     return f's3://{bucket}/{filename}'


def download_s3_files(s3_path: str, images: List[Tuple[str, int]]) -> str:
    """
    Transfer files locally.

    Parameters
    ----------
    s3_path :
    images :

    Returns
    -------
    local_path: Local path of images
    """
    config = get_config()

    folder = hashlib.md5(
        datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S").encode()
    ).hexdigest()

    folder = os.path.join(config.temp_folder, folder)

    raw = os.path.join(folder, "raw")
    pre_processed = os.path.join(folder, "preprocessed")
    result = os.path.join(folder, "result")

    # Create folder
    if not os.path.isdir(config.temp_folder):
        os.mkdir(config.temp_folder)

    # Create all temp folders
    os.mkdir(folder)
    os.mkdir(raw)
    os.mkdir(pre_processed)
    os.mkdir(result)

    # Initialize s3
    s3 = boto3.client("s3")

    for img, _ in images:
        file_name = os.path.join(raw, img)
        print(file_name)
        # s3.download_file(bucket_name, full_path, file_name)

    return folder


def check_images(path: str, images: List[Tuple[str, int]]) -> str:
    """
    Checks folders and files.

    Parameters
    ----------
    path :
    images :

    Returns
    -------
    path of images if success
    """

    if is_s3_file(path):
        path = download_s3_files(path, images)
    else:
        if not os.path.isdir(path):
            raise ValueError("Invalid directory for images!")

        for img, _ in images:
            print(img)

    return path
