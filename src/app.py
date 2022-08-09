"""App entry point."""
import argparse
import logging
from typing import Tuple

from pydantic import BaseModel
from pydantic.error_wrappers import ValidationError

from src import __version__
from src.common.file_utils import check_images
from src.common.schema import Request, TrainingConfig
from src.common.utils import read_csv
from src.config import get_config


def parse_request(request_data: dict) -> Tuple[Request, TrainingConfig]:
    """

    Parameters
    ----------
    request_data :

    Returns
    -------
    request_config and process_config
    """
    rc = Request(**request_data)
    pc = None

    # No need to use else, type is handled in validation already
    if rc.process_type.value == "training":
        pc = TrainingConfig(**rc.params)

    return rc, pc


def get_arguments():
    """
    Gets the commandline arguments passes.

    Returns
    -------

    """
    config = get_config()
    parser = argparse.ArgumentParser(description=config.app_description)

    parser.add_argument(
        "-c",
        "--config",
        dest="config_path",
        required=True,
        type=str,
        help="Config file",
    )

    parser.add_argument(
        "-i",
        "--identifier",
        dest="identifier",
        required=True,
        type=str,
        default="xxx",
        help="Identifier for the process",
    )

    parser.add_argument("-v", "--version", action="version", version=__version__)

    return parser.parse_args()


def setup_logger() -> logging.Logger:
    """
    Logging setup.

    Returns
    -------
    logger instance
    """
    config = get_config()
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        level=logging.DEBUG,
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Setup s3 logs config
    logging.getLogger("boto3").setLevel(logging.CRITICAL)
    logging.getLogger("botocore").setLevel(logging.CRITICAL)
    logging.getLogger("s3transfer").setLevel(logging.CRITICAL)
    logging.getLogger("urllib3").setLevel(logging.CRITICAL)
    logger = logging.getLogger(config.logger_name)

    if config.log_to_file:
        logger.info("Adding file handler")
        file_handler = logging.FileHandler(config.log_file_path)
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def main():
    """Main function."""

    logger = setup_logger()
    args = get_arguments()

    # Reading config
    try:
        logger.info(f"Starting process: {args.identifier}")
        logger.info(f"Reading config from: {args.config_path}")
        request = read_csv(args.config_path)
        request_config, process_config = parse_request(request)
        logger.info(f"Reading config complete.")
    except (ValidationError, ValueError) as err:
        logger.error("Error in validating config.")
        logger.error(err)
        # Uses some sort of closing stuff???
        return
    except BaseException as err:
        logger.error("Unknown error occurred!")
        logger.error(err)
        return

    # NOTE:
    # For conventional purpose, each true_path contains the following sub folders
    # - raw contains the raw images
    # - preprocessed contains the result of the preprocessing, this will be used instead of raw
    # - result will contain the result of the process. For prediction, the images, for training, the model.
    try:
        logger.info(f"Checking images at: {process_config.image_location}")
        true_path = check_images(process_config.image_location, process_config.images)
    except ValueError as err:
        logger.error("Error on checking files!")
        logger.error(err)
        return

    # 1 read config
    # 2 load the image file
    # 3 if there is preprocessing, preprocess
    # 4 perform pred/training

    # Same as robo
    # Can be an API (?) ~5 IMAGES MAX??
    # download(img)
    # preprocess(img)
    # predict(img)
    #
    # OR

    # Check cloud
    # for img in images:
    #     download()
    #     preprocesses()
    #     img_list.append(img)
    #
    # predict(img_list)
