#govBot
***govBot*** will download webpages containing lists of elected officials, track changes, and update dataset. Higher level offices will be monitored with attended processes.

##Overview
govBot is a series of functions which will keep up-to-date a listing of elected officials. Lower level (county and below) and all executive offices will be updated using unattended processes which monitor websites for changes, and higher level legislative offices (state legislative and above) will be update via attended processes which download an entirely new list of legislators and check against current data.

##Attended Scripts
Attended processes are used to standardize data listed in reasonably consistent formats. 

- The Federal script (attended/FE/updateFederal.py) updates 'FE Elected Officials.csv' after the user answers a few clarifying prompts.
- The State Legislative script (attended/SL/updateSL.py) compares data from each state legislature's website to 'SL Elected Officials.csv' and outputs a file listing all disagreements.
- Calling any of the other SL scripts will output a CSV with all the information that can be obtained from the body's website. 


###Current attended scripts:
- attended/FE/updateFederal.py
- attended/SL/updateSL.py
- attended/SL/AKLeg.py
- attended/SL/ALLeg.py
- attended/SL/ARLeg.py
- attended/SL/AZLeg.py
- attended/SL/CALeg.py
- attended/SL/COLeg.py
- attended/SL/CTLeg.py
- attended/SL/DELeg.py
- attended/SL/FLHouse.py
- attended/SL/FLSenate.py
- attended/SL/GAHouse.py
- attended/SL/GASenate.py
- attended/SL/HILeg.py
- attended/SL/IALeg.py
- attended/SL/IDLeg.py
- attended/SL/ILLeg.py
- attended/SL/INLeg.py
- attended/SL/KSLeg.py
- attended/SL/KYLeg.py
- attended/SL/LALeg.py
- attended/SL/MALeg.py
- attended/SL/MDLeg.py
- attended/SL/MELeg.py
- attended/SL/MILeg.py
- attended/SL/MNHouse.py
- attended/SL/MNSenate.py
- attended/SL/MOLeg.py
- attended/SL/MSLeg.py
- attended/SL/MTLeg.py
- attended/SL/NCLeg.py
- attended/SL/NDLeg.py
- attended/SL/NELeg.py
- attended/SL/NHLeg.py
- attended/SL/NJLeg.py
- attended/SL/NMLeg.py
- attended/SL/NVLeg.py
- attended/SL/NYAssembly.py
- attended/SL/NYSenate.py
- attended/SL/OHLeg.py
- attended/SL/OKLeg.py
- attended/SL/ORLeg.py
- attended/SL/PALeg.py
- attended/SL/RILeg.py
- attended/SL/SCLeg.py
- attended/SL/SDLeg.py
- attended/SL/TNLeg.py
- attended/SL/TXLeg.py
- attended/SL/UTLeg.py
- attended/SL/VALeg.py
- attended/SL/VTLeg.py
- attended/SL/WALeg.py
- attended/SL/WILeg.py
- attended/SL/WVLeg.py
- attended/SL/WYLeg.py

##Unattended scripts
The unattended scripts download source from elected official listing pages and add them to a MySQL database, index the current and previous page versions along with known officeholder information to identify when a presumed elected official no longer appears on a given page. Each of these scripts take several hours of uninterrupted internet access to run.

###Current unattended scripts:
- downloadpages.py
- findwordsinpages.py
- wordsfromoffices.py
