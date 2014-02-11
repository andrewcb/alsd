alsd - the Ableton Live Set dumping utility
====

alsd is a utility for extracting and dumping data from Ableton Live set 
files on a disk. It is a standalone Python program which reads the file, 
and does not depend on Live. 

Currently alsd is very basic; it can list the tracks in a Live set, and,
if the -D option is specified, list the devices on each track. For plugin
devices, it lists the name of the plugin, and for AudioUnit plugins, it 
can usually list the preset name (if any) in use. 
Further functionality will be added in the future.

Usage:
======

To use, run alsd.py with the path of the Ableton Live set file; this is 
a file whose name typically ends in .als. 

Technical details
=================

alsd is written in Python and has no external dependencies. It was 
developed using Python 2.7.  

An Ableton Live set file is just a .gzipped XML file, and whilst being 
quite long and detailed, seems not too difficult to understand. 


License
=======

This code is distributed under the Apache open source license.

Author:
======
Andrew Bulhak   http://dev.null.org/acb/  http://github.com/andrewcb/
