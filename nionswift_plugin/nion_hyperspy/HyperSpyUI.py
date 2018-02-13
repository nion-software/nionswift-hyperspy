# system imports
import gettext

# third part imports
import nion.hyperspy

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
calibration = src.display_xdata.dimensional_calibrations[0]
fit_range = calibration.convert_to_calibrated_value(int(fit_region.interval[0] * src.display_xdata.data_shape[0])), calibration.convert_to_calibrated_value(int(fit_region.interval[1] * src.display_xdata.data_shape[0]))
signal_px = int(signal_region.interval[0] * src.display_xdata.data_shape[0]), int(signal_region.interval[1] * src.display_xdata.data_shape[0])
signal = signal.remove_background(signal_range=fit_range)
target.xdata = nion.hyperspy.signal_to_xdata(signal)[signal_px[0]:signal_px[1]]
''',
          'sources': [{'label': 'Source', 'name': 'src',
                       'requirements': [{"type": "dimensionality", "min": 1, "max": 1}],
                       'regions': [
                           {'name': 'fit_region', 'params': {'label': 'Fit', 'interval': (0.2, 0.3)},
                            'type': 'interval'},
                           {'name': 'signal_region', 'params': {'label': 'Signal', 'interval': (0.4, 0.5)},
                            'type': 'interval'},
                       ]}],
          'title': 'Background Removed (HS)',
        },
    "nion.hyperspy.map":
        { 'script': '''# map background subtracted signal with HyperSpy

import hyperspy.api as hyperspy
import nion.hyperspy

calibration = src.display_xdata.dimensional_calibrations[0]
fit_range = calibration.convert_to_calibrated_value(int(fit_region.interval[0] * src.display_xdata.data_shape[0])), calibration.convert_to_calibrated_value(int(fit_region.interval[1] * src.display_xdata.data_shape[0]))
signal_px = int(signal_region.interval[0] * src_fit.display_xdata.data_shape[0]), int(signal_region.interval[1] * src_fit.display_xdata.data_shape[0])
signal = nion.hyperspy.xdata_to_signal(src.xdata)
signal = signal.remove_background(signal_range=fit_range).isig[signal_px[0]:signal_px[1]].integrate1D(2)
target.xdata = nion.hyperspy.signal_to_xdata(signal)
''',
          'sources': [{'label': 'Fitting Source', 'name': 'src_fit',
                       'requirements': [{"type": "dimensionality", "min": 1, "max": 1}],
                       'regions': [
                           {'name': 'fit_region', 'params': {'label': 'Fit', 'interval': (0.2, 0.3)},
                            'type': 'interval'},
                           {'name': 'signal_region', 'params': {'label': 'Signal', 'interval': (0.4, 0.5)},
                            'type': 'interval'},
                       ]},
                      {'label': 'Source', 'name': 'src',
                       'requirements': [{"type": "dimensionality", "min": 3, "max": 3}]
                       }],
          'title': 'Mapped (HS)',
          },
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


class HyperSpyMenuItemBase:

    menu_id = "hyperspy_menu"  # required, specify menu_id where this item will go
    menu_name = _("HyperSpy")  # optional, specify default name if not a standard menu
    menu_before_id = "window_menu"  # optional, specify before menu_id if not a standard menu


class RemoveBackgroundMenuItem(HyperSpyMenuItemBase):

    menu_item_name = _("Remove Background")  # menu item name

    def menu_item_execute(self, window: API.DocumentWindow) -> None:
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
        _document_window = window._document_window
        display_specifier = _document_window.selected_display_specifier
        _data_item = _document_window.document_model.make_data_item_with_computation("nion.hyperspy.background", [(display_specifier.data_item, None)], {"src": [None, None]})
        if _data_item:
            new_display_specifier = DataItem.DisplaySpecifier.from_data_item(_data_item)
            _document_window.display_data_item(new_display_specifier)


class AlignZLPMenuItem(HyperSpyMenuItemBase):

    menu_item_name = _("Align Zero Loss Peak")  # menu item name

    def menu_item_execute(self, window: API.DocumentWindow) -> None:
        data_item = window.target_data_item
        if data_item:
            xdata = data_item.xdata
            if xdata.datum_dimension_count == 1:
                signal = nion.hyperspy.xdata_to_signal(xdata, copy_data=True)
                signal.set_signal_type('EELS')
                signal.align_zero_loss_peak(print_stats=False)
                xdata = nion.hyperspy.signal_to_xdata(signal)
                data_item = window.library.create_data_item_from_data_and_metadata(xdata)
                window.display_data_item(data_item)


class MapSignalMenuItem(HyperSpyMenuItemBase):

    menu_item_name = _("Map Signal")  # menu item name

    def menu_item_execute(self, window: API.DocumentWindow) -> None:
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
        data_item = window.target_data_item
        if data_item and data_item.xdata.is_data_1d and len(data_item.display.graphics) == 3:
            src_data_items = window.library.get_source_data_items(data_item)
            if len(src_data_items) == 1 and src_data_items[0].xdata.is_data_3d:
                src_data_item = src_data_items[0]
                _document_window = window._document_window
                _data_item = _document_window.document_model.make_data_item_with_computation("nion.hyperspy.map", [(data_item._data_item, None), (src_data_item._data_item, None)], {"src_fit": [data_item.display.graphics[1]._graphic, data_item.display.graphics[2]._graphic]})
                if _data_item:
                    new_display_specifier = DataItem.DisplaySpecifier.from_data_item(_data_item)
                    _document_window.display_data_item(new_display_specifier)


class HyperSpyExtension:

    # required for Swift to recognize this as an extension class.
    extension_id = "nionswift.hyperspy"

    def __init__(self, api_broker):
        # grab the api object.
        api = api_broker.get_api(version="1", ui_version="1")
        # be sure to keep a reference or it will be closed immediately.
        self.__menu_item_ref = api.create_menu_item(RemoveBackgroundMenuItem())
        self.__align_zlp_menu_item_ref = api.create_menu_item(AlignZLPMenuItem())
        self.__map_signal_menu_item_ref = api.create_menu_item(MapSignalMenuItem())

    def close(self):
        self.__menu_item_ref.close()
        self.__align_zlp_menu_item_ref.close()
        self.__map_signal_menu_item_ref.close()
