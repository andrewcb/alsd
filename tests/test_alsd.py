import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
import unittest
import alsd

class TestLiveInfo(unittest.TestCase):

	def setUp(self):
		self.testdev1 = alsd.LiveSetData("test_devices_1 Project/test_devices_1.als")
	def test_000_tracks(self):
		lsd = self.testdev1
		self.assertEqual(len(lsd.tracks), 5)
	def test_001_au_devices(self):
		trk = self.testdev1.tracks[0]
		self.assertEqual(trk.devices[0].presetName, "FM8: 6ties Mute Bass")
		self.assertEqual(trk.devices[1].presetName, "Combo: Untitled")
	def test_002_vst_devices(self):
		trk = self.testdev1.tracks[1]
		self.assertEqual(trk.devices[0].presetName, "Massive")
		self.assertEqual(trk.devices[1].presetName, "Driver")

	def test_010_clip_count(self):
		trk = self.testdev1.tracks[0]
		self.assertEqual(len(trk.midiclips), 2)



if __name__ == "__main__":
	unittest.main()
