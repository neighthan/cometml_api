from pathlib import Path
from typing import Optional, Dict, List, Any
from os import path
import json
import requests
import pandas as pd

try:
    with open(path.join(Path.home(), ".comet_rest_key")) as f:
        API_KEY = f.read().strip()
except (FileNotFoundError, PermissionError):
    API_KEY = ""


def set_api_key(key: str) -> None:
    global API_KEY
    API_KEY = key


def _get_url(url: str, url_params: Optional[Dict[str, str]]=None) -> dict:
    response = requests.get(url, url_params, headers={"Authorization": API_KEY})

    if response.ok:
        return json.loads(response.content)
    else:
        response.raise_for_status()


def get_workspaces() -> List[str]:
    url = "https://www.comet.ml/api/rest/v1/workspaces"
    return _get_url(url)["workspaces"]


def get_projects(workspace: str) -> List[Dict[str, Any]]:
    url = f"https://www.comet.ml/api/rest/v1/projects"
    url_params = {"workspace": workspace}
    return _get_url(url, url_params)["projects"]


def get_project_names(workspace: str) -> List[str]:
    projects = get_projects(workspace)
    return [project["project_name"] for project in projects]


def get_project_names_and_ids(workspace: str) -> List[str]:
    projects = get_projects(workspace)
    return {project["project_name"]: project["project_id"] for project in projects}


def get_experiments(project_id: str) -> List[Dict[str, Any]]:
    url = f"https://www.comet.ml/api/rest/v1/experiments"
    url_params = {"projectId": project_id}
    return _get_url(url, url_params)["experiments"]


def get_raw_params(experiment_key: str) -> List[Dict[str, Any]]:
    url = f"https://www.comet.ml/api/rest/v1/experiment/params"
    url_params = {"experimentKey": experiment_key}
    params = _get_url(url, url_params)["results"]
    return params


def get_params(experiment_key: str) -> Dict[str, Any]:
    raw_params = get_raw_params(experiment_key)
    return {param["name"]: param["valueCurrent"] for param in raw_params}


def get_raw_others(experiment_key: str) -> List[Dict[str, Any]]:
    url = f"https://www.comet.ml/api/rest/v1/experiment/log-other"
    url_params = {"experimentKey": experiment_key}
    others = _get_url(url, url_params)["logOtherList"]
    return others


def get_others(experiment_key: str) -> Dict[str, Any]:
    raw_others = get_raw_others(experiment_key)
    return {other["name"]: other["valueCurrent"] for other in raw_others}


def get_html(experiment_key: str) -> str:
    url = f"https://www.comet.ml/api/rest/v1/experiment/html"
    url_params = {"experimentKey": experiment_key}
    return _get_url(url, url_params)["html"]


def get_code(experiment_key: str) -> str:
    url = f"https://www.comet.ml/api/rest/v1/experiment/code"
    url_params = {"experimentKey": experiment_key}
    return _get_url(url, url_params)["code"]


def get_stdout(experiment_key: str) -> str:
    url = f"https://www.comet.ml/api/rest/v1/experiment/stdout"
    url_params = {"experimentKey": experiment_key}
    return _get_url(url, url_params)["output"]


def get_installed_packages(experiment_key: str) -> List[str]:
    url = f"https://www.comet.ml/api/rest/v1/experiment/installed-packages"
    url_params = {"experimentKey": experiment_key}
    return _get_url(url, url_params)["packages"]


def get_graph(experiment_key: str) -> str:
    """
    No idea what format the graph is in...
    """
    url = f"https://www.comet.ml/api/rest/v1/experiment/graph"
    url_params = {"experimentKey": experiment_key}
    return _get_url(url, url_params)["graph"]


def get_image_data(experiment_key: str) -> List[Dict[str, Any]]:
    url = f"https://www.comet.ml/api/rest/v1/experiment/images"
    url_params = {"experimentKey": experiment_key}
    return _get_url(url, url_params)["images"]


def get_raw_metrics(experiment_key: str):
    url = f"https://www.comet.ml/api/rest/v1/experiment/metrics-raw"
    url_params = {"experimentKey": experiment_key}
    return _get_url(url, url_params)["metrics"]


def get_raw_metric_summaries(experiment_key: str) -> List[Dict[str, Any]]:
    url = f"https://www.comet.ml/api/rest/v1/experiment/metrics"
    url_params = {"experimentKey": experiment_key}
    return _get_url(url, url_params)["results"]


def get_metrics(experiment_key: str) -> Dict[str, pd.DataFrame]:
    # TODO: are the metric values really always strings?
    # I assume that all metric values are able to be converted to floats

    # for each metric, return a dataframe so that the user can have plots
    # indexed by timestamp, step, or timestamp + offset
    # (I assume that )
    # I don't know what "runContext" is, but I ignore it

    raw_metrics = get_raw_metrics(experiment_key)
    metrics = {}  # {metric_name: [(value, step, timestamp, offset)]}

    for raw_metric in raw_metrics:
        name = raw_metric["metricName"]
        raw_metric = (float(raw_metric["metricValue"]), raw_metric["step"], raw_metric["timestamp"], raw_metric["offset"])

        if name in metrics:
            metrics[name].append(raw_metric)
        else:
            metrics[name] = [raw_metric]

    metrics = {name: pd.DataFrame(metrics[name], columns=["value", "step", "timestamp", "offset"]) for name in metrics}
    return metrics


def get_experiments_with_params(project_id: str, query_params: Dict[str, Any]):
    """
    Return the keys of the experiments in `project_id` that match all of the query params.

    There are valueMin, valueMax, and valueCurrent for each param, but I think these should
    all be the same? I just check valueCurrent. I also convert to strings when checking
    equality (so querying for 200 is the same as for "200") because it seems that
    strings are always used in Comet's stored parameters.
    """

    experiments = get_experiments(project_id)
    experiment_keys = []
    for experiment in experiments:
        add_experiment = True
        key = experiment["experiment_key"]

        params = get_params(key)
        for name, value in query_params.items():
            matched = name in params and params[name] == value
            add_experiment &= matched

        if add_experiment:
            experiment_keys.append(key)
    return experiment_keys
