#!/usr/bin/python
# -*- coding: utf-8 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import xml.sax.handler
import xml.sax
import sys
import model
import re

masterCounter = 0


class MasterHandler(xml.sax.handler.ContentHandler):
    def __init__(self, exporter, stop_after=0, ignore_missing_tags=False):
        self.knownTags = (
                            'anv',
                            'artist',
                            'artists',
                            'data_quality',
                            'description',
                            'genre',
                            'genres',
                            'id',
                            'image',
                            'images',
                            'join',
                            'main_release',
                            'master',
                            'masters',
                            'name',
                            'notes',
                            'role',
                            'style',
                            'styles',
                            'title',
                            'tracks',
                            'video',
                            'videos',
                            'year'
                            )
        self.master = None
        self.buffer = ''
        self.unknown_tags = []
        self.exporter = exporter
        self.stop_after = stop_after
        self.ignore_missing_tags = ignore_missing_tags
        self.stack = []

    def startElement(self, name, attrs):
        if not name in self.knownTags:
            if not self.ignore_missing_tags:
                print "Error: Unknown Master element '%s'." % name
                sys.exit()
            elif not name in self.unknown_tags:
                self.unknown_tags.append(name)
        self.stack.append(name)

        if name == 'master':
            self.master = model.Master()
            self.master.id = int(attrs['id'])

        elif name == 'artist':
            ma = model.ReleaseArtist()
            self.master.artists.append(ma)

    def characters(self, data):
        self.buffer += data

    def endElement(self, name):
        self.buffer = self.buffer.strip()
        if name == 'title' and self.stack[-2] == 'master':
            if len(self.buffer) != 0:
                self.master.title = self.buffer
        elif name == 'main_release':
            if len(self.buffer) != 0:
                self.master.main_release = int(self.buffer)
        elif name == 'year':
            if len(self.buffer) != 0:
                self.master.year = int(self.buffer)
        elif name == 'notes':
            if len(self.buffer) != 0:
                self.master.notes = self.buffer
        elif name == 'genre':
            if len(self.buffer) != 0:
                self.master.genres.append(self.buffer)
        elif name == 'style':
            if len(self.buffer) != 0:
                self.master.styles.append(self.buffer)
        elif name == 'data_quality':
            if len(self.buffer) != 0:
                self.master.data_quality = self.buffer

        # Release Artist
        elif name == 'anv' and self.stack[-3] == 'artists' and self.stack[-4] == 'master':
            if len(self.buffer) != 0:
                self.master.artists[-1].anv = self.buffer
        elif name == 'id' and self.stack[-3] == 'artists' and self.stack[-4] == 'master':
            if len(self.buffer) != 0:
                self.master.artists[-1].id = int(self.buffer)
        elif name == 'join' and self.stack[-3] == 'artists' and self.stack[-4] == 'master':
            if len(self.buffer) != 0:
                self.master.artists[-1].join = self.buffer
        elif name == 'name' and self.stack[-3] == 'artists' and self.stack[-4] == 'master':
            if len(self.buffer) != 0:
                self.master.artists[-1].name = self.buffer


        elif name == 'master':
            len_a = len(self.master.artists)
            if len_a == 0:
                sys.stderr.writelines("Ignoring Master %s with no artist. Dictionary: %s\n" % (self.master.id, self.master.__dict__))
            else:
                global masterCounter
                masterCounter += 1
                self.exporter.storeMaster(self.master)

                masterCounter += 1
                if self.stop_after > 0 and masterCounter >= self.stop_after:
                    self.endDocument()
                    if self.ignore_missing_tags and len(self.unknown_tags) > 0:
                        print 'Encountered some unknown Master tags: %s' % (self.unknown_tags)
                    raise model.ParserStopError(masterCounter)

        if self.stack[-1] == name:
            self.stack.pop()
        self.buffer = ''

    def endDocument(self):
        self.exporter.finish()
