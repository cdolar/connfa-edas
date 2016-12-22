# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 07:53:12 2016

@author: c_dolar
"""
import datetime, csv, re

def extractAuthorInfo(infostr):
    """
        This function extracts data from the author information string.
        The string needs to be in the format Last_name, first_name (affiliation, country)
    """
    # pattern is (last_name, first_name (affliation, country))
    matches = re.search("^(.+),([^()]+)\((.+)\)$",infostr)
    speaker = Speaker(last_name=matches.groups()[0], first_name=matches.groups()[1].strip(),
                      organization=matches.groups()[2])
    return speaker

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
                 place="NULL", version="NULL", level_id="NULL", type_id="NULL", 
                 track_id="NULL", url="NULL", event_type="NULL", order="NULL", 
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
    
    def __rep__(self):
        return "Event: id {}, start_at {}, end_at {}, name {}, created_at {}, updated_at {}, deleted_at {}".format(self.id, self.start_at, self.end_at, self.name, self.created_at, self.updated_at, self.deleted_at)
    
    def __str__(self):
        return self.__rep__()

    def to_array(self):
        # id, start at, end at, text, name, place, version, level_id, type_id, 
        # track_id, url, event_type, order, deleted_at, created_at, updated_at
        return [self.id, self.start_at, self.end_at, self.text, self.name,
                self.place, self.version, self.level_id, self.type_id,
                self.track_id, self.url, self.event_type, self.order,
                self.deleted_at, self.created_at, self.updated_at]
    
    def update(self, event):
        self.start_at = event.start_at
        self.end_at = event.end_at
        self.text = event.text
        self.name = event.name
        self.place = event.place
        self.version = event.version
        self.level_id = event.level_id
        self.type_id = event.type_id
        self.track_id = event.track_id
        self.url = event.url
        self.event_type = event.event_type
        self.order = event.order
        self.deleted_at = event.deleted_at
        self.created_at = event.created_at
        self.updated_at = nowString()
    
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
    
    def __rep__(self):
        return "Track: id {}, name {}, created_at {}, updated_at {}, deleted_at {}".format(self.id, self.name, self.created_at, self.updated_at, self.deleted_at)
    
    def __str__(self):
        return self.__rep__()
    
    def to_array(self):
        return [self.id, self.name, self.deleted_at, self.created_at, 
                self.updated_at]
    
    def update(self, track):
        self.name = track.name
        self.order = track.order
        self.deleted_at = track.deleted_at
        self.created_at = track.created_at
        self.updated_at = nowString()
        
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
    
    def __rep__(self):
        return "EventSpeaker: id {}, event_id {}, speaker_id {}, name {}, created_at {}, updated_at {}".format(self.id, self.event_id, self.speaker_id, self.created_at, self.updated_at)
    
    def __str__(self):
        return self.__rep__()
    
    def to_array(self):
        return [self.id, self.event_id, self.speaker_id, self.created_at, 
                self.updated_at]
    
    def update(self, eventSpeaker):
        self.event_id = eventSpeaker.event_id
        self.speaker_id = eventSpeaker.speaker
        self.created_at = eventSpeaker.created_at
        self.updated_at = nowString()
        
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
    
    def __rep__(self):
        return "Speaker: id {}, first_name {}, last_name {}, created_at {}, updated_at {}, deleted_at {}".format(self.id, self.first_name, self.last_name, self.created_at, self.updated_at, self.deleted_at)
    
    def __str__(self):
        return self.__rep__()
    
    def to_array(self):
        return [self.id, self.first_name, self.last_name, self.characteristic,
                self.job, self.organization, self.twitter_name, self.website,
                self.avatar, self.email, self.order, self.created_at, 
                self.updated_at, self.deleted_at]
    
    def update(self, speaker):
        self.first_name = speaker.first_name
        self.last_name = speaker.last_name
        self.characteristic = speaker.characteristic
        self.job = speaker.job
        self.organization = speaker.organization
        self.twitter_name = speaker.twitter_name
        self.website = speaker.website
        self.avatar = speaker.avatar
        self.email = speaker.email
        self.order = speaker.order
        self.created_at = speaker.created_at
        self.updated_at = nowString()
        self.deleted_at = speaker.deleted_at

def speaker_from_array(array):
    return Speaker(id=array[0], first_name=array[1], last_name=array[2], 
                   characteristic=array[3], job=array[4], organization=array[5],
                   twitter_name=array[6], website=array[7], avatar=array[8],
                   email=array[9], order=array[10], created_at=array[11],
                   updated_at=array[12], deleted_at=array[13])

class ConnfaData:
    def __init__(self):
        self.tracks=[]
        self.lastTrackId=0
        self.events=[]
        self.lastEventId=0
        self.speakers=[]
        self.lastSpeakerId=0
        self.eventSpeakers=[]
        self.lastEventSpeakerId=0
    
    def loadData(self, speakersFilename="speakers_export.csv", 
                 eventsFilename="events_export.csv",
                 eventspeakersFilename="event_speakers_export.csv",
                 tracksFilename="tracks_export.csv"):
        # first, load the tracks
        with open(tracksFilename) as f:
            reader = csv.reader(f)
            for row in reader:
                newTrack = track_from_array(row)
                self.tracks.append(newTrack)
                self.lastTrackId = max(self.lastTrackId, newTrack.id)
        # now load the speakers
        with open(speakersFilename) as f:
            reader = csv.reader(f)
            for row in reader:
                newSpeaker = speaker_from_array(row)
                self.speakers.append(newSpeaker)
                self.lastSpeakerId = max(self.lastSpeakerId, newSpeaker.id)
        # now load the events
        with open(eventsFilename) as f:
            reader = csv.reader(f)
            for row in reader:
                newEvent = event_from_array(row)
                self.events.append(newEvent)
                self.lastEventId = max(self.lastEventId, newEvent.id)
        # now the event-speakers dad
        with open(eventspeakersFilename) as f:
            reader = csv.reader(f)
            for row in reader:
                newEventSpeaker = event_speaker_from_array(row)
                self.eventSpeakers.append(newEventSpeaker)
                self.lastEventSpeakerId = max(self.lastEventSpeakerId, newEventSpeaker.id)

    def insertSpeaker(self, speaker):
        matchSpeakers = self.getMatchingSpeakers(first_name=speaker.first_name, last_name=speaker.last_name)
        if len(matchSpeakers)==0:
            self.lastSpeakerId=self.lastSpeakerId+1
            speaker.id = self.lastSpeakerId
            self.speakers.append(speaker)
        else:
            matchSpeakers[0].update(speaker)
            if len(matchSpeakers) > 1:
                print("More than one match for speaker {}".format(speaker.__str__()))
        return speaker
    
    def insertTrack(self, track):
        matchTracks = self.getMatchingTracks(track.name)
        if len(matchTracks)==0:
            self.lastTrackId=self.lastTrackId+1
            track.id = self.lastTrackId
            self.tracks.append(track)
        else:
            matchTracks[0].update(track)
            if len(matchTracks) > 1:
                print("More than one match for track {}".format(track.__str__()))
        return track
    
    def insertEvent(self, event):
        matchEvents = self.getMatchingEvents(event.name)
        if len(matchEvents)==0:
            self.lastEventId+=1
            event.id = self.lastEventId
            self.events.append(event)
        else:
            matchEvents[0].update(event)
            if len(matchEvents) > 1:
                print("More than one match for event {}".format(event.__str__()))
        return event
    
    def insertEventSpeakers(self, event, speakers):
        pass
    
    def getMatchingSpeakers(self, first_name=None, last_name=None, updated_at=None):
        matchingSpeakers=[]
        for speaker in self.speakers:
            if first_name != None and speaker.first_name != first_name:
                continue
            if last_name != None and speaker.last_name != last_name:
                continue
            if updated_at != None and fromDateString(speaker.updated_at).date != fromDateString(updated_at).date():
                continue
            matchingSpeakers.append(speaker)
        return matchingSpeakers
    
    def getMatchingTracks(self, name=None, updated_at=None):
        matchingTracks = []
        for track in self.tracks:
            if name != None and name != track.name:
                continue
            if updated_at != None and fromDateString(track.updated_at).date != fromDateString(updated_at).date():
                continue
            matchingTracks.append(track)
        return matchingTracks
    
    def getMatchingEvents(self, title=None, updated_at=None):
        matchingEvents = []
        for event in self.events:
            if title != None and event.name == title:
                continue
            if updated_at != None and fromDateString(event.updated_at).date != fromDateString(updated_at).date():
                continue
            matchingEvents.append(event)
        return matchingEvents
    
class EDASData:    
    def __extractSessionData(self):
        with open(self.sessionsFileName) as f:
            reader = csv.reader(f)
            cols = reader.next()
            self.sessionData = {}
            for num,row in enumerate(reader):
                rowdata = {}
                for i,entry in enumerate(row):
                    rowdata[cols[i]]=entry
                rowdata['Papers'] = []
                rowdata['ID']=num
                self.sessionData[rowdata['Title']] = rowdata
    
    def __extractPaperData(self):
        with open (self.papersFileName, 'r') as f:
            reader = csv.reader(f)
            cols = reader.next()
            data = []
            self.speakers = {}
            for row in reader:
                rowdata={}
                for i,entry in enumerate(row):
                    rowdata[cols[i]]=entry
                try:
                    self.sessionData[rowdata['Session']]['Papers'].append(rowdata)
                except:
                    print("No session data for session {}".format(rowdata['Session']))
                    data.append(rowdata)
    
    def loadData(self, sessionsFileName="2017icce-sessions.csv", 
                 papersFileName="2017icce-papers.csv" ):
        self.sessionsFileName = sessionsFileName
        self.papersFileName = papersFileName
        self.__extractSessionData()
        self.__extractPaperData()
    
    def exportData(self, connfaData):
        """
            Export the data.
        """    
        for key in self.sessionData.keys():
            session = self.sessionData[key]
            # id, name, order, deleted, created, updated
            track = EventTrack(id=session['ID'], name=session['Title'],order=session['ID'])
            connfaData.insertTrack(track)
            if len(session['Papers']) > 0:
                for paper in session['Papers']:
                    sessionstarttime = datetime.strptime(paper['Session start time'],'%Y-%m-%d %H:%M')
                    min_per_paper=float(session['Minutes per paper'])
                    order = int(paper['Order in session'])
                    if ("poster" in session['Title'].lower()):                
                        starttime = session['Start time']
                        endtime = session['End time']
                    else:
                        starttime = (sessionstarttime + datetime.timedelta(minutes=(order-1)*min_per_paper)).strftime('%Y-%m-%d %H:%M')
                        endtime = (sessionstarttime + datetime.timedelta(minutes=order*min_per_paper)).strftime('%Y-%m-%d %H:%M')
                    event = Event(start_at=toDateString(starttime), end_at=toDateString(endtime),
                                  text=paper['Abstract'], name=paper['Title'], place=paper['Session room'], 
                                  type_id='1',track_id=session['ID'],url=paper['URL'], 
                                  event_type='session', order=paper['Order in session'])
                    for n in range(1,9):
                        author = paper['Author {}'.format(n)]
                        if len(author)>0:
                            speaker = extractAuthorInfo(author)
                            if n==1:
                                speaker.characteristic = paper['First author bio']
                            connfaData.insertSpeaker(speaker)
                            connfaData.insertEventSpeaker(event,speaker)
            else:
                event = Event(start_at=toDateString(session['Start time']), 
                              end_at=toDateString(session['End time']), text='', name=session['Title'], 
                              place=session['Room'], type_id='1', track_id=session['ID'], url='', 
                              event_type='session')
            connfaData.insertEvent(event)


if __name__ == "__main__":
    data = ConnfaData()
    data.loadData()
    edas = EDASData()
    edas.loadData()
    edas.exportTrackData(data)