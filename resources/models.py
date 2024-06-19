from dataclasses import dataclass
import datetime
import collections

@dataclass
class Poll:
    question = {
        "text": "Imprison the Delaney?",
    }
    answers = [
        {
            "answer_id": 1,
            "poll_media": {
                "text": "YES!!!"
            }
        },
        {
            "answer_id": 2,
            "poll_media": {
                "text": "Meh."
            }
        },
        {
            "answer_id": 3,
            "poll_media": {
                "text": "nah"
            }
        }
   ]
    duration: int = 1
    multi: bool = False
    layout: int = 1

    def __init__(self, question: str, answers: list[str]):
        self["question"]["text"] = question

        if answers:
            self["answers"] = []
            for i in range(len(answers)):
                answer = {
                    "answer_id": i+1,
                    "poll_media": {
                        "text": answers[i]
                    }
                }
                self["answers"].append(answer)

    def getJson(self):
        return {
            "poll": {
                "question": self.question,
                "answers": self.answers,
                "duration": self.duration,
                "allow_multiselect": self.multi,
                "layout_type": self.layout
            }
        }

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
    
@dataclass
class ActivityRequest:
    userName = ""
    memberId = None
    request = ""
    options = []

    def __init__(self, request, options, memberId, userName):
        self.memberId = memberId
        self.userName = userName
        self.request = request
        self.options = options

    def getJson(self):
        return {
            "userName": self.userName,
            "memberId": self.memberId,
            "request": self.request,
            "options": self.options
        }