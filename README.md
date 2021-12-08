# firstrate-data  

## Description

This is the source code for a simple website to manage a local copy of firstrate data.

## FirstRate Data Structure

FirstRate data is stored in bundled zip files. Updates are stored in update files.
There should not be any overlap between base download files, which are quite large, and the update files.
So, once we initially download, all we have to do is check every day if there is an update on the remote
update files. If there is, then add to our local copies. If not, then do nothing. If we fail to update
for a week straight, then that is the only time when we would have to redownload the original files.
