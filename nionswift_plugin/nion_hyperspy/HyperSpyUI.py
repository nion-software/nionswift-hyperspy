# system imports
import gettext

# third part imports
# None

# local libraries
from nion.swift.model import DataItem
from nion.swift.model import DocumentModel
from nion.typeshed import API_1_0 as API

_ = gettext.gettext


processing_descriptions = {
    "nion.hyperspy.background":
        { 'script': '''# remove background with HyperSpy

import hyperspy.api as hyperspy
import nion.hyperspy

signal = nion.hyperspy.xdata_to_signal(src.display_xdata)
fit_px = int(fit_region.interval[0] * src.display_xdata.data_shape[0]), int(fit_region.interval[1] * src.display_xdata.data_shape[0])
signal_px = int(signal_region.interval[0] * src.display_xdata.data_shape[0]), int(signal_region.interval[1] * src.display_xdata.data_shape[0])
signal = signal.remove_background(signal_range=fit_px)
target.xdata = nion.hyperspy.signal_to_xdata(signal)[signal_px]
''',
          'sources': [{'label': 'Source', 'name': 'src', 'regions': [
              {'name': 'fit_region', 'params': {'label': 'Fit', 'interval': (0.2, 0.3)}, 'type': 'interval'},
              {'name': 'signal_region', 'params': {'label': 'Signal', 'interval': (0.4, 0.5)}, 'type': 'interval'},
          ]}],
          'title': 'Background Removed (HS)',
        }
}

#
# WARNING: NION SWIFT VERSION DEPENDENT CODE. DO NOT USE AS AN EXAMPLE.
#
# The code below is Nion Swift version dependent.  If you are using this as a
# coding example, use with extreme caution. This code is maintained by the
# Nion Swift development team and new versions of Nion Swift will almost
# assuredly be incompatible with this code. The Nion Swift team will update
# this code to work with new versions; however we will not update _your code_
# based on this code. Please use the standard Nion Swift API instead.
#
DocumentModel.DocumentModel.register_processing_descriptions(processing_descriptions)


class RemoveBackgroundMenuItem:

    menu_id = "hyperspy_menu"  # required, specify menu_id where this item will go
    menu_name = _("HyperSpy")  # optional, specify default name if not a standard menu
    menu_before_id = "window_menu"  # optional, specify before menu_id if not a standard menu
    menu_item_name = _("Remove Background")  # menu item name

    def menu_item_execute(self, document_window: API.DocumentWindow) -> None:
        #
        # WARNING: NION SWIFT VERSION DEPENDENT CODE. DO NOT USE AS AN EXAMPLE.
        #
        # The code below is Nion Swift version dependent.  If you are using this as a
        # coding example, use with extreme caution. This code is maintained by the
        # Nion Swift development team and new versions of Nion Swift will almost
        # assuredly be incompatible with this code. The Nion Swift team will update
        # this code to work with new versions; however we will not update _your code_
        # based on this code. Please use the standard Nion Swift API instead.
        #
        _document_window = document_window._document_window
        display_specifier = _document_window.selected_display_specifier
        data_item = _document_window.document_model.make_data_item_with_computation("nion.hyperspy.background", [(display_specifier.data_item, None)], {"src": [None, None]})
        if data_item:
            new_display_specifier = DataItem.DisplaySpecifier.from_data_item(data_item)
            _document_window.display_data_item(new_display_specifier)
            return data_item
        return None


class HyperSpyExtension:

    # required for Swift to recognize this as an extension class.
    extension_id = "nionswift.hyperspy"

    def __init__(self, api_broker):
        # grab the api object.
        api = api_broker.get_api(version="1", ui_version="1")
        # be sure to keep a reference or it will be closed immediately.
        self.__menu_item_ref = api.create_menu_item(RemoveBackgroundMenuItem())

    def close(self):
        # close will be called when the extension is unloaded. in turn, close any references so they get closed. this
        # is not strictly necessary since the references will be deleted naturally when this object is deleted.
        self.__menu_item_ref.close()
