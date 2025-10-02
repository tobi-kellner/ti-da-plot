from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import plotly.graph_objects as go


class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

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
    fig = go.Figure(data=go.Heatmap(
      x=result['x'],
      y=result['y'],
      z=result['z'],
      colorscale='Viridis'
    ))
    self.plot_1.figure = fig

  def link_step_1_click(self, **event_args):
    stat = self.card_step_1.visible
    self.card_step_1.visible = not stat
    if (stat):
      self.link_step_1.icon = 'fa:arrow-circle-right'
    else:
      self.link_step_1.icon = 'fa:arrow-circle-down'
    
