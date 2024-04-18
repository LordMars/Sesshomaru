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
    timezone: str = ""

    def __init__(self, request):
        self.scheduledWeekday = request["scheduledTime"].get("weekday", None)
        self.scheduledHour = request["scheduledTime"].get("hour", 0)
        self.scheduledMinute = request["scheduledTime"].get("minute", 0)
        self.timezone = request["scheduledTime"].get("timezone", "America/New_York")
        self.channelId = request["channelId"]
        self.messageBody = request["messageBody"]

    def getHour(self): return self.scheduledHour

    def getMinute(self): return self.scheduledMinute

    def getScheduledTime(self): return f"{self.scheduledHour}:{self.scheduledMinute}:00"

    def getTimezone(self): return  self.timezone

    def getMessage(self): return self.messageBody

    def getChannelId(self): return self.channelId

    def getObject(self):
        return {
            "scheduledWeekday": self.scheduledWeekday,
            "scheduledHour": self.scheduledHour,
            "scheduledMinute": self.scheduledMinute,
            "channelId": self.channelId,
            "messageBody": self.messageBody
        }