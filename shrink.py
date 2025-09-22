from pathlib import Path
import os, shutil, sys

def error(message):
    print('\033[0;31m' + 'ERROR:' + '\033[0m', message)
    sys.exit(1)

def info(message):
    print('\033[0;32m' + 'INFO:' + '\033[0m', message)

# this function processes iwd archives entirely
def process_iwd(iwd_file, base_dir, iwd_dir_path):
    info('Processing archive: ' + iwd_file)
    try:
        TEMP_DIR = os.path.join(base_dir, 'server-strip-temp')
        os.makedirs(TEMP_DIR)
    except:
        error('Failed to (re)create server-strip-temp directory.')

    # move file to temp dir to be processed
    try:
        shutil.move(os.path.join(base_dir, iwd_dir_path, iwd_file), TEMP_DIR)
    except:
        error('Failed to move archive ' + iwd_file + ' to temp directory ' + TEMP_DIR)

    # rename and unpack archive into temp dir
    TEMP_ZIP = os.path.join(TEMP_DIR, 'current_iwd.zip')
    try:
        os.rename(os.path.join(TEMP_DIR, iwd_file), TEMP_ZIP)
        shutil.unpack_archive(TEMP_ZIP, TEMP_DIR)
        os.remove(TEMP_ZIP) # remove current_iwd.zip since we're done with it

        # remove matching directories: video, images, sound
        for TEMP_DIRS in os.walk(TEMP_DIR):
                if TEMP_DIRS[0].endswith(('video', 'images', 'sound')) and Path(TEMP_DIRS[0]).is_dir():
                    shutil.rmtree(TEMP_DIRS[0])

        # remove matching extensions: .iwi, .mp3
        for TEMP_ROOT, _, TEMP_FILES in os.walk(TEMP_DIR):
            for TEMP_FILE in TEMP_FILES:
                    if TEMP_FILE.endswith(('.iwi', '.mp3')):
                        os.remove(os.path.join(TEMP_ROOT, TEMP_FILE))

    except:
        error('Failed to process archive ' + iwd_file)

    # re-archive and put the file back where it was
    try:
        shutil.make_archive(os.path.join(base_dir, iwd_dir_path, iwd_file), format='zip', root_dir=TEMP_DIR)
        os.rename(os.path.join(base_dir, iwd_dir_path, iwd_file + '.zip'), os.path.join(base_dir, iwd_dir_path, iwd_file))
    except:
        error('Failed to restore processed archive ' + iwd_file)

    # clean out temp directory, the cleanest way to do this is to just remove the dir and remake it, love pythons stdlib
    try:
        shutil.rmtree(TEMP_DIR)
    except:
        error('Failed to remove temp directory ' + TEMP_DIR)

# this function searches for iwd files
def crawl_dir(iwd_dir_path):
    target = os.path.join(base_dir, iwd_dir_path)
    for root, _, files in os.walk(target):
        files = filter(lambda file: file.endswith('.iwd'), files)
        for iwd_file in files:
            process_iwd(iwd_file, base_dir, iwd_dir_path)

def main():
    info('Attempting to strip visual assets from IW4x...')
    # quickly get large 'video' directories out of the way
    for i in os.walk(base_dir):
        if i[0].endswith('video') and Path(i[0]).is_dir():
            info('Removing directory: ' + i[0])
            try:
                shutil.rmtree(i[0])
            except:
                error('Failed to remove directory: ' + i[0])

    for iwd_dir in 'iw4x', 'main': # directories to search for .iwd files
        crawl_dir(iwd_dir)

if len(sys.argv) > 2:
    error('Too many arguments. Expected: server-stripper.py /path/to/directory')
elif len(sys.argv) == 2:
    if Path(sys.argv[1]).is_dir():
        base_dir = sys.argv[1]
    else:
        error('Argument: ' + sys.argv[1] + ' is not a directory.')
else:
    base_dir = os.getcwd()

# VERY basic check to make sure we're in the right place
if not Path(base_dir, 'iw4x').is_dir():
    error('IW4x files not found. Are we in the correct location?')

if __name__ == "__main__":
    main()
