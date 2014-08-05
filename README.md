#govBot
***govBot*** will download webpages containing lists of elected officials, track changes, and update dataset. Higher level offices will be monitored with attended processes.

##Overview
govBot is a series of functions which will keep up-to-date a listing of elected officials. Lower level (county and below) and all executive offices will be updated using [unattended processes](https://github.com/mlambright/govBot/tree/master/unattended/) which monitor websites for changes, and higher level legislative offices (state legislative and above) will be updated via [attended processes](https://github.com/mlambright/govBot/tree/master/attended/) which download an entirely new list of legislators and check against current data.