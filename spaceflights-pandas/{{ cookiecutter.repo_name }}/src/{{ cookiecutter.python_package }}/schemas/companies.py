"""Contracts for the ``companies`` dataset family."""

import pandera.pandas as pa


class RawCompaniesSchema(pa.DataFrameModel):
    """Contract on the raw supplier file, validated when it is loaded.

    Raw ``company_rating`` is a percentage string such as ``"100%"`` and
    ``iata_approved`` is ``t`` or ``f``. Extra columns are allowed so the
    example stays useful when the supplier adds one.
    """

    id: int = pa.Field(nullable=False, unique=True)
    company_rating: str = pa.Field(nullable=True, str_matches=r"^\d+%$")
    iata_approved: str = pa.Field(nullable=True, isin=["t", "f"])

    class Config:
        strict = False
        coerce = True
