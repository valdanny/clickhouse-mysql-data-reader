#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .writer import Writer
from ..event.event import Event
from ..pool.bbpool import BBPool


class PoolWriter(Writer):

    writer_builder = None
    max_pool_size = None
    pool = None

    def __init__(
            self,
            writer_builder=None,
            max_pool_size=10000,
            max_flush_interval=60
    ):
        self.writer_builder = writer_builder
        self.max_pool_size = max_pool_size
        self.max_flush_interval = max_flush_interval

        self.pool = BBPool(
            writer_builder=self.writer_builder,
            max_bucket_size=self.max_pool_size,
            max_interval_between_rotations=self.max_flush_interval,
        )

    def insert(self, event_or_events):
        self.pool.insert(event_or_events)

    def flush(self):
        self.pool.flush()

if __name__ == '__main__':
    path = 'file.csv'

    writer = CSVWriter(path)
    writer.open()
    event = Event()
    event.row_converted={
        'a': 123,
        'b': 456,
        'c': 'qwe',
        'd': 'rty',
    }
    writer.insert(event)
    event.row_converted={
        'a': 789,
        'b': 987,
        'c': 'asd',
        'd': 'fgh',
    }
    writer.insert(event)
    writer.close()
