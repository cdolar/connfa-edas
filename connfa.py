# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 07:53:12 2016

@author: c_dolar
"""
import datetime, csv

def nowString():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

def toDateString(dt):
    try:
        return dt.strftime('%Y-%m-%d %H:%M')
    except:
        return "NULL"

def fromDateString(st):
    try:
        return datetime.datetime.strptime(st,'%Y-%m-%d %H:%M')
    except ValueError:
        return None
    
class Event:
    def __init__(self, id=None, start_at=datetime.datetime.now, 
                 end_at=datetime.datetime.now, text="", name="",
                 place="NULL", version="NULL", level_id=None, type_id=None, 
                 track_id=None, url="NULL", event_type="NULL", order="NULL", 
                 deleted_at="NULL", created_at=nowString(), 
                 updated_at=nowString()):
        self.id = id
        self.start_at = start_at
        self.end_at = end_at
        self.text = text
        self.name = name
        self.place = place
        self.version = version
        self.level_id = level_id
        self.type_id = type_id
        self.track_id = track_id
        self.url = url
        self.event_type = event_type
        self.order = order
        self.deleted_at = deleted_at
        self.created_at = created_at
        self.updated_at = updated_at

    def to_array(self):
        # id, start at, end at, text, name, place, version, level_id, type_id, 
        # track_id, url, event_type, order, deleted_at, created_at, updated_at
        return [self.id, self.start_at, self.end_at, self.text, self.name,
                self.place, self.version, self.level_id, self.type_id,
                self.track_id, self.url, self.event_type, self.order,
                self.deleted_at, self.created_at, self.updated_at]
    
def event_from_array(array):
    return Event(id=array[0], start_at=array[1], end_at=array[2],
                     text=array[3], name=array[4], place=array[5], 
                     version=array[6], level_id=array[7], type_id=array[8],
                     track_id=array[9], url=array[10], event_type=array[11],
                     order=array[12],deleted_at=array[13],
                     created_at=array[14],updated_at=array[15])

class EventTrack:
    def __init__(self, id=None, name="", order="NULL", deleted_at="NULL",
                 created_at=nowString(), updated_at=nowString()):
        self.id = id
        self.name = name
        self.order = order
        self.deleted_at = deleted_at
        self.created_at = created_at
        self.updated_at = updated_at
    
    def to_array(self):
        return [self.id, self.name, self.deleted_at, self.created_at, 
                self.updated_at]
    
def track_from_array(array):
    return EventTrack(id=array[0], name=array[1], order=array[2],
                          deleted_at=array[3], created_at=array[4], 
                          updated_at=array[5])

class EventSpeaker:
    def __init__(self, id=None, event_id=None, speaker_id=None, 
                 created_at=nowString(), updated_at=nowString()):
        self.id = id
        self.event_id = event_id
        self.speaker_id = speaker_id
        self.created_at = created_at
        self.updated_at = updated_at
    
    def to_array(self):
        return [self.id, self.event_id, self.speaker_id, self.created_at, 
                self.updated_at]

def event_speaker_from_array(array):
    return EventSpeaker(id=array[0], event_id=array[1], speaker_id=array[2],
                        created_at=array[3], updated_at=array[4])

class Speaker:
    def __init__(self, id=None, first_name="", last_name="", characteristic="",
                 job="", organization="", twitter_name="", website="", 
                 avatar="", email="", order=None, 
                 created_at=nowString(), updated_at=nowString(),
                 deleted_at="NULL"):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.characteristic = characteristic
        self.job = job
        self.organization = organization
        self.twitter_name = twitter_name
        self.website = website
        self.avatar = avatar
        self.email = email
        self.order = order
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at
    
    def to_array(self):
        return [self.id, self.first_name, self.last_name, self.characteristic,
                self.job, self.organization, self.twitter_name, self.website,
                self.avatar, self.email, self.order, self.created_at, 
                self.updated_at, self.deleted_at]

def speaker_from_array(array):
    return Speaker(id=array[0], first_name=array[1], last_name=array[2], 
                   characteristic=array[3], job=array[4], organization=array[5],
                   twitter_name=array[6], website=array[7], avatar=array[8],
                   email=array[9], order=array[10], created_at=array[11],
                   updated_at=array[12], deleted_at=array[13])

class ConnfaData:
    def __init__(self):
        self.tracks=[]
        self.events=[]
        self.speakers=[]
        self.eventSpeakers=[]
    
    def load_data(self, speakersFilename="speakers_export.csv", 
                 eventsFilename="events_export.csv",
                 eventspeakersFilename="event_speakers_export.csv",
                 tracksFilename="tracks_export.csv"):
        # first, load the tracks
        with open(tracksFilename) as f:
            reader = csv.reader(f)
            for row in reader:
                self.tracks.append(track_from_array(row))
        # now load the speakers
        with open(speakersFilename) as f:
            reader = csv.reader(f)
            for row in reader:
                self.speakers.append(speaker_from_array(row))
        # now load the events
        with open(eventsFilename) as f:
            reader = csv.reader(f)
            for row in reader:
                self.events.append(event_from_array(row))
        # now the event-speakers dad
        with open(eventspeakersFilename) as f:
            reader = csv.reader(f)
            for row in reader:
                self.eventSpeakers.append(event_speaker_from_array(row))
    
    def importData(self, sessionsFileName="2017_sessions.csv", 
                   papersFileName="2017_papers.csv"):
        with open(sessionsFileName) as f:
            reader = csv.reader(f)
            cols = reader.next()
            data = {}
            for num,row in enumerate(reader):
                rowdata = {}
                for i,entry in enumerate(row):
                    rowdata[cols[i]]=entry
                rowdata['Papers'] = []
                rowdata['ID']=num
                data[rowdata['Title']] = rowdata
            
        

if __name__ == "__main__":
    data = ConnfaData()
    data.load_data()