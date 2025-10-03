# handles storing and retreiving data
from anvil_extras.logging import Logger, DEBUG
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime as dt
import pickle
import lzma
import pandas as pd

if (anvil.server.session.session_id == None):
  id = 0
else:
  id = hashlib.sha1(anvil.server.session.session_id.encode('utf-8')).hexdigest()

user_logging = Logger(
  name="user",
  level=DEBUG,
  format="{name}-{level} {datetime:%Y-%m-%d %H:%M:%S}: {msg}",
)

MAX_BLOB_SIZE = 10_000_000

def save_datatable(data):
  sesh_id = id
  row = app_tables.user_data.get(session_id=sesh_id)
  if (row is None):
    row = app_tables.user_data.add_row(session_id=sesh_id,
                                       dt_created = dt.now(),
                                       access_counter=0)
  else:
    row['access_counter'] += 1
  row['dt_changed'] = dt.now()
  pick = pickle.dumps(data)
  le = len(pick)
  pick = lzma.compress(pick)
  row['raw_data'] = anvil.BlobMedia("bytes", pick, "anvil.pickle")
  le2 = len(pick)
  if (le2 > MAX_BLOB_SIZE):
    # this pickle is suspiciously large
    user_logging.critical(f"ServerData.save_data: attempt to storecompressed pickle of size {le2} for session {sesh_id}")
    raise(Exception(f"SUSPICIOUS ACTIVITY: ServerData.save_data attempted to store pickle of size {le} for session {sesh_id}"))
    return
  user_logging.info(f"Saved {le2:,} bytes, previously {le:,} bytes")

def load_data(sesh_id)