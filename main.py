#!/usr/bin/env python3
"""news-23 b144 numbers-led: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.
Stdlib only (no PIL). Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
which the grader points at an empty output dir. Validates the PNG header, chunk
structure, CRCs and size before copying, then re-reads the output to confirm it
is byte-identical to the source.
"""
import hashlib
import os
import struct
import sys
import zlib

EXPECTED_SHA256 = "96226d3f74edf049b993d7b473754eaf36695f8745f97e8e2f6c74d1cfe53cfc"
# PNG layout: signature 8 bytes; IHDR chunk: length [8:12], type [12:16],
# data [16:29] (13 bytes), CRC [29:33]; next chunk starts at 33.
# Each chunk: length (4, big-endian) + type (4) + data (length) + CRC (4)
# where CRC covers type+data only, never the length field.
MIN_BYTES = 10000
MAX_BYTES = 1024 * 1024


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    return 1


def validate(data):
    if len(data) < MIN_BYTES:
        return "too small: %d bytes" % len(data)
    if len(data) > MAX_BYTES:
        return "too big: %d bytes" % len(data)
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return "bad PNG signature"
    # First chunk must be IHDR, 13 bytes, 1024x1024, bit depth 8,
    # colour type 2 or 6, compression/filter/interlace 0.
    clen, ctype = struct.unpack(">I4s", data[8:16])
    if ctype != b"IHDR" or clen != 13:
        return "first chunk is not a 13-byte IHDR"
    ihdr_crc = zlib.crc32(b"IHDR" + data[16:29]) & 0xFFFFFFFF
    stored_crc = struct.unpack(">I", data[29:33])[0]
    if ihdr_crc != stored_crc:
        return "bad CRC in chunk IHDR"
    w, h, depth, ctype_b, comp, filt, inter = struct.unpack(">IIBBBBB", data[16:29])
    if (w, h) != (1024, 1024):
        return "wrong dimensions: %dx%d" % (w, h)
    if depth != 8 or ctype_b not in (2, 6):
        return "unsupported IHDR: depth %d colour %d" % (depth, ctype_b)
    if comp != 0 or filt != 0 or inter != 0:
        return "unsupported IHDR flags"
    # Walk chunks: each must have a valid CRC, IDATs non-empty, IEND last.
    pos = 8
    idat_total = 0
    seen_iend = False
    while pos + 8 <= len(data):
        clen, ctype = struct.unpack(">I4s", data[pos:pos + 8])
        end = pos + 12 + clen
        if end > len(data):
            return "truncated chunk %r" % ctype
        crc = zlib.crc32(data[pos + 4:pos + 8 + clen]) & 0xFFFFFFFF
        stored = struct.unpack(">I", data[pos + 8 + clen:pos + 12 + clen])[0]
        if crc != stored:
            return "bad CRC in chunk %r" % ctype
        if ctype == b"IDAT":
            if clen == 0:
                return "empty IDAT chunk"
            idat_total += clen
        if ctype == b"IEND":
            if clen != 0:
                return "IEND must be empty"
            if end != len(data):
                return "trailing data after IEND"
            seen_iend = True
            break
        pos = end
    if not seen_iend:
        return "missing IEND"
    if idat_total < 1000:
        return "IDAT payload too small: %d bytes" % idat_total
    return None


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not outdir:
        return fail("MAKEFUN_OUTPUT_DIR is empty")
    outdir_abs = os.path.abspath(outdir)
    if os.path.commonpath([outdir_abs, here]) == here:
        return fail("MAKEFUN_OUTPUT_DIR must not be inside the repo")
    if os.path.isfile(outdir_abs):
        return fail("MAKEFUN_OUTPUT_DIR is a file")
    dst = os.path.join(outdir_abs, "entry.png")
    if os.path.abspath(dst) == os.path.abspath(src):
        return fail("output would overwrite the source")
    with open(src, "rb") as f:
        data = f.read()
    err = validate(data)
    if err:
        return fail(err)
    sha = hashlib.sha256(data).hexdigest()
    if sha != EXPECTED_SHA256:
        return fail("sha256 mismatch: got %s" % sha)
    os.makedirs(outdir_abs, exist_ok=True)
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        back = f.read()
    if back != data:
        return fail("output is not byte-identical to source")
    print("wrote %s (%d bytes, sha256 %s)" % (dst, len(data), sha))
    return 0


if __name__ == "__main__":
    sys.exit(main())
