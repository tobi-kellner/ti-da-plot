from ._anvil_designer import Form1Template
from anvil_extras.logging import Logger, DEBUG
from anvil import *
import anvil.server
import plotly.graph_objects as go

user_logging = Logger(
  name="user",
  level=DEBUG,
  format="{name}-{level} {datetime:%Y-%m-%d %H:%M:%S}: {msg}",
)

class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.


  def link_step_1_click(self, **event_args):
    self.show_hide_card(self.card_step_1,self.link_step_1)

  def show_hide_card(self, card: ColumnPanel, link: Link, **event_args):
    stat = card.visible
    card.visible = not stat
    if (stat):
      link.icon = 'fa:arrow-circle-right'
    else:
      link.icon = 'fa:arrow-circle-down'
    

  def file_loader_1_change(self, file, **event_args):
    if file:
      result = anvil.server.call('process_file', file)
      self.plot_heatmap(result)

  def text_area_1_change(self, **event_args):
    text_data = self.text_area_1.text
    if text_data.strip():
      result = anvil.server.call('process_text', text_data)
      self.plot_heatmap(result)

  def plot_heatmap(self, result):
    # result contains: x (dates), y (times), z (values)

    self.show_hide_card(self.card_step_1,self.link_step_1)
    
    fig = go.Figure(data=go.Heatmap(
      x=result['x'],
      y=result['y'],
      z=result['z'],
      colorscale='Viridis'
    ))
    self.plot_1.figure = fig

    
