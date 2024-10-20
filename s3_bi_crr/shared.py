from pydantic import BaseModel


class Bucket(BaseModel):
    name_prefix: str
    account_number: str
    region: str

    @property
    def name(self) -> str:
        return f"{self.name_prefix}-{self.region}-{self.account_number}"

    @property
    def arn(self) -> str:
        return f"arn:aws:s3:::{self.name}"
