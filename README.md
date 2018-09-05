# comet_ml_api

This is a set of _unofficial_ Python bindings for the CometML REST API. There are functions for all current endpoints as well as a couple of functions that build on the basic endpoint ones to provide, e.g., simpler output or filtering. I haven't used all of the endpoints myself, so some of the functions haven't been tested at all (e.g. `get_html`). Documentation is currently limited but the functions provided are generally quite simple.

See [Endpoints][endpoints] for the official documentation of the REST API.

## Authentication

See [this page][api key] first for how to generate your REST API key. There are two possible methods of authentication using that key:
1. Store the key in `~/.comet_rest_key`. When you import the `api` script, it will automatically load a key that it finds in this file.
2. Call the `set_api_key` function and pass your key in. The key will be saved in a global variable so that the same key is used for all subsequent requests unless you explicitly set a new key.

## Endpoints

Most of the basic endpoint functions are named `get_<endpoint>` where `<endpoint>` is the corresponding endpoint (e.g. `get_workspaces` to access `https://www.comet.ml/api/rest/v1/workspaces`). However, there are a few exceptions.

### Metrics
There are two endpoints for metrics: `metrics` and `metrics-raw`. I call both of these "raw" because they return data that isn't well-formatted for immediate plotting/analysis. As the `metrics` endpoint only return the min, max, and most recent data points for a given metric, I call that one a summary, hence `get_raw_metric_summaries`; the function for `metrics-raw` is `get_raw_metrics`. There is also a helper function `get_metrics` which converts the metrics into a better format for visualization or analysis.

### Params
Similarly to metrics, the raw parameters data may not be in the most usable format right away. I thus also call this endpoint `get_raw_params` and have a helper function `get_params` which provides a more concise output.

### Other
As for params except, though the endpoint is `log-other`, the functions are `get_raw_others` and `get_others`.

### Images
The `images` endpoint doesn't return the images themselves, just the data about them (including the URLs from which the actual images can be downloaded?). I call this endpoint `get_image_data`, but I haven't tested it.

## Example Usage

```python
from comet_ml_api import api

workspaces = api.get_workspaces()
project_ids = api.get_project_names_and_ids(workspaces[0]) # {name: id}
experiments = api.get_experiments(project_ids.popitem()[1])
api.get_params(experiments[0]["experiment_key"])
```

[endpoints]: https://www.comet.ml/docs/rest-api/endpoints/
[api key]: https://www.comet.ml/docs/rest-api/getting-started/
