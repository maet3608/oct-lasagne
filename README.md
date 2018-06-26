# oct-lasagne

Tool for the surface annotation of retinal Optical Coherence Tomography (OCT) 
volumes.

![UI](https://github.ibm.com/aur-mma/gazer-oct/blob/master/ui.png)



## Installation

```
git clone https://github.com/maet3608/oct-lasagne.git
cd oct-lasagne
python setup.py install
```
 
If the [Kivy](https://kivy.org) installation fails, install manually: 
[installation instructions](https://kivy.org/#download)
   


## Usage

```
USAGE:
python -m octlasange.app <datadir>
python octlasange.app.py <datadir>

EXAMPLE:
python -m octlasange.app  mydata/octvolumes
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

### Exiting

Exit a dialog or the application by pressing the ESC button. The layer 
annotation will automatically be saved (provided ``Auto ON`` is set)


## Data

The data folder must contain OCT volumes as 3D numpy arrays (``dtype='uint8``), 
where the first axis is the B-scan, followed by height and width of the B-scan.


## Annotation

Surface annotation is stored as a pickle file in ``annotation.pkl``, 
within the data folder.

In addition a backup file of the annotation in CSV format is also stored
and can be loaded via the menu item ``Load backup``

