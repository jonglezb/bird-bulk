

CHUNK_SIZE = 4096


def recv_atleast(sock, buf, nb_bytes):
    """Read data from the socket into the buffer until at least the given
    number of bytes is available in the buffer, or the end of stream is
    reached.  Existing data in the buffer is taken into account, so it's
    entirely possible that this function does not read anything.

    Returns the number of bytes read, which might be different than the
    resulting amount of data available in the buffer (if there was already
    some data in the buffer before calling this function).
    """
    total_read = 0
    while len(buf) < nb_bytes:
        data = sock.recv(CHUNK_SIZE)
        total_read += len(data)
        if data == b"":
            return total_read
        buf += data
    return total_read

def recv_until(sock, buf, char):
    """Read data on the socket until a specified bytestring is encountered.

    Returns the position of the bytestring if found, or None if the end of
    stream was reached before encountering the bytestring.
    """
    pos = buf.find(char)
    while pos == -1:
        data = sock.recv(CHUNK_SIZE)
        if data == b"":
            return
        buf += data
        pos = buf.find(char)
    return pos

def parse_reply(sock):
    """Parse a complete reply from Bird output on the Unix socket.  A reply
    may consist of several messages, each with a code.

    Returns a list of [code, message] tuples.  Codes and messages are
    represented as bytearrays.

    Documentation: https://bird.network.cz/?get_doc&v=16&f=prog-2.html#ss2.9
    List of codes: https://github.com/sileht/bird-lg/blob/master/bird.py
    """
    msgs = []
    end = False
    buf = bytearray()
    while not end:
        recv_atleast(sock, buf, 5)
        if len(buf) < 5:
            end = True
            break
        if bytes(buf[0:1]) == b' ':
            # Continuation line
            pos = recv_until(sock, buf, b'\n')
            line = buf[1:pos]
            msgs[-1][1] += b'\n' + line
        else:
            # New code
            code = bytes(buf[:4])
            if bytes(buf[4:5]) == b' ':
                end = True
            pos = recv_until(sock, buf, b'\n')
            line = buf[5:pos]
            msgs.append([code, line])
        del buf[:pos+1]
    return msgs

def send_message(sock, msg):
    if isinstance(msg, str):
        msg = msg.encode()
    if not msg.endswith(b"\n"):
        msg += b"\n"
    sock.send(msg)
