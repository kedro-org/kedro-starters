import logging
from datetime import datetime
from typing import Any, Dict
import concurrent.futures

import datarobot as dr
import pandas as pd

log = logging.getLogger(__name__)


def format_date(date_str: str):
    return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")


def build_dr_otv_project(
    project_name: str,
    df_train: pd.DataFrame,
    target_col: str,
    datetime_col: str,
    n_backtests: int = 1,
    disable_holdout: bool = False,
    backtest_dates: dict | None = None,
    autopilot_mode: str = "quick",
):
    if backtest_dates is None:
        backtest_dates = {}

    project = dr.Project.create(
        sourcedata=df_train, project_name=project_name, max_wait=int(1e5)
    )

    if not backtest_dates:
        time_partition = dr.DatetimePartitioningSpecification(
            use_time_series=False,
            datetime_partition_column=datetime_col,
            disable_holdout=disable_holdout,
            number_of_backtests=n_backtests,
        )
    else:
        backtests = []
        for bt in range(n_backtests):
            dates = backtest_dates[f"backtest{bt}"]
            backtest = dr.BacktestSpecification(
                index=bt,
                primary_training_start_date=format_date(dates[0][0]),
                primary_training_end_date=format_date(dates[0][1]),
                validation_start_date=format_date(dates[1][0]),
                validation_end_date=format_date(dates[1][1]),
            )

            backtests.append(backtest)

        time_partition = dr.DatetimePartitioningSpecification(
            use_time_series=False,
            datetime_partition_column=datetime_col,
            disable_holdout=disable_holdout,
            number_of_backtests=n_backtests,
            backtests=backtests,
        )

    # create new feature list removing any DR derived date features
    project_fl = project.get_featurelists()
    informative_fl = [fl for fl in project_fl if fl.name == "Informative Features"][0]

    derived_names = ["(Year)", "(Month)", "(Day of Month)", "(Day of Week)"]
    if informative_fl.features is None:
        reduced_features = []
    else:
        reduced_features = [
            f for f in informative_fl.features if not any(d in f for d in derived_names)
        ]

    new_fl = project.create_featurelist("modeling_features", reduced_features)

    project.set_target(
        target=target_col,
        featurelist_id=new_fl.id,
        mode=autopilot_mode,
        worker_count=-1,
        partitioning_method=time_partition,
    )

    return project


def train_single_model(tier, training_data, parameters):
    project_name = parameters["project_name"] + f"_{tier}"
    log.info(f"Building models for {project_name}")

    df_train = training_data[tier]

    # run autopilot
    # ******************************************    
    # project = build_dr_otv_project(
    #     df_train=df_train,
    #     target_col=parameters["target_column"],
    #     datetime_col=parameters["datetime_column"],
    #     n_backtests=1,
    #     disable_holdout=True,
    #     autopilot_mode=dr.AUTOPILOT_MODE.QUICK,  
    #     project_name=project_name,
    # )
    # project.wait_for_autopilot()
    # ******************************************    

    # manually run GAM blueprint from repository
    # ******************************************
    project = build_dr_otv_project(
        df_train=df_train,
        target_col=parameters["target_column"],
        datetime_col=parameters["datetime_column"],
        n_backtests=1,
        disable_holdout=True,
        autopilot_mode=dr.AUTOPILOT_MODE.MANUAL,  
        project_name=project_name,
    )

    for bp in project.get_blueprints():
        if bp.model_type == "Generalized Additive Model":
            model_job = project.train_datetime(bp.id)
            _ = dr.models.modeljob.wait_for_async_model_creation(project.id, model_job.id) 
    # ******************************************

    return tier, {
        "project_name": project_name,
        "project_id": project.id,
    }


def train_models(
    training_data: Dict[str, pd.DataFrame], parameters: Dict[str, Any]
) -> Dict[str, Any]:
    dr_projects = {}

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(train_single_model, tier, training_data, parameters)
            for tier in training_data
        ]
        for _, future in zip(training_data, futures):
            tier, project_data = future.result()
            dr_projects[tier] = project_data

    return dr_projects