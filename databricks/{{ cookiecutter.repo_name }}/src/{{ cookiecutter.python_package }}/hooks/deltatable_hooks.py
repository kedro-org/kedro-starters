import logging
from typing import Any, Dict, List

from kedro.framework.hooks import hook_impl
from kedro.io import DataCatalog, DataSetError
from kedro.pipeline import Pipeline
from pyspark import SparkConf
from pyspark.sql import SparkSession

logger = logging.getLogger(__name__)


class ManagedTableHooks:
    """
    Create or update delta-tables used in catalog
    """
    @hook_impl
    def after_context_created(self, context) -> None:
        """Initialises a SparkSession using the config
        defined in project's conf folder.
        """

        # Load the spark configuration in spark.yaml using the config loader
        parameters = context.config_loader.get("spark*", "spark*/**")
        spark_conf = SparkConf().setAll(parameters.items())

        # Initialise the spark session
        spark_session_conf = (
            SparkSession.builder.appName(context._package_name)
            .enableHiveSupport()
            .config(conf=spark_conf)
        )
        _spark_session = spark_session_conf.getOrCreate()
        _spark_session.sparkContext.setLogLevel("WARN")

    @hook_impl
    def after_pipeline_run(
        self, run_params: Dict[str, Any], pipeline: Pipeline, catalog: DataCatalog
    ):
        for ds_name in pipeline.all_outputs():
            try:
                ds_obj = catalog._get_dataset(ds_name)
                cls_name = ds_obj.__class__.__name__
            except DataSetError:
                continue  # ignore MemoryDataSets

            if cls_name == "ManagedTableDataSet":
                delta_catalog = ds_obj._table.catalog
                database = ds_obj._table.database
                table = ds_obj._table.table
                owner_group = ds_obj._table.owner_group
                if owner_group:
                    _get_spark().sql(
                        f"ALTER TABLE {delta_catalog}.{database}"
                        + f".{table} OWNER TO `{owner_group}`;"
                    )
                    logger.info(
                        f"Transferred ownership of "
                        + f"{delta_catalog}.{database}.{table} to {owner_group}"
                    )

    @hook_impl
    def before_pipeline_run(
        self, run_params: Dict[str, Any], pipeline: Pipeline, catalog: DataCatalog
    ):
        """
        Create or update delta-tables used in catalog before a pipeline runs.
        This will also confirm all input tables exist before the pipeline runs.
        It is possible for a table to exist but for the user to not have permission to the table.
        Please ensure you are running the pipeline with the correct user.

        Args:
            run_params: kedro run parameters
            pipeline: kedro pipeline
            catalog: kedro catalog

        Returns:

        Raises:
            RuntimeError

        """
        for ds_name in pipeline.inputs():
            try:
                ds_obj = catalog._get_dataset(ds_name)
                cls_name = ds_obj.__class__.__name__
            except DataSetError:
                continue  # ignore MemoryDataSets

            if cls_name == "ManagedTableDataSet":
                delta_catalog = ds_obj._table.catalog
                database = ds_obj._table.database
                table = ds_obj._table.table
                schema = ds_obj._table.schema()
                owner_group = ds_obj._table.owner_group
                partition_columns = ds_obj._table.partition_columns
                table_location = ds_obj._table.full_table_location()
                if not is_database_exists(
                    delta_catalog, database
                ) or not is_table_exists(table, delta_catalog, database):
                    raise RuntimeError(
                        f"Table {delta_catalog}.{database}.{table} does not exist"
                    )

        for ds_name in pipeline.all_outputs():
            try:
                ds_obj = catalog._get_dataset(ds_name)
                cls_name = ds_obj.__class__.__name__
            except DataSetError:
                continue  # ignore MemoryDataSets

            if cls_name == "ManagedTableDataSet":
                delta_catalog = ds_obj._table.catalog
                database = ds_obj._table.database
                table = ds_obj._table.table
                schema = ds_obj._table.schema()
                owner_group = ds_obj._table.owner_group
                partition_columns = ds_obj._table.partition_columns
                table_location = ds_obj._table.full_table_location()

                if not is_database_exists(delta_catalog, database):
                    create_database(delta_catalog, database, owner_group)
                if schema:
                    create_or_alter_table(
                        catalog_name=delta_catalog,
                        database_name=database,
                        table_name=table,
                        schema=schema,
                        table_location=table_location,
                        partition_columns=partition_columns,
                    )
        if catalog.layers:
            for dataset_name in list(catalog.layers.get("monitoring", [])):
                dataset = eval(f"catalog.datasets.{dataset_name}")
                delta_catalog = dataset._catalog
                database = dataset._database
                # schema = dataset._schema
                owner_group = dataset._owner_group
                if not is_database_exists(delta_catalog, database):
                    create_database(delta_catalog, database, owner_group)


