"""Simple Python script to archive log files older than 30 days"""

import os
import datetime as dt
import ShoppingTracker.PythonSrc.core.config as cf

def archive_old_log_files():

    """Archives any files in the log directory that are older than 30 days"""
    log_dir = cf.LOG_DIR
    archive_dir = cf.LOG_ARCHIVE_DIR
    cur_date = dt.date.today()
    archived_count = 0

    for log_file in os.listdir(log_dir):
        current_loc = os.path.join(log_dir,log_file)

        # Skipping any subdirectories (e.g. Archive)
        if not os.path.isfile(current_loc):
            continue

        creation_time = os.path.getctime(os.path.join(log_dir,log_file))
        creation_date = dt.date.fromtimestamp(creation_time)
        date_dif = cur_date - creation_date

        if date_dif.days > 30:

            new_loc = os.path.join(archive_dir,log_file)
            try:
                os.replace(src=current_loc,dst=new_loc)
                print(f"Archived: ${current_loc}")
                archived_count += 1
            except OSError:
                print(f"Could not replace {current_loc} with {new_loc}")

        else:
            print(f"Not archived: {log_file}")

    print(f"Finished housekeeping! {archived_count} files archived...")
