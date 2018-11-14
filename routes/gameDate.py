from server import api
import tourneyDatabase
import json
import falcon
import persistent
import persistent.list
import transaction
import uuid
import shortuuid
from routes import pitch

class GameDate(persistent.Persistent):
    def __init__(self, id):
        self.id = id
        self.date = None
        self.gameTimes = persistent.list.PersistentList()
        self.pitches = persistent.list.PersistentList()

    def __str__(self):
        return str(self.date)

    @staticmethod
    def getGameDate(response, connection, id, dateId):
      tournament = connection.tournaments.getByShortId(id)                
      if not tournament:
        response.status = '404 Not Found'
        response.body = '{"message"="Tournament with id ' + id + ' not found."}'              
      else:
        fullDateId = shortuuid.decode(dateId)
        date = next((x for x in tournament.gameDates if x.id == fullDateId), None)
        if not date:
          response.status = '404 Not Found'
          response.body = '{"message"="Date with id ' + dateId + ' not found."}'              
        else:
          return (tournament, date)

      return (None, None)

    def ensureGameDate(self):
        if not hasattr(self, 'pitches'):
            self.pitches = persistent.list.PersistentList()
            transaction.commit()
        if not hasattr(self, 'gameTimes'):
            self.gameTimes = persistent.list.PersistentList()
            transaction.commit()

    def ensurePitch(self):
        self.ensureGameDate()
        if len(self.pitches) == 0:
            self.addPitch()
            transaction.commit()

    def addPitch(self): 
        self.ensureGameDate()

        newPitch = pitch.Pitch(uuid.uuid4())
        newPitch.name = 'Pitch ' + str(len(self.pitches) + 1)
        
        self.pitches.append(newPitch)
        transaction.commit()

        return newPitch

    def deleteLastPitch(self):
        self.ensureGameDate()

        if len(self.pitches) > 1:
            self.pitches.pop()
            transaction.commit()

    def pasteGameTimes(self, text):
      self.ensureGameDate()
      self.gameTimes.clear()
      lines = text.splitlines()
      for line in lines:        
        self.gameTimes.append(line)
      transaction.commit()

class DateRoute: 
    def on_delete(self, request, response, id, dateId):  
      connection = tourneyDatabase.tourneyDatabase()
      try:                                                
          (tournament, date) = GameDate.getGameDate(response, connection, id, dateId)
          if date:
              tournament.deleteDate(date)         
      finally:
          connection.close()

class GameTimePasteRoute: 
    def on_put(self, request, response, id, dateId): 
      body = json.loads(request.stream.read()) 
      connection = tourneyDatabase.tourneyDatabase()
      try:                                                
        date = GameDate.getGameDate(response, connection, id, dateId)[1]
        if date:
          date.pasteGameTimes(body['clipboardText'])                     
      finally:
        connection.close()

class PitchRoute: 
    def on_put(self, request, response, id, dateId):  
      connection = tourneyDatabase.tourneyDatabase()
      try:                                                
          date = GameDate.getGameDate(response, connection, id, dateId)[1]
          if date:
              date.addPitch()                
      finally:
          connection.close()

    def on_delete(self, request, response, id, dateId):  
      connection = tourneyDatabase.tourneyDatabase()
      try:                                                
          date = GameDate.getGameDate(response, connection, id, dateId)[1]
          if date:
             date.deleteLastPitch()                
      finally:
          connection.close()    

api.add_route('/data/tournament/{id}/date/{dateId}', DateRoute()) 
api.add_route('/data/tournament/{id}/date/{dateId}/times/paste', GameTimePasteRoute()) 
api.add_route('/data/tournament/{id}/date/{dateId}/pitch', PitchRoute()) 