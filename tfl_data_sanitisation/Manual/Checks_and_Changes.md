# Manual Data Review

### First Pass Time Taken (Inc Documentation): 39 Minutes

## Tubeline - Name Check
- Bakerloo - Passed
- Central - Passed
- Circle - Failed
    - 1 Route Missing Assignment
        - Paddington -> Royal Oak
- District - Passed
- Hammersmith & City - Passed
- Jubilee - Passed
- Metropolitan - Passed
- Northern - Passed
- Piccadilly - Passed
- Victoria - Passed
- Waterloo & City - Passed

## Start & End Station Check
- Bakerloo - Passed - Harrow & Wealdstone - Elephant & Castle
- Central - Passed - Epping - West Ruislip
- Circle - Passed - Edgware Road - Hammersmith
- District - Passed - Upminster - Ealing Broadway
- Hammersmith & City - Passed - Barking - Hammersmith
- Jubilee - Passed - Stanmore - Stratford
- Metropolitan - Passed - Amersham - Aldgate
- Northern - Passed - High Barnet - Morden
- Piccadilly - Passed - Cockfosters - Uxbridge
- Victoria - Passed - Walthamstow Central - Brixton
- Waterloo & City - Passed - Bank - Waterloo

## Missing / Duplicate Data Check
- Bakerloo - Passed
    - 25 Stations, 24 Routes Provided
- Central - Failed
    - 49 Stations, 49 Routes Provided
        - Roding Valley -> Woodford - Duplicate Route To Woodfood - To Be Removed
- Circle - Partial Fail
    - 35 Stations, 35 Routes Provided
        - Fail disregarded, assume as valid. Additional route provided as tube line re-visits Paddington.
- District - Passed
    - 60 Stations, 59 Routes Provided
- Hammersmith & City - Passed
    - 29 Stations, 28 Routes Provided
- Jubilee - Passed
    - 27 Stations, 26 Routes Provided
- Metropolitan - Failed
    - 34 Stations, 36 Routes Provided
        - Harrow-on-the-Hill -> Wembley Park - Duplicate Route To Wembley Park - To Be Removed
        - Harrow-on-the-Hill -> Finchley Road - Duplicate Route To Finchley Road - To Be Removed
        - Harrow-on-the-Hill -> Northwick Park - Duplicate Route To Northwick Park - To Be Removed
- Northern - Failed
    - 50 Stations, 51 Routes Provided
        - Warren Street -> Euston - Duplicate Route To Euston - To Be Removed
        - Euston -> Camden Town - Duplicate Route To Camden Town - To Be Removed
- Piccadilly - Failed
    - 53 Stations, 53 Routes Provided
        - Hammersmith -> Acton Town - Duplicate Route To Action Down - To Be Removed
- Victoria - Passed
    - 16 Stations, 15 Routes Provided
- Waterloo & City - Passed
    - 2 Stations, 1 Route Provided

## Data Integrity Check
- Bakerloo - Passed
- Central - Failed
    - 4 Incorrect Routes
        - Snaresbrook -> Leytonstone - Should be: Snaresbrook -> Roding Valley
        - Roding Valley	-> Chigwell - Should be: Woodford -> Chigwell
        - North Acton -> West Acton - Should be: Hanger Lane -> West Acton
        - Hanger Lane -> Perivale - Should be: Ealing Broadway -> Perivale
- Circle - Passed
- District - Failed
    - 4 Incorrect Routes
        - Earl's Court -> High Street Kensington - Should be: Kensington (Olympia) -> High Street Kensington
        - Earl's Court -> West Brompton - Should be: Edgware Road -> West Brompton
        - Earl's Court -> West Kensington - Should be: Wimbledon -> West Kensington
        - Turnham Green -> Chiswick Park - Should be: Richmond -> Chiswick Park
- Hammersmith & City - Passed
- Jubilee - Passed
- Metropolitan - Failed
    - 5 Incorrect Routes
        - Amersham -> Chalfont & Latimer - Should be: Amersham -> Chesham
        - Rickmansworth -> Moor Park - Should be: Rickmansworth -> Watford
        - Croxley -> Moor Park - Should be: Croxley -> Uxbridge
        - Moor Park -> Harrow-on-the-Hill  - Should be: Moor Park -> Northwick Park
        - Harrow-on-the-Hill -> Wembley Park
- Northern - Failed
    - 2 Incorrect Routes
        - West Finchley -> Finchley Central - Should be: West Finchley -> Mill Hill East
        - Euston -> King's Cross St. Pancras - Should be: Kennington -> King's Cross St. Pancras
- Piccadilly - Failed
    - 2 Incorrect Routes
        - Hatton Cross -> Heathrow Terminal 4 - Should be: Heathrow Terminal 5 -> Heathrow Terminal 4
        - Acton Town -> Ealing Common - Should be: Heathrow Terminal 4 -> Ealing Common
- Victoria - Passed
- Waterloo & City - Passed

## Station Name Validation Check
- Bakerloo - Passed
- Central - Passed
- Circle - Passed
- District - Passed
- Hammersmith & City - Passed
- Jubilee - Passed
- Metropolitan - Passed
- Northern - Passed
- Piccadilly - Passed
- Victoria - Passed
- Waterloo & City - Passed

## Extreme Value Check
- Bakerloo - Passed
- Central - Passed
- Circle - Passed
- District - Passed
- Hammersmith & City - Passed
- Jubilee - Passed
- Metropolitan - Failed
    - 2 Routes Pending Review
        - Moor Park -> Harrow-on-the-Hill - 14 minutes.
        - Harrow-on-the-Hill -> Finchley Road - Disregard, route to be removed.
- Northern - Passed
- Piccadilly - Passed
- Victoria - Passed
- Waterloo & City - Passed