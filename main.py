"""news-image-20261119: ship the bundled front page to the output dir.

Thursday 19 November 2026, drawn as a four-panel newspaper front page:
Vice City opens as GTA VI reaches players worldwide; the Gulf exchange
of fire between the US and Iran widens; Trump, Xi and Putin meet in
Shenzhen; Brussels puts a 45-billion-euro loan for Ukraine on the
table. The entry only moves bytes that are already in the repository:
it reads the bundled image, checks it, and writes the same bytes out.
No network, no clock, no randomness, so two runs produce identical
output.
"""
import hashlib
import os
import sys

SOURCE_NAME = "entry.png"
SIGNATURE = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])
LIMIT = 1 << 20


def fail(message):
    print("error: " + message, file=sys.stderr)
    raise SystemExit(1)


def payload():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, SOURCE_NAME)
    with open(path, "rb") as handle:
        blob = handle.read()
    if blob[:8] != SIGNATURE:
        fail("bundled entry.png is not a PNG")
    if len(blob) > LIMIT:
        fail("bundled entry.png exceeds 1 MiB")
    return blob


def deliver(blob):
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, SOURCE_NAME)
    with open(target, "wb") as handle:
        handle.write(blob)
    with open(target, "rb") as handle:
        again = handle.read()
    if hashlib.sha256(again).hexdigest() != hashlib.sha256(blob).hexdigest():
        fail("output bytes differ from the bundled image")
    return target


def run():
    blob = payload()
    target = deliver(blob)
    print("wrote " + target + " (" + str(len(blob)) + " bytes)")


if __name__ == "__main__":
    run()
