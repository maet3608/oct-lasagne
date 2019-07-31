# oct-lasagne

Tool for the surface annotation of retinal Optical Coherence Tomography (OCT) 
volumes.

![UI](https://github.com/maet3608/oct-lasagne/blob/master/ui.png)



## Installation

```
git clone https://github.com/maet3608/oct-lasagne.git
cd oct-lasagne
python setup.py install
```
 
If the [Kivy](https://kivy.org) installation fails, install it manually: 

```
python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew
python -m pip install kivy
```

For more details see the [installation instructions](https://kivy.org/#download).
If this fails as well, try to install the wheel instead. 
Download a matching wheel from [here](https://kivy.org/downloads/appveyor/kivy/), 
e.g. `Kivy-2.0.0.dev0-cp37-cp37m-win32.whl` for Windows and Python 3.7,
and install with 

```
python -m pip install Kivy-1.10.1-cp36-cp36m-win_amd64.whl
```   


## Usage

```
USAGE:
python octlasagne.py <configfile> 

EXAMPLE 1:
cd oct-lasange/octlasange
python octlasagne.py  config.json
```

## Configuration file

The configuration file is a file in JSON format that specifies application 
parameters such as

- the data directory (datadir) that contains the OCT volumes to annotate
- a scaling factor (ratio) for the width of the displayed scans
- a list of scans that are locked for annotation. 
 
Here an example of a configuration file:

```JSON
{
  "datadir": "data/oct_volumes",
  "ratio" : 4.0,
  "locked" : [0, 5, 10]
}
```


## User interface

A short description of the user interface.

### Menu

- ``Annotation``
    - ``Filter``: Filter for data using [Pandas]() format, e.g. 
        ``oct_id.str.startswith('oct_d15_1')``  
    - ``Add layer...``: Add a new layer with the given name
    - ``Del layer...``: Deletes the layer with the given name
    - ``Save`` : Save current annotation to ``annotation.pkl``
    - ``Load backup`` : Loads the backup of the annotation file.
    - ``Show all ON|OFF`` : Toggle display of ALL layers
    - ``Show layer ON|OFF`` : Toggle display of current layer polyline
    - ``Autosave ON|OFF`` : Automatically save annotation when exiting 
    
### Navigation

- Button ``OCT >>`` or ``Cursor up``: next cube 
- Button ``<< OCT`` or ``Cursor down``: previous cube
- Button ``Scan >>`` or ``Cursor left``: next B-scan within current cube
- Button ``<< Scan`` or ``Cursor right``: previous B-scan within current cube

### Viewing

- Hold any mouse button and move to pan
- Use mouse wheel for zooimng in and out
- Toggle display of current annotation layer by pressing ``v``
- Toggle display of all annotated layers by pressing ``a``

### Editing

- Add point: ALT + left mouse click
- Move point: CTRL + left mouse click
- Delete point: SHIFT + left mouse click

### Timer
- start/stop timer by pressing ``s``
- reset timer by pressing ``r``

### Exiting

Exit a dialog or the application by pressing the ESC button. The layer 
annotation will automatically be saved (provided ``Auto ON`` is set)


## Data

The data folder must contain OCT volumes as 3D numpy arrays (``dtype='uint8'``), 
where the first axis is the B-scan, followed by rows(depth) and cols(width) 
of the B-scan, with image origin in the upper left corner.


## Annotation

Surface annotation is stored as a pickle file in ``annotation.pkl``, 
within the data folder.

In addition a backup file of the annotation in CSV format is also stored
and can be loaded via the menu item ``Load backup``

