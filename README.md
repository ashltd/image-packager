# image-packager
This tool allows to create an Arkham Horror LCG or Marvel Champions LCG Image Package.

The script expects to find the following items in the execution folder:
	1 - set.xml: The definition of the scenario pack from where the GUID are extracted.
	2 - scans: The folder containing all the images. Each image must be name as the Card number. If the card is the back side the ".B" must be added to the number


The script will generate the image pack file (.o8c)