import os
import config as cf
import time
import datetime as dt

logDirectory = cf.logDirectory
archiveDirectory = cf.logArchiveDirectory
cur_date = dt.date.today()
archived_count = 0

for file in os.listdir(logDirectory):
    current_loc = os.path.join(logDirectory,file)
    
    # Skipping any subdirectories (e.g. Archive)
    if not os.path.isfile(current_loc):
        continue
        
    creation_time = os.path.getctime(os.path.join(logDirectory,file))
    creation_date = dt.date.fromtimestamp(creation_time)
    date_dif = cur_date - creation_date
    
    if date_dif.days > 30:
        
        new_loc = os.path.join(archiveDirectory,file)
        try:
            os.replace(src=current_loc,dst=new_loc)
            archived_count += 1
        except OSError:
            print(f"Could not replace {current_loc} with {new_loc}")
        
    else:
        print(f"Newish file: {file}")
        
print(f"Finished housekeeping! {archived_count} files archived...")