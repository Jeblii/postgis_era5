import dataclasses as dc

@dc.dataclass
class DailyNorm:
    temperature_min: float
    temperature_mean: float
    temperature_max: float
    dewpoint_temperature_min: float
    dewpoint_temperature_mean: float
    dewpoint_temperature_max: float
