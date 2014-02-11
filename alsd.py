#!/usr/bin/python

# alsd -- Ableton Live set dumping utility
# by Andrew Bulhak  http://dev.null.org/acb/
#
# For instructions, read the README, or type alsd.py -h

import xml.etree.ElementTree as ET
import gzip
import plistlib

# the maybe monad
def bind(val, f):
    return (val is not None) and f(val) or None

hexchars = set('0123456789abcdef')
def decodeHexString(str):
    """Decode a hex string, ignoring all non-hex characters"""
    return filter(lambda c:c in hexchars, str.lower()).decode('hex')

def hideUnprintable(str, maskchar='.'):
    return ''.join(map(lambda c:(ord(c)>0x1f and ord(c)<0x7e) and c or maskchar, str))

#  ---- classes

class ALSNode(object):
    """
    The parent class of all .als nodes
    """
    def __init__(self, elem):
        self.elem = elem


class LiveSetMidiClipData(object):
    """
    An object encapsulating a MidiClip node.
    """
    pass

class LiveSetAuPluginPresetData(object):
    """
    An object encapsulating the data stored in a preset buffer
    """
    def __init__(self, text):
        self.text = decodeHexString(text)
        self.plist = plistlib.readPlistFromString(self.text)
        self.name = self.plist.get('name')

class LiveSetDeviceData(ALSNode):
    """
    An object encapsulating the data for a device
    """
    def __init__(self, elem):
        super(LiveSetDeviceData, self).__init__(elem)
        self.deviceType = elem.tag
        self.auPresetBuffer = bind(elem.find("PluginDesc/AuPluginInfo/Preset/AuPreset/Buffer"), lambda e:LiveSetAuPluginPresetData(e.text))
        self.auPresetName = bind(self.auPresetBuffer, lambda b:b.name)

        self.presetName = bind(elem.find("UserName"), lambda e:e.get("Value")) \
                or bind(elem.find("PluginDesc/AuPluginInfo/Name"), lambda e:': '.join([v for v in [e.get("Value"),self.auPresetName] if v is not None])) \
                or bind(elem.find("PluginDesc/VstPluginInfo/PlugName"), lambda e:e.get("Value")) \
                or ""
        self.name = "%s: %s"%(self.deviceType, self.presetName)


class LiveSetTrackData(ALSNode):
    """
    An object encapsulating the data for a Track
    """
    def __init__(self, elem):
        super(LiveSetTrackData, self).__init__(elem)
        self.trackType = elem.tag
        self.name = bind(elem.find('Name/EffectiveName'), lambda e:e.get('Value'))
        self.devices = [LiveSetDeviceData(c) for c in elem.find("DeviceChain/DeviceChain/Devices")]
        self.clipslots = bind(elem.find("DeviceChain/MainSequencer/ClipSlotList"), lambda x:x.findall("ClipSlot"))
        # TODO: encapsulate these in a class
        self.midiclips = bind(elem.find("DeviceChain/MainSequencer/ClipSlotList"), lambda x:x.findall(".//MidiClip"))


class LiveSetData(object):
    """
    An object encapsulating a parsed Live set.
    """
    def __init__(self, path):
        self.etree = ET.parse(gzip.GzipFile(path))
        self.live_set = self.etree.getroot().find("LiveSet")
        self.tracks = [LiveSetTrackData(c) for c in self.live_set.find("Tracks")]


def dumpinfo(path, track=None, show_devices=True):
    """Print out some info about an Ableton Live set at a path"""
    lsd = LiveSetData(path)


    def dumptrack(i, t):
        print "%d: %s (%s)"%(i, t.name, t.trackType)
        if show_devices:
            for dev in t.devices:
                print "  %s"%dev.name
    if track is not None:
        try:
            track = int(track)
        except ValueError:
            sys.exit("Track option must be a number")
        if track>len(lsd.tracks):
            sys.exit("%s has only %d tracks"%(path, len(lsd.tracks)))

        dumptrack(track, lsd.tracks[track-1])
    else:
        for (i,t) in enumerate(lsd.tracks):
            dumptrack(i+1, t)


if __name__ == "__main__":
    import sys
    import optparse

    globalopts = [
        optparse.make_option("-t", "--track", dest="track", help="The track number to display"),
        optparse.make_option("-D", "--show-devices", dest="show_devices", action="store_true", default=False, help="List devices for each track")
    ]

    optp = optparse.OptionParser(option_list=globalopts)
    (opts, args) = optp.parse_args(sys.argv[1:])
    for fn in args:
        dumpinfo(fn, track=opts.track, show_devices=opts.show_devices)

