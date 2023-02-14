# run_kedro_pipeline.py
import argparse
import logging
from typing import Dict, List
from kedro.framework.project import configure_project
from kedro.framework.session import KedroSession

def unflatten(dictionary: Dict) -> Dict:
    """Unflattens an incoming dictionary with keys in the form 
    key1.key2.key3 into a nested dictionary

    Args:
        dictionary (Dict): The incoming dictionary with flat keys

    Returns:
        Dict: Unflattened dictionary with nested keys
    """
    resultDict = dict()
    for key, value in dictionary.items():
        parts = key.split(".")
        d = resultDict
        for part in parts[:-1]:
            if part not in d:
                d[part] = dict()
            d = d[part]
        d[parts[-1]] = value
    return resultDict

def params_parser(params: str) -> Dict:
    """Parses a command line argument in the form of key1:value1,key2:value2
    into a dictionary in python: {"key1":"value1", "key2":"value2"}

    Args:
        params (str): string representation of the params

    Returns:
        Dict: Python dictionary parsed according to the incoming params
    """
    result = dict()
    for i in params.split(","):
        key = i.split(":")[0]
        value = i.split(":")[1]
        result[key]=value
    return result

def params_joiner(params_list: List[Dict]) -> Dict:
    """ Joins a list of dictionaries into one dictionary

    Args:
        params_list (List[Dict]): List of dictionaries with flat keys

    Returns:
        Dict: One dictionary with all the keys that were in the list
    """
    result = dict()
    for param in params_list:
        result.update(param)
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", dest="package")
    parser.add_argument("--pipeline", dest="pipeline")
    parser.add_argument("--params", dest="params", type=params_parser, action="append")
    parser.add_argument("--tags", dest="tags", type=str)
    parser.add_argument("--env", dest="env", type=str)
    args = parser.parse_args()
    env = args.env
    package_name = args.package
    pipeline_name = args.pipeline
    params = unflatten(params_joiner(args.params))
    tags = None
    if args.tags:
        tags = [tag.strip() for tag in args.tags.split(",")]
    # https://kb.databricks.com/notebooks/cmd-c-on-object-id-p0.html
    logging.getLogger("py4j.java_gateway").setLevel(logging.ERROR)
    logging.getLogger("py4j.py4j.clientserver").setLevel(logging.ERROR)

    configure_project(package_name)

    with KedroSession.create(package_name, extra_params=params, env=env) as session:
        session.run(pipeline_name, tags=tags)
