from typing import Any, Dict

import datarobot as dr


def select_models(dr_projects: Dict[str, Any]) -> Dict[str, Any]:

    dr_models = {}
    for tier in dr_projects:
        project_info = dr_projects[tier]
        project = dr.Project.get(project_id=project_info["project_id"])
        # most_accurate_model = project.get_top_model()
        top_ten_models = project.get_models()[0:10]
        most_accurate_model = top_ten_models[0]
        
        project_info["model_id"] = most_accurate_model.id
        project_info["model_type"] = most_accurate_model.model_type

        dr_models[tier] = project_info    

    return dr_models
