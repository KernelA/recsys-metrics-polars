from abc import ABC, abstractmethod
from typing import Optional

import polars as pl

from .data_info import DataInfo
from .utils import join_true_recs_and_preprocess


class BaseRecMetric(ABC):
    """Base class for metrics"""

    def __init__(self, data_info: DataInfo):
        self.data_info = data_info
        self._joined_data: Optional[pl.DataFrame] = None

    def fit(self, true_interactions: pl.DataFrame, recommendations: pl.DataFrame) -> "BaseRecMetric":
        """Prepare data for metric computing

        :param true_interactions: true interactions
        :param recommendations: predicted interactions with scores for each pair query and item
        """
        self._joined_data = join_true_recs_and_preprocess(true_interactions, recommendations, self.data_info)
        return self

    def _hit_at_k_metric_name(self, k: int) -> str:
        return f"hit@{k}"

    @abstractmethod
    def compute_per_query(self, **kwargs) -> pl.DataFrame:
        """Compute metric per query"""
        pass

    @abstractmethod
    def avergae_over_queries(self, **kwargs) -> float:
        """Compute mean metric value over all queries"""
        pass


class BaseMetricAtK(BaseRecMetric):
    @abstractmethod
    def compute_per_query(self, k: int, **kwargs) -> pl.DataFrame:
        pass

    @abstractmethod
    def avergae_over_queries(self, k: int, **kwargs) -> float:
        pass
