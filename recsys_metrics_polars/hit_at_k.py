import polars as pl

from .constants import RANK_COL


def compute_hit_at_k(joined_true_with_recs: pl.DataFrame, k: int):
    """Compute hit at k

    :param joined_true_with_recs: _description_
    :param k: _description_
    :return: _description_
    """
    assert k > 0, "k must be psotive"
    assert RANK_COL in joined_true_with_recs.columns, f"Cannot find '{RANK_COL}' in the list of columns"
    metric_name = f"hit@{k}"

    if metric_name not in joined_true_with_recs.columns:
        joined_true_with_recs = joined_true_with_recs.with_columns(
            (pl.col(RANK_COL) <= k).fill_null(False).alias(metric_name)
        )

    return joined_true_with_recs
