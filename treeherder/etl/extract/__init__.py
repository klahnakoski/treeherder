import sys

VENDOR_PATH = "treeherder.etl.extract.vendor"

if VENDOR_PATH not in sys.path:
    sys.path.append(VENDOR_PATH)