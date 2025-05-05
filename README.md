# mouse-process
The data processing and analysis code for the mouse tracker data. Does not include any of the necessary data for privacy reasons.

The `src/comp specs collect.html` file includes a modified version of the narrative game used for research purposes, which does
include a mouse tracker that records the position of the mouse on the click event. This data is discarded unless downloaded
from the browser on the last page of the story. This downloaded data would also include information about the final state of
the variables used during the playthrough.

The four python files are all designed to take in an assortment of data and preprocess it for the `src/data_analysis.R` file.
They are designed to be run outside of the `src` folder, though that is somewhat irrelevant on account of the fact that the
data is not included. Below is the commands in the recommended order.

1. `python src\data_processing.py`
2. `python src\times_processing.py`
3. `python src\html_processing.py`
4. `python src\final_sort.py`

Once the data prepocessing is complete, the `src/data_analysis.R` file is ready to be run. The current paths are
hardcoded to the machine it was ran on, as it was run using RStudio's `Source` functionality. As such, they would
need to be modified to suit the user's machine/paths.
