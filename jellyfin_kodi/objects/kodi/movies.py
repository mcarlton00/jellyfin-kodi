# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, print_function, unicode_literals

##################################################################################################

from helper import LazyLogger

from .kodi import Kodi
from . import queries as QU

##################################################################################################

LOG = LazyLogger(__name__)

##################################################################################################


class Movies(Kodi):

    def __init__(self, cursor):

        self.cursor = cursor
        Kodi.__init__(self)

    def create_entry_unique_id(self):
        self.cursor.execute(QU.create_unique_id)

        return self.cursor.fetchone()[0] + 1

    def create_entry_rating(self):
        self.cursor.execute(QU.create_rating)

        return self.cursor.fetchone()[0] + 1

    def create_entry(self):
        self.cursor.execute(QU.create_movie)

        return self.cursor.fetchone()[0] + 1

    def get(self, *args):

        try:
            self.cursor.execute(QU.get_movie, args)
            return self.cursor.fetchone()[0]
        except TypeError:
            return

    def add(self, *args):
        self.cursor.execute(QU.add_movie, args)

    def update(self, *args):
        self.cursor.execute(QU.get_movie, (args[-1],))
        old = self.cursor.fetchone()
        self.cursor.execute(QU.update_movie, args)
        self.cursor.execute(QU.get_movie, (args[-1],))
        new = self.cursor.fetchone()
        changed = False
        for index, value in enumerate(old):
            if value != new[index]:
                LOG.info('Movie {} has had column {} updated'.format(old[2], index))
                LOG.info('Old value: {}'.format(value))
                LOG.info('New value: {}'.format(new[index]))
                changed = True
        if not changed:
            LOG.info('Movie {} was updated, but had no changes'.format(old[2]))

    def delete(self, kodi_id, file_id):

        self.cursor.execute(QU.delete_movie, (kodi_id,))
        self.cursor.execute(QU.delete_file, (file_id,))

    def get_rating_id(self, *args):

        try:
            self.cursor.execute(QU.get_rating, args)

            return self.cursor.fetchone()[0]
        except TypeError:
            return None

    def add_ratings(self, *args):

        ''' Add ratings, rating type and votes.
        '''
        self.cursor.execute(QU.add_rating, args)

    def update_ratings(self, *args):

        ''' Update rating by rating_id.
        '''
        self.cursor.execute(QU.update_rating, args)

    def get_unique_id(self, *args):

        try:
            self.cursor.execute(QU.get_unique_id, args)

            return self.cursor.fetchone()[0]
        except TypeError:
            return

    def add_unique_id(self, *args):

        ''' Add the provider id, imdb, tvdb.
        '''
        self.cursor.execute(QU.add_unique_id, args)

    def update_unique_id(self, *args):

        ''' Update the provider id, imdb, tvdb.
        '''
        self.cursor.execute(QU.update_unique_id, args)

    def add_countries(self, countries, *args):

        for country in countries:
            self.cursor.execute(QU.update_country, (self.get_country(country),) + args)

    def add_country(self, *args):
        self.cursor.execute(QU.add_country, args)
        return self.cursor.lastrowid

    def get_country(self, *args):

        try:
            self.cursor.execute(QU.get_country, args)

            return self.cursor.fetchone()[0]
        except TypeError:
            return self.add_country(*args)

    def add_boxset(self, *args):
        self.cursor.execute(QU.add_set, args)
        return self.cursor.lastrowid

    def update_boxset(self, *args):
        self.cursor.execute(QU.update_set, args)

    def set_boxset(self, *args):
        self.cursor.execute(QU.update_movie_set, args)

    def remove_from_boxset(self, *args):
        self.cursor.execute(QU.delete_movie_set, args)

    def delete_boxset(self, *args):
        self.cursor.execute(QU.delete_set, args)
