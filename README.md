#govBot
***govBot*** will download webpages containing lists of elected officials, track changes, and update dataset. Higher level offices will be monitored with attended processes.

##Overview
govBot is a series of functions which will keep up-to-date a listing of elected officials. Lower level (county and below) and all executive offices will be updated using unattended processes which monitor websites for changes, and higher level legislative offices (state legislative and above) will be update via attended processes which download an entirely new list of legislators and check against current data.

##Attended Scripts
Attended processes are used to standardize data listed in reasonably consistent formats. 
-The Federal script is complete, and will update 'FE Elected Officials.csv' after the user answers a few clarifying prompts. 
-Calling any of the current SL scripts will output a CSV with all the information that can be obtained from the body's website. 
Once the SL functions are complete, they will be merged into a single file which can update the more-than-7000 State Legislators.

###Current attended scripts:
attended/FE/updatefederal.py,
attended/SL/FLHouse.py,
attended/SL/GAHouse.py,
attended/SL/GASenate.py,
attended/SL/HILeg.py,
attended/SL/INLeg.py,
attended/SL/MALeg.py,
attended/SL/MNSenate.py,
attended/SL/MSLeg.py

##Unattended scripts
The unattended scripts download source from elected official listing pages and add them to a MYSQL database, index the current and previous page versions along with known officeholder information to identify when a presumed elected official no longer appears on a given page. Each of these scripts take several hours of uninterrupted internet access to run.

###Current unattended scripts:
downloadpages.py,
findwordsinpages.py,
wordsfromoffices.py,
