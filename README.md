# PY3finder
Search for Python 3 compatible packages which are Idle or Blocked in PortingDB.
If you find some package with this tool:

* Check, if it is really Python 3 compatible.
  * If you find package, which is not Python 3 compatible (it is miss marked in PyPI or it is different package in PortingDB and PyPI), add it to `ingnore.txt` file.
* If it is IDLE package: 
  * Look at Bugzilla, if there is already a reported "Provide Python 3 subpackage" or "New version release" bug.
    * If there is a bug, make it Blocks #1285816.
    * If there is no bug read this: https://fedoraproject.org/wiki/User:Pviktori/Python_3_Bug_Filing and fill the bug! :)
* If it is BLOCKED package, continue there: Investigate & Annotate > But it is Python 3 compatible upstream! > Blocked packages http://fedora.portingdb.xyz/howto/#investigate-annotate
