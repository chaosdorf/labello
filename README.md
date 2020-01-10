## ABOUT ##

A printing service for the **Brother QL-720NW** and similar label printer.  
The brotherprint library  is from: https://github.com/fozzle/python-brotherprint  

## RUN ##

You only need Python 2.7 or Python 3!  
Change the **labelprinterServeConf.py** to yor needs or create a **labelprinterServeConf_local.py**, all variables set there will overwrite the default config.

run

```
python labelprinterServe.py
```

or: use Docker  

## POSSIBLE PROBLEMS AND POSSIBLE SOLUTIONS ##

### weird behaviour on old Python versions ###

The main deployment of this software uses a relatively current version
of Python (take a look at `Dockerfile` to see which one).

If you experience weird bugs (especially encoding-related ones)
while using an older version of Python, please file an issue and
try to use a newer version of Python.
