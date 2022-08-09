"""
Preprocessing related functions.

Preprocessing will only be called on specific images.
Each preprocessing approach has different configuration.
Please refer to sdd-common for preprocessing documentation.
"""
import os
from typing import Tuple

import cv2
from sdd_common import preprocess
from sdd_common.preprocess_pipeline import ImagePreprocessPipeline

from src.common.schema import PreprocessingConfig


def adjust_params(name: str, params: dict) -> dict:
    """
    Adjust parameters for special use cases.

    Some preprocessing have special variables such as files
    need to download/overwrite the files.

    If you need to add other special use cases, like file reading.
    Please add it here.

    Parameters
    ----------
    name :
    params :

    Returns
    -------
    params - new dict of parameters
    """

    if name == "TranslateImagePreprocess":
        params["template"] = cv2.imread(params["template"])

    return params


def get_pipeline(preprocessing: list[PreprocessingConfig]) -> ImagePreprocessPipeline:
    """
    Format and return preprocess pipeline.

    Formats each preprocessing and adds it to pipeline

    Parameters
    ----------
    preprocessing :

    Returns
    -------
    preprocessing pipeline
    """
    _preprocessing = [
        (getattr(preprocess, pr.name), adjust_params(pr.name, pr.params))
        for pr in preprocessing
    ]
    return ImagePreprocessPipeline(_preprocessing)


def perform_preprocessing(
    img_path: str,
    output_path: str,
    images: list[Tuple[str, int]],
    pipeline: ImagePreprocessPipeline,
):
    """
    Apply preprocessing on all image.

    Parameters
    ----------
    img_path :
    output_path :
    images :
    pipeline :

    Returns
    -------

    """
    # Temporary variable so I don't
    # forget the mask feature
    mask_img = None

    for img, _ in images:
        preprocessed = pipeline.transform(
            cv2.imread(os.path.join(img_path, img)), mask_img
        )

        # Write preprocessed file
        cv2.imwrite(os.path.join(output_path, img), preprocessed)
