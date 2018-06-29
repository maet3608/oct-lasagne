# Data set

Original source of example data is [Duke University](http://people.duke.edu/~sf59/software.html).

The dataset consists of volumetric scans acquired from 45 patients: 15 normal patients, 
15 patients with dry AMD, and 15 patients with DME using Spectralis SD-OCT.
The original data set and details can be found [here](http://people.duke.edu/~sf59/Srinivasan_BOE_2014_dataset.htm)


## Example data

3 volumes (1 normal, 1 AMD, 1 DME) were selected and converted
to Numpy format (1st axis is B-scan, then row and cols of B-scan)
with shape (49, 496, 512).
