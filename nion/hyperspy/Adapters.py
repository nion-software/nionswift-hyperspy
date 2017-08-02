import hyperspy.signals
from nion.data import DataAndMetadata

def xdata_to_signal(xdata: DataAndMetadata.DataAndMetadata) -> hyperspy.signals.BaseSignal:
    return hyperspy.signals.Signal1D(xdata.data)

def signal_to_xdata(signal: hyperspy.signals.BaseSignal) -> DataAndMetadata.DataAndMetadata:
    return DataAndMetadata.new_data_and_metadata(signal.data)
