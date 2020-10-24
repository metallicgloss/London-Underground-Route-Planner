# Sanitisation Review

## IMPORTANT NOTES
The testing carried out in this section should be considered void due to incorrect assumptions made that related to the data (linear trainline without connections).

## Assumptions & Testing Notes
Testing was carried out using only the data that was provided with no context to carry out obvious validation problems such as missing data, incorrect data or duplicated content.
Following the data provided and the station order, it was assumed that the data should be interpreted as a linear train line.

## Automated Method Overview
The automated testing was carried out to be able to identify quickly any obvious errors that would fail simple data validation checks. Utilising this method allows for obvious outliers to be rapidly identified, including any missing data which could be overlooked when manually checking. Initial development may take as much time as a single manual review, or potentially more, but repeated checks or on subsequent data sets would dramatically cut down the on time taken to process information.

## Manual Method Overview
The manual method was carried out to be able to determine if the automated process was able to pick up all of the problems with the document; this method is considerably slower for repeat checks compared to the automated version and also can find more challenging problems that could have been missed by the script (at the same time introducing human error)

## Findings
- The formatting of the data and lack of context made the initial review and cleansing of the data much harder than it needed to be.
- The automated script took 41 minutes but didn't catch all of the identifiable problems with the data. Repeated checks would be less than 5 seconds.
- The manual review method took 39 minutes but introduced one obvious human error for route validation. Repeated checks would be similar in time.
- The data that has been given, which provided the order of the tube stations, was identified quickly as being a source of a problem and didn't provide any contextual information that would be needed to handle line branches or loops.
- Timed data allows for line branches to be identified; factoring line branches and loops would allow for most of the data integrity faults to be cleared. It has been noted that the import of the data is going to be considerably more tricky to handle such anomalies than if it is linear.