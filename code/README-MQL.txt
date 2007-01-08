What is this?
=============

This is Constantin von Tischendorf's 8th edition of the Greek New
Testament, packaged in MQL format for easy loading into Emdros.


Using it with Emdros
====================

Run the tisch.mql file through the mql program:

- If on MySQL:

  mql -b my -p <password> -u <dbuser> tisch.mql

- If on PostgreSQL:

  mql -b pg -p <password> -u <dbuser> tisch.mql

- If on SQLite 2:

  mql -b l tisch.mql

- If on SQLite 3:

  mql -b 3 tisch.mql


This will create and populate the database "tisch".


There is a "tisch.cfg" file that you can use with the Emdros Query
Tool.


Ulrik Petersen



------------------- Official introduction starts -------------------

