from ._anvil_designer import ItemTemplateColorscaleTemplate
from anvil import *
import anvil.server


class ItemTemplateColorscale(ItemTemplateColorscaleTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def link_colorscale_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.parent.raise_event("x-item-click", item=self.item)
