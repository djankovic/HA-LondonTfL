from enum import StrEnum
from typing import TypedDict, Union
from .tfl_data import TfLData
from .const import LINE_SHORT_NAMES


class TransportType(StrEnum):
    METRO = "METRO"
    BUS = "BUS"
    TRAM = "TRAM"
    TRAIN = "TRAIN"
    SHIP = "SHIP"
    FERRY = "FERRY"
    TAXI = "TAXI"


class DepartureDeviation(TypedDict):
    importance_level: int
    consequence: str
    message: str


class DepartureLine(TypedDict):
    id: Union[int, str]
    designation: str
    transport_mode: TransportType
    group_of_lines: str
    color: str
    provider: str


class Departure(TypedDict):
    destination: str
    deviations: list[DepartureDeviation] | None
    # direction: str
    direction_code: int
    # state: str
    # display: str
    # stop_point: dict
    line: DepartureLine
    # scheduled: str
    expected: str


def as_hasl_departures(data: TfLData) -> list[Departure]:
    """
    converts the list of departures into a format
    that HASL Departure card (3.2.0+) can understand

    the format can be found [here](https://github.com/hasl-sensor/lovelace-hasl-departure-card/blob/master/src/models.ts)
    """

    departures = data.get_departures()
    line_colours = data.get_line_colours()

    return [
        {
            "destination": dep["destination"],
            "deviations": None,
            "direction_code": 0,
            "line": {
                "id": data.line,
                "designation": LINE_SHORT_NAMES.get(data.line, str(dep["line"])),
                "transport_mode": (
                    TransportType.METRO
                    if dep["type"] == "Metros"
                    else (
                        TransportType.TRAIN
                        if dep["type"] == "Trains"
                        else TransportType.BUS
                    )
                ),
                "group_of_lines": "",
                "color": f"rgb({line_colours['r']}, {line_colours['g']}, {line_colours['b']})",
                "provider": "ha-londontfl",
            },
            "expected": dep["expected"],
        }
        for dep in departures
    ]
