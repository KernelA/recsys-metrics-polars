import polars as pl

from .base import BaseMetricAtK
from .hit_at_k import compute_hit_at_k


class PrecisionAtK(BaseMetricAtK):
    """
    Precision@k

    :math:`Precision@k = \\dfrac{\\text{Number of relevant items with rank} \\leq k}{k}`
    """

    def _compute_hit_at_k(self, k: int):
        assert self._joined_data is not None, "fit(...) first"
        self._joined_data = compute_hit_at_k(self._joined_data, k)

    def compute_per_query(self, k: int, **kwargs):
        self._compute_hit_at_k(k)
        hit_metric_name = self._hit_at_k_metric_name(k)
        return (
            self._joined_data.lazy()
            .group_by(self.data_info.query_id_cols)
            .agg((pl.sum(hit_metric_name).cast(pl.Float32) / k).alias(f"prec@{k}"))
            .collect()
        )

    def avergae_over_queries(self, k: int, **kwargs) -> float:
        self._compute_hit_at_k(k)
        hit_metric_name = self._hit_at_k_metric_name(k)
        return self._joined_data.select(pl.col(hit_metric_name).sum().cast(pl.Float32) / k)[
            0, 0
        ] / self._joined_data.n_unique(self.data_info.query_id_cols)
