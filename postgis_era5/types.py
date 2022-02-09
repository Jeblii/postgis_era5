import dataclasses as dc


@dc.dataclass(frozen=True)
class WGS84Point:
    """
    A point on earth in WGS 84 (EPSG 4326).

    Important:
        It is the constructors responsibility to ensure a point is valid. Specifically
        this means that ``-90 <= latitude <= 90 and -180 <= longitude <= 180``.

    Raises:
        ValueError: If ``latitude`` or ``longitude`` is out of bounds.

    See Also:
        See https://epsg.io/4326 for more info on the coordinate system.
    """

    latitude: float
    longitude: float

    def __post_init__(self) -> None:
        if not (-90.0 <= self.latitude <= 90.0):
            raise ValueError(
                f"latitude should be between -90 and 90 but found {self.latitude!r}"
            )

        if not (-180.0 <= self.longitude <= 180.0):
            raise ValueError(
                f"longitude should be between -180 and 180 but found {self.longitude!r}"
            )
