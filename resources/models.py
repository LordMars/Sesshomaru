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

    def getObject(self):
        return {
            "name": self.name,
            "description": self.description,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "entity_type": self.entity_type,
            "location": self.location,
            "privacy_level": self.privacy_level
        }
    
@dataclass
class ScheduleMessageRequest:
    scheduledWeekday: str = ""
    scheduledHour: int = 0
    scheduledMinute: int = 0
    channelId: str = ""
    messageBody: str = ""

    def getObject(self):
        return {
            "scheduledWeekday": self.scheduledWeekday,
            "scheduledHour": self.scheduledHour,
            "scheduledMinute": self.scheduledMinute,
            "channelId": self.channelId,
            "messageBody": self.messageBody
        }