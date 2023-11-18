import math

import polars as pl
import pytest

from recsys_metrics_polars import AvgPrecisionAtK, DataInfo
from recsys_metrics_polars.constants import RANK_COL

from .conftest import ITEM_ID_COL, MAX_ITEMS_PER_USER, SCORE_COL, SESSION_ID_COL, USER_ID_COL


def avg_prec_except_one_item_at_rank(k: int, excluded_rank: int):
    return (
        (0 if excluded_rank == 1 else 1)
        + math.fsum((i if i < excluded_rank else (i - 1)) / i for i in range(2, k + 1) if i != excluded_rank)
    ) / k


@pytest.mark.parametrize("group_cols", [USER_ID_COL, [SESSION_ID_COL, USER_ID_COL]])
def test_perfect_value(group_cols, true_interactions: pl.DataFrame, exact_recomendations: pl.DataFrame):
    prec_at_k = AvgPrecisionAtK(data_info=DataInfo(group_cols, ITEM_ID_COL, SCORE_COL))
    prec_at_k.fit(true_interactions, exact_recomendations)

    for k in range(1, MAX_ITEMS_PER_USER + 2):
        metric_per_query = prec_at_k.compute_per_query(k=k)

        query_with_ones_value = metric_per_query.join(
            true_interactions.group_by(prec_at_k.data_info.query_id_cols).count().filter(pl.col("count") >= k),
            on=prec_at_k.data_info.query_id_cols,
        )
        average_value = prec_at_k.avergae_over_queries(k=k)

        assert query_with_ones_value.filter(pl.col(f"avg_prec@{k}") < 1).is_empty()
        assert 0 <= average_value <= 1


@pytest.mark.parametrize("group_cols", [USER_ID_COL, [SESSION_ID_COL, USER_ID_COL]])
def test_zero_value(group_cols, true_interactions: pl.DataFrame, all_incorrect_recomendations: pl.DataFrame):
    prec_at_k = AvgPrecisionAtK(data_info=DataInfo(group_cols, ITEM_ID_COL, SCORE_COL))
    prec_at_k.fit(true_interactions, all_incorrect_recomendations)

    for k in range(1, MAX_ITEMS_PER_USER + 2):
        metric_per_query = prec_at_k.compute_per_query(k=k)
        average_value = prec_at_k.avergae_over_queries(k=k)
        assert metric_per_query.filter(pl.col(f"avg_prec@{k}") > 0).is_empty()
        assert pytest.approx(0.0) == average_value


def test_intremediate_value():
    true_interactions = pl.DataFrame(
        {
            USER_ID_COL: [0, 0, 0],
            ITEM_ID_COL: [1, 2, 3],
        },
        schema={USER_ID_COL: pl.UInt16, ITEM_ID_COL: pl.UInt16},
    )

    orig_rec = pl.DataFrame(
        {USER_ID_COL: [0, 0, 0], ITEM_ID_COL: [1, 2, 3], SCORE_COL: [3, 2, 1]},
        schema={USER_ID_COL: pl.UInt16, ITEM_ID_COL: pl.UInt16, SCORE_COL: pl.Float32},
    )

    avg_prec = AvgPrecisionAtK(data_info=DataInfo(USER_ID_COL, ITEM_ID_COL, SCORE_COL))

    incorrect_item_id = orig_rec.get_column(ITEM_ID_COL).max() + 1

    k = len(true_interactions)

    for excluded_item_id in orig_rec.get_column(ITEM_ID_COL):
        recs = orig_rec.with_columns(
            pl.when(pl.col(ITEM_ID_COL) == excluded_item_id)
            .then(incorrect_item_id)
            .otherwise(pl.col(ITEM_ID_COL))
            .alias(ITEM_ID_COL)
        )
        avg_prec.fit(true_interactions, recs)
        # restore missing rank: missing_rank = sum((1, 2, ..., n)) - actual_sum_with_missing_rank
        excluded_rank = (1 + k) * k // 2 - avg_prec._joined_data.get_column(RANK_COL).sum()
        assert pytest.approx(avg_prec.avergae_over_queries(k=k)) == avg_prec_except_one_item_at_rank(k, excluded_rank)
