from dataclasses import dataclass
from typing import List, Union


@dataclass
class DataInfo:
    """Information about data structure

    .. role:: python(code)
        :language: python

    For example:

    .. list-table:: User interactions
        :header-rows: 1
        :align: center

        * - user_id
          - item_id
          - score
        * - 0
          - 1
          - 0.01
        * - 0
          - 5
          - 10
        * - 1
          - 1
          - 0.2
        * - 2
          - 9
          - 7.96

    :py:attr:`.DataInfo.query_id_cols` is equal to :python:`"user_id"`

    :py:attr:`.DataInfo.item_col` is equal to :python:`"item_id"`

    :py:attr:`.DataInfo.score_col` is equal to :python:`"score"`

    In the example:

    .. list-table:: User interactions per session
        :header-rows: 1
        :align: center

        * - user_id
          - item_id
          - session_id
          - score
        * - 0
          - 10
          - 1
          - 0.01
        * - 0
          - 10
          - 5
          - 10
        * - 1
          - 20
          - 1
          - 0.2
        * - 2
          - 90
          - 9
          - 7.96

    :py:attr:`.DataInfo.query_id_cols` is equal to :python:`["user_id", "session_id"]`

    """

    query_id_cols: Union[str, List[str]]  #: Single or group of columns which unique identifier query
    item_col: str  #: Name of column with items
    score_col: str  #: Name of columns with item scores per query. For any pair of items, an item with higher score is more relevant.

    def __post_init__(self):
        if isinstance(self.query_id_cols, str):
            self.query_id_cols = [self.query_id_cols]
