import random

import polars as pl
import pytest

from recsys_metrics_polars.data_info import DataInfo

MAX_ITEMS_PER_USER = 5
USER_ID_COL = "user_id"
ITEM_ID_COL = "item_id"
SESSION_ID_COL = "session_id"
SCORE_COL = "score"


@pytest.fixture(scope="function")
def data_info():
    return DataInfo(USER_ID_COL, ITEM_ID_COL, SCORE_COL)


@pytest.fixture(scope="session")
def true_interactions():
    gen = random.Random(11233)
    user_ids = list(range(MAX_ITEMS_PER_USER))
    session_ids = user_ids.copy()
    item_ids = list(range(10))

    item_ids_per_user = [gen.sample(item_ids, k=i) for i in range(len(user_ids))]

    all_user_ids = []
    all_item_ids = []
    all_session_ids = []

    for user_id, session_id, item_ids in zip(user_ids, session_ids, item_ids_per_user):
        all_user_ids += [user_id] * len(item_ids)
        all_item_ids += item_ids
        all_session_ids += [session_id] * len(item_ids)

    return pl.DataFrame(
        {USER_ID_COL: all_user_ids, ITEM_ID_COL: all_item_ids, SESSION_ID_COL: all_session_ids},
        schema={USER_ID_COL: pl.UInt16, ITEM_ID_COL: pl.UInt16, SESSION_ID_COL: pl.UInt16},
    )


@pytest.fixture(scope="session")
def exact_recomendations(true_interactions: pl.DataFrame):
    return true_interactions.with_columns(
        -((pl.col(USER_ID_COL).cumcount() + 1).cast(pl.Int32)).alias(SCORE_COL).over(USER_ID_COL)
    )


@pytest.fixture(scope="session")
def all_incorrect_recomendations(true_interactions: pl.DataFrame):
    return true_interactions.with_columns(pl.col(ITEM_ID_COL).max() + 1, pl.lit(1).alias(SCORE_COL))
