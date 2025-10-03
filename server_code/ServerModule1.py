import anvil.server
import pandas as pd
import io
import plotly.graph_objects as go

@anvil.server.callable
def process_file(file):
  # Read CSV into pandas
  df = pd.read_csv(io.BytesIO(file.get_bytes()))
  return _process_dataframe(df)

@anvil.server.callable
def process_text(text_data):
  # Assume tab or comma separated
  df = pd.read_csv(io.StringIO(text_data), sep=None, engine="python")
  return _process_dataframe(df)

def _process_dataframe(df):
  # Expect two columns: datetime, value
  df.columns = ['datetime', 'value']
  df['datetime'] = pd.to_datetime(df['datetime'])

  # Extract date and time-of-day
  df['date'] = df['datetime'].dt.date
  df['time'] = df['datetime'].dt.strftime('%H:%M')

  # Pivot into matrix for heatmap
  pivot = df.pivot_table(index='time', columns='date', values='value', aggfunc='mean')
  
  # fig = go.Figure(data=go.Heatmap(
  #   x=pivot.columns.astype(str).tolist(),
  #   y=pivot.index.astype(str).tolist(),
  #   z=pivot.values.astype(float).tolist(),
  #   colorscale='magma',
  #   autocolorscale=False
  # ))  
  # return fig
  
  return {
    'x': list(pivot.columns.astype(str)),   # dates
    'y': list(pivot.index),                 # times
    'z': pivot.values.astype(float).tolist()              # matrix of values
  }



