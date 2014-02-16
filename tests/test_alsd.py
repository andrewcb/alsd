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

	def test_001_mastertrack(self):
		self.assertEqual(self.testdev1.mastertrack.mixer.params['Volume'].manual, 1)
		self.assertEqual(self.testdev1.mastertrack.mixer.params['Tempo'].manual, 120)
	def test_010_au_devices(self):
		trk = self.testdev1.tracks[0]
		self.assertEqual(trk.devices[0].presetName, "FM8: 6ties Mute Bass")
		self.assertEqual(trk.devices[1].presetName, "Combo: Untitled")
	def test_011_vst_devices(self):
		trk = self.testdev1.tracks[1]
		self.assertEqual(trk.devices[0].presetName, "Massive")
		self.assertEqual(trk.devices[1].presetName, "Driver")

	def test_020_clips(self):
		trk = self.testdev1.tracks[0]
		self.assertEqual(len(trk.midiclips), 2)
		self.assertEqual([c.name for c in trk.midiclips], ["A clip", "Another clip"])

		clip0 = trk.midiclips[0]
		self.assertEqual(clip0.launchMode, 0)
		self.assertEqual(clip0.currentStart, 0)
		self.assertEqual(clip0.currentEnd, 16)
		self.assertEqual(clip0.loopLength, 16)

		clip1 = trk.midiclips[1]
		self.assertEqual(clip1.loopLength, 4)

	def test_021_midinotes(self):
		trk = self.testdev1.tracks[0]
		clip0 = trk.midiclips[0]
		self.assertEqual(len(clip0.notes), 4)
		self.assertEqual([n.time for n in clip0.notes], [0.0, 1.0, 1.5, 2.0])
		self.assertEqual([n.key for n in clip0.notes], [60, 65, 57, 62])
		self.assertEqual([n.duration for n in clip0.notes], [1.0, 0.5, 0.5, 0.25])
		self.assertEqual([int(n.velocity) for n in clip0.notes], [110, 64, 100, 100])
		clip1 = trk.midiclips[1]
		self.assertEqual(len(clip1.notes), 7)

	def test_100_timesigs(self):
		testtimesig = alsd.LiveSetData("test_timesignatures Project/test_timesignatures.als")
		self.assertEqual(testtimesig.timeSignatures(), [(0, (4,4)), (4,(1,1)), (8,(6,8)), (14,(7,4)), (21,(1,16))])



if __name__ == "__main__":
	unittest.main()
