alsd - An Ableton Live Set dumping utility
====

alsd is a utility for extracting and dumping data from Ableton Live set 
files on a disk. It is a standalone Python program which reads the file, 
and does not depend on Live. 

Currently alsd is very basic; it can list the tracks in a Live set, and,
optionally list the devices or MIDI clips on each track, if the -D or -C 
options are specified. For plugin devices, it lists the name of the 
plugin, and for AudioUnit plugins, it can usually list the preset name 
(if any) in use.  Currently, only the names and durations (in beats) of 
clips are displayed.  Further functionality will be added in the future.

Usage:
======

To use, run alsd.py with the path of the Ableton Live set file; this is 
a file whose name typically ends in .als. This is typically located within
a Project folder which Live creates for you.

I.e., an invocation could look like: 

```
./alsd.py -D  /Volumes/Music/Bangin\ Groove\ Project/Bangin\ Groove.als
```

You may need to ```chmod +x alsd.py``` first or otherwise prefix it with 
```python``` if it is not executable.

To see a list of options, run alsd.py with the -h flag, i.e.,
```
alsd.py -h
```

Technical details
=================

alsd is written in Python and has no external dependencies. It was 
developed using Python 2.7.  

An Ableton Live set file is just a .gzipped XML file, and whilst being 
quite long and detailed, seems not too difficult to understand. 

There are unit tests in the tests subdirectory; to run, use 
```python test_alsd.py```.

License
=======

This code is distributed under the Apache open source license.

Author:
======
Andrew Bulhak   http://dev.null.org/acb/  http://github.com/andrewcb/

Ableton and Live are trademarks of Ableton AG. This code is not in any way
associated with or endorsed by them, and makes no claim of any official 
connection with Ableton.

This program is provided without any warranty of any sort; in fact, at the 
moment, it is pretty much guaranteed to be incomplete.
