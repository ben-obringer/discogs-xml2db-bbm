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

releaseCounter = 0


class ReleaseHandler(xml.sax.handler.ContentHandler):
    def __init__(self, exporter, stop_after=0, ignore_missing_tags=False):
        self.knownTags = (
                            'anv',
                            'artist',
                            'artists',
                            'catno',
                            'companies',
                            'company',
                            'country',
                            'data_quality',
                            'description',
                            'descriptions',
                            'duration',
                            'entity_type',
                            'entity_type_name',
                            'extraartists',
                            'format',
                            'formats',
                            'genre',
                            'genres',
                            'id',
                            'identifier',
                            'identifiers',
                            'image',
                            'images',
                            'join',
                            'label',
                            'labels',
                            'master_id',
                            'name',
                            'notes',
                            'position',
                            'release',
                            'releases',
                            'released',
                            'resource_url',
                            'role',
                            'style',
                            'styles',
                            'sub_tracks',
                            'title',
                            'track',
                            'tracklist',
                            'tracks',
                            'url',
                            'urls',
                            'video',
                            'videos'
                            )
        self.release = None
        self.buffer = ''
        self.unknown_tags = []
        self.exporter = exporter
        self.stop_after = stop_after
        self.ignore_missing_tags = ignore_missing_tags
        self.stack = []

    def startElement(self, name, attrs):
        if not name in self.knownTags:
            if not self.ignore_missing_tags:
                print "Error: Unknown Release element '%s'." % name
                sys.exit()
            elif not name in self.unknown_tags:
                self.unknown_tags.append(name)
        self.stack.append(name)

        if name == 'release':
            self.release = model.Release()
            self.release.id = int(attrs['id'])

        elif name == 'track' and self.stack[-2] == 'tracklist':
            self.release.tracklist.append(model.Track())

        elif name == 'format':
            fmt = model.Format()
            fmt.name = attrs['name']
            self.release.formats.append(fmt)

        elif name == 'label':
            lbl = model.ReleaseLabel()
            lbl.name = attrs['name']
            lbl.catno = attrs['catno']
            self.release.labels.append(lbl)

        elif name == 'company':
            cmp = model.ReleaseCompany()
            self.release.companies.append(cmp)

        elif name == 'artist' and 'track' not in self.stack and 'extraartists' not in self.stack:
            aj = model.ReleaseArtist()
            self.release.artists.append(aj)

        elif name == 'artist' and 'track' in self.stack and 'sub_track' not in self.stack and 'extraartists' not in self.stack:
            taj = model.ReleaseArtist()
            self.release.tracklist[-1].artists.append(taj)

        elif name == 'artist' and 'track' not in self.stack and 'extraartists' in self.stack:
            eaj = model.ExtraArtist()
            self.release.extraartists.append(eaj)

        elif name == 'artist' and 'track' in self.stack and 'sub_track' not in self.stack and 'extraartists' in self.stack:
            teaj = model.ExtraArtist()
            self.release.tracklist[-1].extraartists.append(teaj)



    def characters(self, data):
        self.buffer += data

    def endElement(self, name):
        self.buffer = self.buffer.strip()

        # Release Country
        if name == 'country':
            if len(self.buffer) != 0:
                self.release.country = self.buffer

        # Release DataQuality
        elif name == 'data_quality':
            if len(self.buffer) != 0:
                self.release.data_quality = self.buffer

        # Release Date
        elif name == 'released':
            if len(self.buffer) != 0:
                self.release.released = self.buffer

        # Release Format Description
        elif name == 'description' and 'formats' in self.stack:
            if len(self.buffer) != 0:
                self.release.formats[-1].descriptions.append(self.buffer)

        # Release Notes
        elif name == 'notes':
            if len(self.buffer) != 0:
                self.release.notes = self.buffer

        # Release Genre
        elif name == 'genre':
            if len(self.buffer) != 0:
                self.release.genres.append(self.buffer)

        # Release Master
        elif name == 'master_id':
            self.release.master_id = int(self.buffer)

        # Release Style
        elif name == 'style':
            if len(self.buffer) != 0:
                self.release.styles.append(self.buffer)

        # Release Title
        elif name == 'title' and self.stack[-2] == 'release':
            if len(self.buffer) != 0:
                self.release.title = self.buffer


        # Track Duration
        elif name == 'duration' and 'sub_track' not in self.stack:
            self.release.tracklist[-1].duration = self.buffer

        # Track Position
        elif name == 'position' and 'sub_track' not in self.stack:
            self.release.tracklist[-1].position = self.buffer

        # Track Title
        elif name == 'title' and self.stack[-2] == 'track' and 'sub_track' not in self.stack:
            if len(self.buffer) != 0:
                self.release.tracklist[-1].title = self.buffer


        # Release Artist Anv
        elif name == 'anv' and 'artist' in self.stack and 'track' not in self.stack and 'extraartists' not in self.stack:
            if len(self.buffer) != 0:
                self.release.artists[-1].anv = self.buffer

        # Release Artist Id
        elif name == 'id' and 'artist' in self.stack and 'track' not in self.stack and 'extraartists' not in self.stack:
            if len(self.buffer) != 0:
                self.release.artists[-1].id = int(self.buffer)

        # Release Artist Join
        elif name == 'join' and 'artist' in self.stack and 'track' not in self.stack and 'extraartists' not in self.stack:
            if len(self.buffer) != 0:
                self.release.artists[-1].join = self.buffer

        # Release Artist Name
        elif name == 'name' and 'artist' in self.stack and 'track' not in self.stack and 'extraartists' not in self.stack:
            if len(self.buffer) != 0:
                self.release.artists[-1].name = self.buffer

        # Release Artist Role
        elif name == 'role' and 'artist' in self.stack and 'track' not in self.stack and 'extraartists' not in self.stack:
            if len(self.buffer) != 0:
                self.release.artists[-1].role = self.buffer


        # Track Artist Anv
        elif name == 'anv' and 'artist' in self.stack and 'track' in self.stack and 'sub_track' not in self.stack and 'extraartists' not in self.stack:
            if len(self.buffer) != 0:
                self.release.tracklist[-1].artists[-1].anv = self.buffer

        # Track Artist Id
        elif name == 'id' and 'artist' in self.stack and 'track' in self.stack and 'sub_track' not in self.stack and 'extraartists' not in self.stack:
            if len(self.buffer) != 0:
                self.release.tracklist[-1].artists[-1].id = int(self.buffer)

        # Track Artist Join
        elif name == 'join' and 'artist' in self.stack and 'track' in self.stack and 'sub_track' not in self.stack and 'extraartists' not in self.stack:
            if len(self.buffer) != 0:
                self.release.tracklist[-1].artists[-1].join = self.buffer

        # Track Artist Name
        elif name == 'name' and 'artist' in self.stack and 'track' in self.stack and 'sub_track' not in self.stack and 'extraartists' not in self.stack:
            if len(self.buffer) != 0:
                self.release.tracklist[-1].artists[-1].name = self.buffer

        # Track Artist Role
        elif name == 'role' and 'artist' in self.stack and 'track' in self.stack and 'sub_track' not in self.stack and 'extraartists' not in self.stack:
            if len(self.buffer) != 0:
                self.release.tracklist[-1].artists[-1].name = self.buffer


        # Release ExtraArtist Anv
        elif name == 'anv' and 'artist' in self.stack and 'track' not in self.stack and 'extraartists' in self.stack:
            if len(self.buffer) != 0:
                self.release.extraartists[-1].anv = self.buffer

        # Release ExtraArtist Id
        elif name == 'id' and 'artist' in self.stack and 'track' not in self.stack and 'extraartists' in self.stack:
            if len(self.buffer) != 0:
                self.release.extraartists[-1].id = int(self.buffer)

        # Release ExtraArtist Join
        elif name == 'join' and 'artist' in self.stack and 'track' not in self.stack and 'extraartists' in self.stack:
            if len(self.buffer) != 0:
                self.release.extraartists[-1].role = self.buffer

        # Release ExtraArtist Name
        elif name == 'name' and 'artist' in self.stack and 'track' not in self.stack and 'extraartists' in self.stack:
            if len(self.buffer) != 0:
                self.release.extraartists[-1].name = self.buffer

        # Release ExtraArtist Role
        elif name == 'role' and 'artist' in self.stack and 'track' not in self.stack and 'extraartists' in self.stack:
            if len(self.buffer) != 0:
                self.release.extraartists[-1].role = self.buffer

        # Release ExtraArtist Tracks
        elif name == 'tracks' and 'artist' in self.stack and 'track' not in self.stack and 'extraartists' in self.stack:
            if len(self.buffer) != 0:
                self.release.extraartists[-1].tracks = self.buffer


        # Track ExtraArtist Anv
        elif name == 'anv' and 'artist' in self.stack and 'track' in self.stack and 'sub_track' not in self.stack and 'extraartists' in self.stack:
            if len(self.buffer) != 0:
                self.release.tracklist[-1].extraartists[-1].anv = self.buffer

        # Track ExtraArtist Id
        elif name == 'id' and 'artist' in self.stack and 'track' in self.stack and 'sub_track' not in self.stack and 'extraartists' in self.stack:
            if len(self.buffer) != 0:
                self.release.tracklist[-1].extraartists[-1].id = int(self.buffer)

        # Track ExtraArtist Join
        elif name == 'join' and 'artist' in self.stack and 'track' in self.stack and 'sub_track' not in self.stack and 'extraartists' in self.stack:
            if len(self.buffer) != 0:
                self.release.tracklist[-1].extraartists[-1].join = self.buffer

        # Track ExtraArtist Name
        elif name == 'name' and 'artist' in self.stack and 'track' in self.stack and 'sub_track' not in self.stack and 'extraartists' in self.stack:
            if len(self.buffer) != 0:
                self.release.tracklist[-1].extraartists[-1].name = self.buffer

        # Track ExtraArtist Role
        elif name == 'role' and 'artist' in self.stack and 'track' in self.stack and 'sub_track' not in self.stack and 'extraartists' in self.stack:
            if len(self.buffer) != 0:
                self.release.tracklist[-1].extraartists[-1].role = self.buffer


        # Company Catno
        elif name == 'catno' and 'company' in self.stack:
            if len(self.buffer) != 0:
                self.release.companies[-1].catno = self.buffer

        # Company Entity_type
        elif name == 'entity_type' and 'company' in self.stack:
            if len(self.buffer) != 0:
                self.release.companies[-1].entity_type = self.buffer

        # Company Id
        elif name == 'id' and 'company' in self.stack:
            if len(self.buffer) != 0:
                self.release.companies[-1].id = int(self.buffer)

        # Company Name
        elif name == 'name' and 'company' in self.stack:
            if len(self.buffer) != 0:
                self.release.companies[-1].name = self.buffer


        # End of Release
        elif name == 'release':
            len_a = len(self.release.artists)
            if len_a == 0:
                sys.stderr.writelines("Ignoring Release %s with no artist. Dictionary: %s\n" % (self.release.id, self.release.__dict__))
            else:
                global releaseCounter
                releaseCounter += 1
                self.exporter.storeRelease(self.release)

                releaseCounter += 1
                if self.stop_after > 0 and releaseCounter >= self.stop_after:
                    self.endDocument()
                    if self.ignore_missing_tags and len(self.unknown_tags) > 0:
                        print 'Encountered some unknown Release tags: %s' % (self.unknown_tags)
                    raise model.ParserStopError(releaseCounter)

        if self.stack[-1] == name:
            self.stack.pop()
        self.buffer = ''

    def endDocument(self):
        self.exporter.finish()
