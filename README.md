# IOready
Python code to handle multi-regional input-output tables

This repository includes Python3 code and various materials to handle multi-regional input-output tables (mrio), in particular [exiobase](http://www.exiobase.eu/) tables, preparing them for further analysis (e.g. carbon footprint-ing etc.). The primary audience is people working within the field of industrial ecology.

This code leaves some manual work to the user, but also autonomy. The idea is that IOready should allow importing/exporting/preparing/reshaping mrio tables in a format consistent with the official [exiobase format](http://www.exiobase.eu/index.php/data-download/exiobase2-year-2007-full-data-set), thus making them *ready* for further analysis/calculations. This is stuff I have initially developed for my own use because I was frustrated by how unpractical was working with large mrio tables.

For calculations and further analysis, and on the same topic as mrio and IO analysis, you find more advanced material at Konstantin Stadler's [pmyrio](https://github.com/konstantinstadler/pymrioSim) repository and Stefan Pauliuk's [pySUT](https://github.com/stefanpauliuk/pySUT) repository. Many many operations possible with them.


This repository included:
+ __IOready_inout.py__: functions to import and export mrio tables in different formats (single, multi, exiobase)and from files of different formats (.txt, .csv).

+ __IOready.py__: a Python Class to do some stuff with these tables, in particular:
    - aggregate a non-square mrio table to get a square one based on a key
    - correct a table for investments using value added extensions


+ Some __test scripts__ where the principles of the above mentioned functions is explained (right now only in .py format, soon to be in Jupyter Notebook format)

At present stage it is not possible to perform other operations.
