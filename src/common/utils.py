"""Util functions."""
import re
import os
import json
import boto3

from typing import Tuple

from src.config import get_config


def is_s3_file(url: str) -> bool:
    """
    Checks if url is from s3.

    Parameters
    ----------
    url : url string

    Returns
    -------
    boolean
    """
    pattern = re.compile("s3://(.+?)/(.+)")
    return pattern.match(url) is not None


def extract_s3_path(s3_path: str) -> Tuple[str, str, str]:
    """
    Gets s3 parth info from s3 string url.

    Parameters
    ----------
    s3_path :

    Returns
    -------
    bucket_name, full_path, filename
    """
    segment = s3_path.split("//")[1].split("/")

    bucket_name = segment[0]
    full_path = '/'.join(segment[1:]).strip()
    return bucket_name, full_path, segment[-1]


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


def read_csv(csv_file: str) -> dict:
    """

    Parameters
    ----------
    csv_file :

    Returns
    -------
    csv dictionary
    """
    if is_s3_file(csv_file):
        s3 = boto3.client("s3")
        split = csv_file.strip("s3://").split("/")
        bucket = split[0]
        file_key = "/".join(split[1:])
        result = s3.get_object(Bucket=bucket, Key=file_key)
        data = result["Body"].read().decode()
        data = json.loads(data)
    else:
        with open(csv_file, encoding="UTF-8") as f:
            data = json.load(f)

    return data
