import collections


class FrameDict(collections.OrderedDict):
    #   Any restrictions to the frame dictionary goes here.
    def __init__(self, *args, **kwds):
        super(FrameDict, self).__init__(*args, **kwds)

    def __setitem__(self, key, value):
        # if value is 999.9 then keep the old one else update.
        if value != 999.9:
            collections.OrderedDict.__setitem__(self, key, value)
