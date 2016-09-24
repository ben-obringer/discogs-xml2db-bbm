class Artist:
   def __init__(self):
      self.aliases = []
      self.data_quality = ''
      self.groups = []
      self.id = 0
      self.members = []
      self.name = ''
      self.namevariations = []
      self.profile = ''
      self.realname = ''
      self.urls = []

class Label:
  def __init__(self):
    self.contactinfo = ''
    self.data_quality = ''
    self.id = 0
    self.name = ''
    self.parentLabel = ''
    self.profile = ''
    self.sublabels = []
    self.urls = []

class Master:
   def __init__(self):
     self.artists = [] #class ReleaseArtist
     self.genres = []
     self.id = 0
     self.main_release = 0
     self.notes = ''
     self.styles = []
     self.title = ''
     self.year = 0

class Release:
   def __init__(self):
     self.artists = [] #class ReleaseArtist
     self.companies = [] #class ReleaseCompany
     self.country = ''
     self.data_quality = ''
     self.extraartists = [] #class ExtraArtist
     self.formats = [] #class Format
     self.genres = []
     self.id = 0
     self.labels = [] #class ReleaseLabel
     self.master_id = 0
     self.notes = ''
     self.released = ''
     self.styles = []
     self.title = ''
     self.tracklist = [] #class Track, ExtraArtist, ReleaseArtist


class ExtraArtist:
  def __init__(self):
    self.anv = ''
    self.id = ''
    self.join = ''
    self.name = ''
    self.role = ''
    self.tracks = ''

class Format:
  def __init__(self):
    self.descriptions = []
    self.name = ''

class ReleaseArtist:
  def __init__(self):
    self.anv = ''
    self.id = ''
    self.join = ''
    self.name = ''
    self.role = ''

class ReleaseCompany:
  def __init__(self):
    self.catno = ''
    self.entity_type = ''
    self.id = ''
    self.name = ''

class ReleaseLabel:
  def __init__(self):
    self.catno = ''
    self.name = ''

class Track:
  def __init__(self):
    self.artists = [] #class ReleaseArtist
    self.duration = ''
    self.extraartists = [] #class ExtraArtist
    self.position = ''
    self.title = ''



class ParserStopError(Exception):
    """Raised by a parser to signal that it wants to stop parsing."""
    def __init__(self, count):
        self.records_parsed = count
