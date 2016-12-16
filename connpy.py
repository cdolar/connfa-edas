# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 16:52:42 2016

@author: c_dolar
"""
from datetime import datetime, timedelta
import csv
import requests
import json
import re

base_url = "https://connfa.cdolar.de/api/v2/"

def getTracksFromServer(url):
    response = requests.get(url+"getTracks")
    data = json.loads(response.text)
    return data

def getSessionsFromServer(url):
    response = requests.get(url+"getSessions")
    data = json.loads(response.text)
    return data
    
def getSpeakersFromServer(url):
    response = requests.get(url+"getSpeakers")
    data = json.loads(response.text)
    return data

#------------------------------------------------------------------------------

def extractAuthorInfo(infostr):
    """
        This function extracts data from the author information string.
        The string needs to be in the format Last_name, first_name (affiliation, country)
    """
    # pattern is (last_name, first_name (affliation, country))
    matches = re.search("^(.+),([^()]+)\((.+)\)$",infostr)
    return {'Last name':matches.groups()[0], 'First name':matches.groups()[1].strip(),
            'Organization':matches.groups()[2]}

def extractDateTime(datetimestr):
    """
        This function extracts the date and time from the server format to the
        format used in csv export
    """
    return datetimestr[:-8].replace('T',' ')

#------------------------------------------------------------------------------

def exportTrackData(sessionData,filename):
    """
        Export the track data.
    """    
    data = []
    for key in sessionData.keys():
        session = sessionData[key]
        # id, name, order, deleted, created, updated
        data.append([session['ID'], session['Title'],session['ID'],'NULL','NULL',datetime.now().strftime('%Y-%m-%d %H:%M')])
    with open(filename,"w") as f:
        writer = csv.writer(f)
        writer.writerows(data)


def exportEventData(eventExportData,filename):
    """
        Export the session data
    """
    with open(filename,"w") as f:
        writer = csv.writer(f)
        writer.writerows(eventExportData)


def exportSpeakers(speakerExportData, filename):
    with open(filename,"w") as f:
        writer = csv.writer(f)
        writer.writerows(speakerExportData)


def exportEventSpeaker(speakerEventExportData, filename):
    with open(filename,"w") as f:
        writer = csv.writer(f)
        writer.writerows(speakerEventExportData)
    
#------------------------------------------------------------------------------

def prepareEventData(sessionData):
    eventExportData = []
    paperid=1
    for key in sessionData.keys():
        session = sessionData[key]
        if len(session['Papers']) > 0:
            for paper in session['Papers']:
                sessionstarttime = datetime.strptime(paper['Session start time'],'%Y-%m-%d %H:%M')
                min_per_paper=float(session['Minutes per paper'])
                order = int(paper['Order in session'])
                if ("poster" in session['Title'].lower()):                
                    starttime = session['Start time']
                    endtime = session['End time']
                else:
                    starttime = (sessionstarttime + timedelta(minutes=(order-1)*min_per_paper)).strftime('%Y-%m-%d %H:%M')
                    endtime = (sessionstarttime + timedelta(minutes=order*min_per_paper)).strftime('%Y-%m-%d %H:%M')
                # id, start at, end at, text, name, place, version, level_id, type_id, track_id, url, event_type, order, deleted_at, created_at, updated_at
                eventExportData.append([paperid, starttime, endtime, paper['Abstract'], paper['Title'], paper['Session room'], 'NULL','NULL','1',session['ID'],paper['URL'], 'session', paper['Order in session'], 'NULL','NULL',datetime.now().strftime('%Y-%m-%d %H:%M')])
                #eventExportData.append(['NULL', starttime, endtime, paper['Abstract'], paper['Title'], paper['Session room'], 'NULL','NULL','1',session['ID'],paper['URL'], 'session', paper['Order in session'], 'NULL','NULL',datetime.now().strftime('%Y-%m-%d %H:%M')])
                paperid+=1
        else:
            eventExportData.append([paperid, session['Start time'], session['End time'], '', session['Title'], session['Room'], 'NULL','NULL','1',session['ID'], '', 'session', 'NULL', 'NULL','NULL',datetime.now().strftime('%Y-%m-%d %H:%M')])
            #eventExportData.append(['NULL', session['Start time'], session['End time'], '', session['Title'], session['Room'], 'NULL','NULL','1',session['ID'], '', 'session', 'NULL', 'NULL','NULL',datetime.now().strftime('%Y-%m-%d %H:%M')])
            paperid+=1
    return eventExportData

def syncEventData(eventExportData,url):
    serverEventData = getSessionsFromServer(url)
    # build a dictionary for indexing the paper in the eventExportData
    paperLookup = { eventExportData[linenum][4]:linenum for linenum in range(len(eventExportData)) }
    linesNotFound = range(len(eventExportData))
    if len(serverEventData) == 0:
        return
    for day in serverEventData['days']:
        for event_srv in day['events']:
            linenum = -1
            try:
                linenum = paperLookup[event_srv['name'].encode('utf-8')]
            except:
                print(event_srv)
                print("The event {} is on the server but not in local data".format(event_srv['name'].encode('utf-8')))
                if False: #disabled the deletion, was: event_srv[u'deleted'] is False:
                    #                       id,                   start at,                           end at,                           text,                              name,                             place,               version, level_id, type_id,            track_id,            url,              event_type,order,              deleted_at,                              created_at, updated_at
                    eventExportData.append([event_srv[u'eventId'],extractDateTime(event_srv[u'from']),extractDateTime(event_srv[u'to']),event_srv[u'text'].encode('utf-8'),event_srv['name'].encode('utf-8'),event_srv[u'place'],'NULL',  'NULL',   event_srv[u'type'], event_srv[u'track'], event_srv[u'link'],'session',event_srv[u'order'],datetime.now().strftime('%Y-%m-%d %H:%M'),'NULL',datetime.now().strftime('%Y-%m-%d %H:%M')])
                continue
            event_loc = eventExportData[linenum]
            if event_loc[0] != event_srv['eventId']:
                event_loc[0] = event_srv['eventId']
            linesNotFound.remove(linenum)
    for linenum in linesNotFound:
        print("The event {} is not yet on the server".format(event_srv['name']))
            

def updateEventIds(eventExportData):
    # ToDo: Update the event ids from server
    pass

#------------------------------------------------------------------------------

def prepareSpeakerData(speakerData):
    speakerExportData = []
    id = 1
    for authorkey in speakerData.keys():
        speaker = speakerData[authorkey]
        # id, first_name, last_name, characteristic, job, organization, twitter_name, website, avatar, email, order, created_at, updated_at, deleted_at
        speakerExportData.append([id, speaker['First name'], speaker['Last name'], speaker['Bio'], '', speaker['Organization'],'','','','','NULL','NULL',datetime.now().strftime('%Y-%m-%d %H:%M'),'NULL'])
        id+=1
    return speakerExportData

def updateSpeakerIds(speakerExportData):
    # ToDo: Update the speaker ids with the server data
    pass

#------------------------------------------------------------------------------

def prepareEventSpeakerData(sessionData, eventExportData, speakerExportData):
    eventSpeakerExportData = []
    eventIdLookup = {}
    for event in eventExportData:
        eventIdLookup[event[4]] = event[0]
    speakerIdLookup = {}
    for speaker in speakerExportData:
        speakerIdLookup['{}, {}'.format(speaker[2],speaker[1])] = speaker[0]
    id=1
    for key in sessionData.keys():
        session = sessionData[key]
        for paper in session['Papers']:
            for n in range(1,9):
                author = paper['Author {}'.format(n)]
                if len(author)>0:
                    speaker = extractAuthorInfo(author)
                    speakerkey = "{}, {}".format(speaker['Last name'], speaker['First name'])
                    eventSpeakerExportData.append([id, eventIdLookup[paper['Title']], speakerIdLookup[speakerkey],'NULL',datetime.now().strftime('%Y-%m-%d %H:%M')])
                    id+=1
    return eventSpeakerExportData

#------------------------------------------------------------------------------
    
def extractPaperData(paperCSVFile,sessionData):
    with open (paperCSVFile, 'r') as f:
        reader = csv.reader(f)
        cols = reader.next()
        data = []
        speakers = {}
        for row in reader:
            rowdata={}
            for i,entry in enumerate(row):
                rowdata[cols[i]]=entry
            try:
                sessionData[rowdata['Session']]['Papers'].append(rowdata)
            except:
                print("No session data for session {}".format(rowdata['Session']))
                data.append(rowdata)
            for n in range(1,9):
                author = rowdata['Author {}'.format(n)]
                if len(author)>0:
                    print author
                    speakerdata = extractAuthorInfo(author)
                    speakerkey = "{}, {}".format(speakerdata['Last name'], speakerdata['First name'])
                    speakerdata['Bio']=''
                    if n==1:
                        speakerdata['Bio'] = rowdata['First author bio']
                    if not speakerkey in speakers.keys(): 
                        speakers[speakerkey] = speakerdata
    return sessionData, speakers

#------------------------------------------------------------------------------

def extractSessionData(sessionCSVFile):
    with open(sessionCSVFile) as f:
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
    return data

#------------------------------------------------------------------------------

if __name__ == "__main__":
    sessionData = extractSessionData('2017icce-sessions.csv')
    sessionData, speakerData = extractPaperData('2017icce-papers.csv',sessionData)
    
    eventExportData = prepareEventData(sessionData)
    syncEventData(eventExportData, base_url)
    
    speakerExportData = prepareSpeakerData(speakerData)
    eventSpeakerExportData = prepareEventSpeakerData(sessionData, eventExportData, speakerExportData)

    exportTrackData(sessionData,"tracks_export.csv")
    exportEventData(eventExportData,"events_export.csv")
    exportSpeakers(speakerExportData,"speakers_export.csv")
    exportEventSpeaker(eventSpeakerExportData, "event_speakers_export.csv")
    
    for sessionName in sessionData.keys():
        print(" Session {} has {} papers:\n".format(sessionName, len(sessionData[sessionName]['Papers'])))
