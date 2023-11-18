from typing import Optional

import polars as pl

from .base import BaseMetricAtK, BaseRecMetric
from .data_info import DataInfo
from .hit_at_k import compute_hit_at_k


class RecallAtK(BaseMetricAtK):
    """
    Recall@k

    :math:`Recall@k = \\dfrac{\\text{Number of relevant items with rank} \\leq k}{\\min(k, \\text{Total relevenat items for query})}`
    """

    _TOTAL_ITEMS_PER_GROUP_COL = "total_items_per_query"

    def __init__(self, data_info: DataInfo):
        super().__init__(data_info)
        self._total_items_per_query: Optional[pl.DataFrame] = None

    def fit(self, true_interactions: pl.DataFrame, recommendations: pl.DataFrame) -> BaseRecMetric:
        super().fit(true_interactions, recommendations)
        self._total_items_per_query = (
            self._joined_data.group_by(self.data_info.query_id_cols)
            .count()
            .with_columns(pl.col("count").alias(self._TOTAL_ITEMS_PER_GROUP_COL))
        )
        return self

    def _compute_hit_at_k(self, k: int):
        assert self._joined_data is not None, "fit(...) first"
        self._joined_data = compute_hit_at_k(self._joined_data, k)

    def compute_per_query(self, k: int, **kwargs):
        self._compute_hit_at_k(k)
        hit_metric_name = self._hit_at_k_metric_name(k)
        return (
            self._joined_data.lazy()
            .join(self._total_items_per_query.lazy(), on=self.data_info.query_id_cols)
            .group_by(self.data_info.query_id_cols)
            .agg(
                pl.sum(hit_metric_name).cast(pl.Float32).alias(f"recall@{k}"),
                pl.when(pl.max(self._TOTAL_ITEMS_PER_GROUP_COL) < k)
                .then(pl.max(self._TOTAL_ITEMS_PER_GROUP_COL))
                .otherwise(k)
                .alias(self._TOTAL_ITEMS_PER_GROUP_COL),
            )
            .with_columns(pl.col(f"recall@{k}") / pl.col(self._TOTAL_ITEMS_PER_GROUP_COL))
            .select(pl.col("*").exclude(self._TOTAL_ITEMS_PER_GROUP_COL))
            .collect()
        )

    def avergae_over_queries(self, k: int, **kwargs):
        metric_per_query = self.compute_per_query(k=k)
        return metric_per_query.get_column(f"recall@{k}").mean()
