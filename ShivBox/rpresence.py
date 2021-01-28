import asyncio
import json
import os
import struct
import sys
import time

class RichPresence:
    def __init__(self):
        if sys.platform == 'linux':
            self.ipc_path = (os.environ.get('XDG_RUNTIME_DIR', None) or os.environ.get('TMPDIR', None) or
                             os.environ.get('TMP', None) or os.environ.get('TEMP', None) or '/tmp') + '/discord-ipc-0'
            self.loop = asyncio.get_event_loop()
        elif sys.platform == 'win32':
            self.ipc_path = r'\\?\pipe\discord-ipc-0'
            self.loop = asyncio.ProactorEventLoop()
        self.sock_reader: asyncio.StreamReader = None
        self.sock_writer: asyncio.StreamWriter = None

    async def read_output(self):
        print("reading output")
        data = await self.sock_reader.read(1024)
        code, length = struct.unpack('<ii', data[:8])
        print('OP Code: {}; Length: {}\nResponse:\n{}\n'.format(
            code, length, json.loads(data[8:].decode('utf-8'))))

    def send_data(self, op: int, payload: dict):
        payload = json.dumps(payload)
        data = self.sock_writer.write(struct.pack('<ii', op, len(payload)) + payload.encode('utf-8'))
        yield from self.sock_writer.drain()
        print(data)

    async def make_pc(self, clientid):
        if sys.platform == 'linux':
            self.sock_reader, self.sock_writer = await asyncio.open_unix_connection(self.ipc_path, loop=self.loop)
        elif sys.platform == 'win32':
            self.sock_reader = asyncio.StreamReader(loop=self.loop)
            reader_protocol = asyncio.StreamReaderProtocol(self.sock_reader, loop=self.loop)
            self.sock_writer, _ = await self.loop.create_pipe_connection(lambda: reader_protocol, self.ipc_path)
        self.send_data(0, {'v': 1, 'client_id': clientid})
        data = await self.sock_reader.read(1024)
        code, length = struct.unpack('<ii', data[:8])
        print('OP Code: {}; Length: {}\nResponse:\n{}\n'.format(
            code, length, json.loads(data[8:].decode('utf-8'))))
