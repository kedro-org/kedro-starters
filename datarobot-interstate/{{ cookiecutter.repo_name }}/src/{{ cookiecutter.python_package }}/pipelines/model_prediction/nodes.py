import concurrent.futures
from typing import Any, Dict

import datarobot as dr
import pandas as pd


def fetch_predictions(tier, data, dr_deployments):
    deployment_info = dr_deployments[tier]
    scoring = data[tier]

    job, scores = dr.BatchPredictionJob.score_pandas(
        deployment_info["deployment_id"], scoring
    )
    job.wait_for_completion()

    return tier, scores


def predict(
    data: Dict[str, pd.DataFrame], dr_deployments: Dict[str, Any]
) -> Dict[str, pd.DataFrame]:
    predictions = {}

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(fetch_predictions, tier, data, dr_deployments)
            for tier in dr_deployments
        ]

        for _, future in zip(dr_deployments, futures):
            tier, scores = future.result()
            predictions[tier] = scores

    return predictions
