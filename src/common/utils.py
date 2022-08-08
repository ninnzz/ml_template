"""Util functions."""
import json
import os
import re
from typing import Tuple

import boto3

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
    full_path = "/".join(segment[1:]).strip()
    return bucket_name, full_path, segment[-1]


def read_csv(config_file: str) -> dict:
    """

    Parameters
    ----------
    config_file :

    Returns
    -------
    config dictionary
    """
    if is_s3_file(config_file):
        s3 = boto3.client("s3")
        split = config_file.strip("s3://").split("/")
        bucket = split[0]
        file_key = "/".join(split[1:])
        result = s3.get_object(Bucket=bucket, Key=file_key)
        data = result["Body"].read().decode()
        data = json.loads(data)
    else:
        with open(config_file, encoding="UTF-8") as f:
            data = json.load(f)

    return data
