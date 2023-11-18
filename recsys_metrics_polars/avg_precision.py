import polars as pl

from .base import BaseMetricAtK
from .constants import RANK_COL


class AvgPrecisionAtK(BaseMetricAtK):
    """Average precision and MAP (see :py:meth:`.AvgPrecisionAtK.avergae_over_queries`)

    AP@k

    .. math::
        & AP@k = \\dfrac{\\sum\\limits_{i=1}^{k} Precision@i \\cdot Rel(i)}{\\min(k, \\text{Total relevean items})}, \\\\
        & Rel(i) = \\begin{cases}
            1, \\text{item with rank } i \\text{ is relevant,} \\\\
            0, \\text{otherwise}
        \\end{cases}

    """

    def compute_per_query(self, k: int, **kwargs) -> pl.DataFrame:
        lazy_data = self._joined_data.lazy()

        # avg_prec(k) = sum_{i=1}^{i=min(k, number_of_relevant_items)} hit_at_rank(i) / i * relevant(i)
        # is is denum
        precision_at = (
            lazy_data.select(self.data_info.query_id_cols)
            .with_columns(
                (pl.col(self.data_info.query_id_cols[0]).cumcount().over(self.data_info.query_id_cols) + 1)
                .alias("prec_k")
                .cast(self._joined_data.schema[RANK_COL])
            )
            .filter(pl.col("prec_k") <= k)
            .collect()
        )

        group_cols = self.data_info.query_id_cols + [RANK_COL]

        # hit_at_rank(i) * relevant(i)
        hit_at_rank = (
            precision_at.lazy()
            .join(
                lazy_data.group_by(group_cols).agg(pl.count(RANK_COL).alias("hit_at_k")),
                left_on=self.data_info.query_id_cols + ["prec_k"],
                right_on=group_cols,
                how="left",
            )
            .with_columns(
                pl.col("hit_at_k").fill_null(0),
                pl.when(pl.col("hit_at_k").is_null())
                .then(pl.lit(0, dtype=pl.Int8))
                .otherwise(pl.lit(1, dtype=pl.Int8))
                .alias("is_relevant_at_k"),
            )
            .sort("prec_k")
            .with_columns(pl.col("hit_at_k").cumsum().over(self.data_info.query_id_cols).cast(pl.Float32))
        )

        return (
            hit_at_rank.group_by(self.data_info.query_id_cols)
            .agg(
                ((pl.col("hit_at_k") / pl.col("prec_k") * pl.col("is_relevant_at_k")).sum() / pl.count()).alias(
                    f"avg_prec@{k}"
                )
            )
            .collect()
        )

    def avergae_over_queries(self, k: int, **kwargs) -> float:
        """Compute MAP@k

        .. math::
            MAP@k = \\dfrac{\\sum\\limits_{i=1}^N AP_i@k}{N},

        :math:`AP_i@k`- average precision for query :math:`i`, :math:`i \\in {1,2,\\ldots,N}, N-` total number of queries.
        """
        avg_per_query = self.compute_per_query(k=k)
        return avg_per_query.get_column(f"avg_prec@{k}").mean()
