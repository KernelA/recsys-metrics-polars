import polars as pl

from .constants import RANK_COL
from .data_info import DataInfo


def join_true_recs_and_preprocess(
    true_interactions: pl.DataFrame,
    recommendations: pl.DataFrame,
    data_info: DataInfo,
) -> pl.DataFrame:
    """Join two tables and compute ranks based on :py:attr:

    :param true_interactions: _description_
    :param recommendations: _description_
    :return: _description_
    """
    data = true_interactions.lazy().join(
        recommendations.lazy().with_columns(
            pl.when(pl.col(data_info.score_col).is_not_null())
            .then(pl.col(data_info.score_col).rank(method="ordinal", descending=True).over(data_info.query_id_cols))
            .otherwise(pl.lit(None))
            .alias(RANK_COL)
        ),
        how="left",
        on=data_info.query_id_cols + [data_info.item_col],
    )

    return data.collect()
