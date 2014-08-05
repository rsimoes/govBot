##Unattended scripts
The unattended scripts download source from elected official listing pages and add them to a MySQL database, index the current and previous page versions along with known officeholder information to identify when a presumed elected official no longer appears on a given page. Each of these scripts requires several hours of uninterrupted internet access to run.

###Current unattended scripts:
- [downloadpages.py](https://github.com/mlambright/govBot/blob/master/unattended/downloadpages.py)
- [confirmNames.py](https://github.com/mlambright/govBot/blob/master/unattended/confirmNames.py)

###Required packages
- [MySQLdb](https://pypi.python.org/pypi/MySQL-python/1.2.5)
