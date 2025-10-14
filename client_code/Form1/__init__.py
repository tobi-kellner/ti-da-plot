from ._anvil_designer import Form1Template
from anvil_extras.logging import Logger, DEBUG
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
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

    #Initially hide Step 3 card
    self.show_hide_card(self.card_step_3,self.link_step_3)
    
    #Populate color scales in Step 3 card
    self.colorscales = [
      "viridis", "plasma", "inferno", "magma", "cividis",
      "Greens", "Blues", "Reds", "coolwarm", "Spectral"
    ]
    self.flow_panel_colorscales.clear()
    for cs in self.colorscales:
      tile = Link(role="colorscale-tile")
      filename = f"_/theme/colorscales/{cs}.png"
      image = Image(source=filename, width="300px", height="30px", tooltip=cs)
      tile.add_component(image)
      tile.set_event_handler("click", lambda cs=cs, **event_args: self.select_colorscale(cs, **event_args))
      self.flow_panel_colorscales.add_component(tile)
    #Now set first one as selected
    self.flow_panel_colorscales.get_components()[0].role = "colorscale-tile-selected"
    self.selected_colorscale = cs[0]
   
  def select_colorscale(self, cs, **event_args):
    for comp in self.flow_panel_colorscales.get_components():
      comp.role = "colorscale-tile"
    event_args['sender'].role = "colorscale-tile-selected"
    self.selected_colorscale = cs
    Notification(f"Selected {cs}").show()

  def link_step_1_click(self, **event_args):
    self.show_hide_card(self.card_step_1,self.link_step_1)

  def link_step_2_click(self, **event_args):
    self.show_hide_card(self.card_step_2,self.link_step_2)

  def link_step_3_click(self, **event_args):
    self.show_hide_card(self.card_step_3,self.link_step_3)

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
      #self.plot_heatmap(result)
      self.show_hide_card(self.card_step_1,self.link_step_1)
      self.show_hide_card(self.card_step_3,self.link_step_3)
      self.show_heatmap(result)

  def plot_heatmap(self, result):
    # result contains: x (dates), y (times), z (values)

    my_cs = "blues"
    fig = go.Figure(data=go.Heatmap(
      x=result['x'],
      y=result['y'],
      z=result['z'],
      colorscale='plasma',
      tickformat='%a %d %b %y',
      autocolorscale=False
    ))

    self.plot_1.figure = fig
    user_logging.info(f"Created heatmap with {my_cs}")

  def show_heatmap(self, fig):
    self.plot_1.figure = fig


