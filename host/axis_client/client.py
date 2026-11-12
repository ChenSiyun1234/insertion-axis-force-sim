"""Nonblocking client for transports exposing write(bytes) and read()."""

import struct

from .identifiers import Command
from .protocol import Reader, decode_status, encode


class Client:

    def __init__(self, transport):
        self.transport = transport
        self.seq = 0
        self.reader = Reader()

    def request(self, cmd, payload=b""):
        """Frame a request and return its sequence number without waiting for an ACK."""
        self.seq = self.seq + 1 & 255
        self.transport.write(encode(self.seq, cmd, payload))
        return self.seq

    def frames(self):
        yield from self.reader.feed(self.transport.read())

    def ping(self):
        return self.request(Command.PING)

    def enable(self):
        return self.request(Command.ENABLE)

    def disable(self):
        return self.request(Command.DISABLE)

    def start_insert(self, target_mm=296):
        return self.request(Command.START_INSERT, struct.pack("<f", target_mm))

    def home(self):
        return self.request(Command.HOME)

    def stop(self):
        return self.request(Command.STOP)

    def retract(self, distance_mm):
        return self.request(Command.RETRACT, struct.pack("<f", distance_mm))

    def tare(self):
        return self.request(Command.TARE)

    def clear_fault(self):
        return self.request(Command.CLEAR_FAULT)

    def status(self):
        return self.request(Command.GET_STATUS)

    def set_param(self, parameter_id, value):
        return self.request(Command.SET_PARAM, struct.pack("<Bf", parameter_id, value))

    def get_param(self, parameter_id):
        return self.request(Command.GET_PARAM, bytes((parameter_id,)))

    def stream(self, period_ms):
        return self.request(Command.STREAM, struct.pack("<H", period_ms))

    @staticmethod
    def status_fields(frame):
        return decode_status(frame.payload)
