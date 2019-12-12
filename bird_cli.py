
import socket

SOCKET_PATH = "/var/run/bird/bird.ctl"
CHUNK_SIZE = 4096


class BirdCLI(object):

    def __init__(self, socket_path=SOCKET_PATH, chunk_size=CHUNK_SIZE):
        self.socket_path = socket_path
        self.chunk_size = chunk_size
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(self.socket_path)
        self.buf = bytearray()

    def recv_atleast(self, nb_bytes):
        """Read data from the socket into the buffer until at least the given
        number of bytes is available in the buffer, or the end of stream
        is reached.  Existing data in the buffer is taken into account, so
        it's entirely possible that this function does not read anything.

        Returns the number of bytes read, which might be different than
        the resulting amount of data available in the buffer (if there was
        already some data in the buffer before calling this function).

        To check whether we have reached the end of stream, the caller
        should compare `len(self.buf)` and [nb_bytes] and test that there
        is less bytes in the buffer than what was requested.
        """
        total_read = 0
        while len(self.buf) < nb_bytes:
            data = self.sock.recv(self.chunk_size)
            total_read += len(data)
            if data == b"":
                return total_read
            self.buf += data
        return total_read

    def recv_until(self, char):
        """Read data on the socket until a specified bytestring [char] is encountered.

        Returns the position of the bytestring if found, or None if the
        end of stream was reached before encountering the bytestring.
        """
        if isinstance(char, str):
            char = char.encode()
        pos = self.buf.find(char)
        while pos == -1:
            data = self.sock.recv(self.chunk_size)
            if data == b"":
                return
            self.buf += data
            pos = self.buf.find(char)
        return pos

    def parse_reply(self):
        """Parse a complete reply from the Bird CLI.  A reply may consist of
        several messages, each with an associated code, until a final message.

        Returns a list of [code, message] tuples.  Codes and messages
        are represented as bytearrays.

        Documentation: https://bird.network.cz/?get_doc&v=16&f=prog-2.html#ss2.9
        List of codes: https://github.com/sileht/bird-lg/blob/master/bird.py
        """
        msgs = []
        final = False
        while not final:
            self.recv_atleast(5)
            if len(self.buf) < 5:
                final = True
                break
            if self.buf[0] == 32: # Space
                # Continuation line
                pos = self.recv_until(b'\n')
                line = self.buf[1:pos]
                msgs[-1][1] += b'\n' + line
            else:
                # New code
                code = bytes(self.buf[:4])
                if self.buf[4] == 32: # Space
                    final = True
                pos = self.recv_until(b'\n')
                line = self.buf[5:pos]
                msgs.append([code, line])
            del self.buf[:pos+1]
        return msgs

    def send_message(self, msg):
        if isinstance(msg, str):
            msg = msg.encode()
        if not msg.endswith(b"\n"):
            msg += b"\n"
        self.sock.send(msg)
