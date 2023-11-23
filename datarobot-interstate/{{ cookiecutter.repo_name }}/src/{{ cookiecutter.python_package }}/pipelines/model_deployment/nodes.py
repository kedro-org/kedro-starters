from typing import Any, Dict

import datarobot as dr


def deploy_models(
    dr_models: Dict[str, Any], parameters: Dict[str, Any]
) -> Dict[str, Any]:

    dr_deployments = {}
    for tier in dr_models:
        model_info = dr_models[tier]
        pred_serv_id = dr.PredictionServer.list()[0].id
        deployment = dr.Deployment.create_from_learning_model(
            model_id=model_info["model_id"],
            label=model_info["project_name"],
            description=model_info["model_type"],
            default_prediction_server_id=pred_serv_id,
        )

        model_info["deployment_id"] = deployment.id
        dr_deployments[tier] = model_info

    return dr_deployments