def _get_spark():
    return (
        SparkSession.builder.getOrCreate()
    )


def create_or_alter_table(
    catalog_name: str,
    table_name: str,
    schema: Dict[str, Any],
    database_name: str = "default",
    table_location: str = None,
    partition_columns: List[str] = None,
    owner: str = None,
) -> None:
    full_table_address = f"{catalog_name}.{database_name}.{table_name}"

    if is_table_exists(table_name, catalog_name, database_name):
        logger.info(f"Found existing table {full_table_address}")

        data_frame = _get_spark().table(full_table_address)
        existing_schema = data_frame.schema.jsonValue()
        existing_fields = existing_schema["fields"]
        incoming_fields = schema["fields"]
        new_columns = set(field["name"] for field in incoming_fields) - set(
            field["name"] for field in existing_fields
        )
        if new_columns:
            new_fields = [
                field for field in incoming_fields if field["name"] in new_columns
            ]
            columns = " ".join(
                [column["name"] + " " + column["type"] + "," for column in new_fields]
            ).strip(",")
            query = f"""ALTER TABLE {catalog_name}.{database_name}.{table_name} \\
                    ADD COLUMNS ({columns})"""
            logger.info("Running query: " + query)
            _get_spark().sql(query)
            if owner:
                _get_spark().sql(
                    f"ALTER TABLE {catalog_name}.{database_name}"
                    + f".{table_name} OWNER TO `{owner}`;"
                )
        else:
            logger.info(f"Table {full_table_address} conforms to schema")
            if owner:
                _get_spark().sql(
                    f"ALTER TABLE {catalog_name}.{database_name}"
                    + f".{table_name} OWNER TO `{owner}`;"
                )

    else:
        logger.info(f"Table {full_table_address} not found")

        create_table(
            catalog_name,
            table_name,
            schema,
            database_name,
            table_location,
            partition_columns,
            owner,
        )


def is_table_exists(
    table_name: str, catalog_name: str = "main", database_name: str = "default"
) -> bool:
    if catalog_name:
        _get_spark().sql(f"USE CATALOG {catalog_name}")
    try:
        return (
            _get_spark()
            .sql(f"SHOW TABLES IN `{database_name}`")
            .filter(f"tableName = '{table_name}'")
            .count()
            > 0
        )
    except:
        return False


def is_database_exists(
    catalog_name: str = "main", database_name: str = "default"
) -> bool:
    if catalog_name:
        return (
            _get_spark()
            .sql(f"SHOW SCHEMAS IN `{catalog_name}`")
            .filter(f"databaseName = '{database_name}'")
            .count()
            > 0
        )
    else:
        return (
            _get_spark()
            .sql(f"SHOW SCHEMAS")
            .filter(f"databaseName = '{database_name}'")
            .count()
            > 0
        )


def create_table(
    catalog_name: str,
    table_name: str,
    schema: Dict[str, Any],
    database_name: str = "default",
    table_location: str = None,
    partition_columns: List[str] = None,
    owner: str = None,
) -> None:
    fields = schema["fields"]

    columns = " ".join(
        [field["name"] + " " + field["type"] + "," for field in fields]
    ).strip(",")

    query = f"""CREATE TABLE {catalog_name}.{database_name}.{table_name} \\
    ({columns}) USING DELTA"""
    if partition_columns:
        query += f" PARTITIONED BY ({','.join(partition_columns)})"
    if table_location:
        query += f" LOCATION '{table_location}'"

    logger.info("Running query: " + query)
    _get_spark().sql(query)
    if owner:
        _get_spark().sql(
            f"ALTER TABLE {catalog_name}.{database_name}"
            + f".{table_name} OWNER TO `{owner}`;"
        )


def create_database(catalog_name: str, database_name: str, owner: str) -> None:
    full_database_path = catalog_name + "." + database_name if catalog_name else database_name
    logger.info("Creating database: " + full_database_path)
    if catalog_name:
        _get_spark().sql(f"USE CATALOG {catalog_name};")
    _get_spark().sql(f"CREATE SCHEMA IF NOT EXISTS {database_name};")
    logger.info("Database: " + full_database_path + " created.")
    if owner:
        _get_spark().sql(
            f"ALTER SCHEMA {catalog_name}.{database_name} OWNER TO `{owner}`;"
        )
        logger.info(
            "Database: "
            + catalog_name
            + "."
            + database_name
            + " owner set to: "
            + owner
        )
