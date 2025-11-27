from typing import Any
from kedro.io import AbstractDataset
from sqlalchemy import create_engine, Engine


class SQLAlchemyEngineDataset(AbstractDataset):
    """
    Kedro dataset for creating and managing a SQLAlchemy Engine.

    Behavior:
    - `load()`: returns a new SQLAlchemy Engine from provided credentials.
    - `save()`: not implemented (engines are read-only objects in this context).
    """

    def __init__(self, credentials: dict[str, Any]):
        """
        Args:
            credentials: Dict containing SQLAlchemy connection parameters.
                Must include:
                - "con": SQLAlchemy connection string (e.g., "sqlite:///mydb.sqlite")
                Optional:
                - Any extra arguments supported by `sqlalchemy.create_engine()`.
        """
        self._connection_str = credentials["con"]
        self._connection_args = {
            key: value for key, value in credentials.items() if key != "con"
        }

    def load(self) -> Engine:
        """Create and return a SQLAlchemy Engine."""
        return create_engine(self._connection_str, **self._connection_args)

    def save(self, data):
        """Not implemented — engines are read-only datasets."""
        raise NotImplementedError("Saving an Engine is not supported.")

    def _describe(self) -> dict:
        """Return dataset metadata for Kedro catalog introspection."""
        return {"type": type(self).__name__}
