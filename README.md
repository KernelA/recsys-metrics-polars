# recsys-metrics-polars

## Description

Python library for computing some metrics for recomendations systems based on [polars](https://www.pola.rs/)

Available metrics:
* Precision at k
* Recall at k
* Average precision at k
* Mean average precision

[Documentation](https://kernela.github.io/recsys-metrics-polars/_autosummary/recsys_metrics_polars.data_info.html#module-recsys_metrics_polars.data_info)

## PyPI

[![PyPi version](https://badge.fury.io/py/recsys-metrics-polars.svg)](https://badge.fury.io/py/recsys-metrics-polars)

## Requirements

1. Python 3.9 or higher.

## How to run

1. [Install poetry](https://python-poetry.org/docs/#installation)
2. [Install poetry-version-plugin](https://pypi.org/project/poetry-version-plugin/)

Install dependencies:
```
poetry install --only main --no-root
```

For development:
```
poetry install --only main,dev --no-root
```

For docs:
```
poetry install --only main,dev,doc --no-root
```

## Tests

```
pytest ./tests
```

## Doc building

Install XeTeX

```
sphinx-build -n -b html ./docs/source/ ./docs/build/
```

