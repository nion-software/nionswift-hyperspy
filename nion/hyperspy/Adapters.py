import numpy
import hyperspy.signals
from nion.data import Calibration
from nion.data import DataAndMetadata

def xdata_to_signal(xdata: DataAndMetadata.DataAndMetadata, copy_data=False) -> hyperspy.signals.BaseSignal:
    axes = list()
    for size, calibration in zip(xdata.data_shape, xdata.dimensional_calibrations):
        axis = dict()
        axis['size'] = size
        if calibration.offset:
            axis['offset'] = calibration.offset
        if calibration.scale:
            axis['scale'] = calibration.scale
        if calibration.units:
            axis['units'] = calibration.units
        axes.append(axis)
    data = numpy.copy(xdata.data) if copy_data else xdata.data
    return hyperspy.signals.Signal1D(data, axes=axes)

def signal_to_xdata(signal: hyperspy.signals.BaseSignal) -> DataAndMetadata.DataAndMetadata:
    dimensional_calibrations = list()
    for axis in signal.axes_manager.navigation_axes + signal.axes_manager.signal_axes:
        dimensional_calibrations.append(Calibration.Calibration(axis.offset, axis.scale, axis.units))
    data_descriptor = DataAndMetadata.DataDescriptor(False, len(signal.axes_manager.navigation_axes), len(signal.axes_manager.signal_axes))
    return DataAndMetadata.new_data_and_metadata(signal.data, dimensional_calibrations=dimensional_calibrations, data_descriptor=data_descriptor)
