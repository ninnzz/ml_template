"""
Schema definition
"""
import enum
from typing import List, Tuple

from pydantic import AnyHttpUrl, BaseModel


class Processes(str, enum.Enum):
    training = "training"
    prediction = "prediction"
    auto_tuning = "auto_tuning"


class PreprocessingConfig(BaseModel):
    """Preprocessing."""

    id: str
    name: str
    params: dict


class TrainingConfig(BaseModel):
    """Training."""

    model_reference_id: str
    image_location: str  # can be s3 or local
    images: List[Tuple[str, int]]  # image keys and labels
    algo_class: str  # algorithm to use
    algo_config: dict
    has_preprocessing: bool = False
    preprocessing: List[PreprocessingConfig] | None  # Optional


class Request(BaseModel):
    """Request config."""

    process_type: Processes
    params: dict
    # Writes the output image from preprocessing
    write_preprocessing_results: bool | None = True
    timeout: int | None = 3600
    callback_url: AnyHttpUrl | None
    callback_retries: int | None = 3
