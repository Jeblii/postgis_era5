import dataclasses as dc

@dc.dataclass
class Config:
    path_to_nc_files: str
    database_url: str