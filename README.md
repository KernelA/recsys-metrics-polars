# recsys-metrics-polars

## Description

Python library for computing some metrics for recomendations systems based on [polars](https://www.pola.rs/)

Available metrics:
* [Precision at k](https://kernela.github.io/recsys-metrics-polars/_autosummary/recsys_metrics_polars.precision.html)
* [Recall at k](https://kernela.github.io/recsys-metrics-polars/_autosummary/recsys_metrics_polars.recall.html)
* [Average precision at k](https://kernela.github.io/recsys-metrics-polars/_autosummary/recsys_metrics_polars.avg_precision.html)
* [Mean average precision](https://kernela.github.io/recsys-metrics-polars/_autosummary/recsys_metrics_polars.avg_precision.html#recsys_metrics_polars.avg_precision.AvgPrecisionAtK.avergae_over_queries)

[Documentation](https://kernela.github.io/recsys-metrics-polars/index.html)

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
poetry install --only main,dev,test --no-root
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

