###MCDA Decision Analytics.

This code implements a MCDA model through Python. It reads input data from a
Google Spreadsheet which was generated using Google Apps Script using the code in
generateform.js. This input form data is in likert scales measuring the users
preferences in a pairwise manner.

The output being a final decision tree with weights for the relative importance
of the different factors in the decision.

##Dependencies

This script makes use of the following Python packages:

1. gspread

2. oauth2client

3. numpy

4. pandas

5. networkx
