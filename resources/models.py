from dataclasses import dataclass


@dataclass
class ScheduleEventRequest:
    name: str = ""
    description: str = ""
    start_time: str = ""
    end_time: str = ""
    entity_type: str = ""
    location: str = ""
    privacy_level: str = ""