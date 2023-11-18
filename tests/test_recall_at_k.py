import polars as pl
import pytest

from recsys_metrics_polars import DataInfo, RecallAtK

from .conftest import ITEM_ID_COL, MAX_ITEMS_PER_USER, SCORE_COL, SESSION_ID_COL, USER_ID_COL


@pytest.mark.parametrize("group_cols", [USER_ID_COL, [SESSION_ID_COL, USER_ID_COL]])
def test_perfect_value(group_cols, true_interactions: pl.DataFrame, exact_recomendations: pl.DataFrame):
    prec_at_k = RecallAtK(data_info=DataInfo(group_cols, ITEM_ID_COL, SCORE_COL))

    prec_at_k.fit(true_interactions, exact_recomendations)

    for k in range(1, MAX_ITEMS_PER_USER + 2):
        metric_per_query = prec_at_k.compute_per_query(k=k)
        average_value = prec_at_k.avergae_over_queries(k=k)
        assert metric_per_query.filter(pl.col(f"recall@{k}") < 1).is_empty()
        assert pytest.approx(1) == average_value


@pytest.mark.parametrize("group_cols", [USER_ID_COL, [SESSION_ID_COL, USER_ID_COL]])
def test_zero_value(group_cols, true_interactions: pl.DataFrame, all_incorrect_recomendations: pl.DataFrame):
    prec_at_k = RecallAtK(data_info=DataInfo(group_cols, ITEM_ID_COL, SCORE_COL))
    prec_at_k.fit(true_interactions, all_incorrect_recomendations)

    for k in range(1, MAX_ITEMS_PER_USER + 2):
        metric_per_query = prec_at_k.compute_per_query(k=k)
        average_value = prec_at_k.avergae_over_queries(k=k)
        assert metric_per_query.filter(pl.col(f"recall@{k}") > 0).is_empty()
        assert pytest.approx(0.0) == average_value
