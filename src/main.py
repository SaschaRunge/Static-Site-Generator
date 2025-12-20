import os
import shutil

LOG_PATH = "./copy_log.md"
STATIC_FOLDER = "./static"
PUBLIC_FOLDER = "./public"

def main():
    write_to_log(LOG_PATH, "", True)
    clean_public_folder()
    copy(STATIC_FOLDER, PUBLIC_FOLDER)

def copy(source, destination):
    abs_source = os.path.abspath(source)
    abs_destination = os.path.abspath(destination)

    if not os.path.exists(abs_destination):
        try: 
            os.mkdir(abs_destination)
        except Exception as e:
            raise Exception(f"Could not recreate {abs_destination}: {e}")
    
    for content in os.listdir(abs_source):
        abs_content_path = os.path.join(abs_source, content)
        write_to_log(LOG_PATH, f"Writing from: {abs_content_path} to: {abs_destination}")
        
        if os.path.isfile(abs_content_path):
            shutil.copy(abs_content_path, abs_destination)
        elif os.path.isdir(abs_content_path):
            new_dir_name = os.path.join(abs_destination, os.path.basename(abs_content_path))
            copy(abs_content_path, new_dir_name)
        else:
            raise Exception(f"{abs_content_path} is neither file nor directory.")

def clean_public_folder():
    if os.path.exists(PUBLIC_FOLDER):
        try:
            shutil.rmtree(PUBLIC_FOLDER)
        except Exception as e:
            raise Exception(f"Could not remove public folder: {e}")


def write_to_log(logfile, text, overwrite = False):
    mode = "w" if overwrite else "a"
    try:
        with open(logfile, mode) as file:
            file.write(text + "\n")
    except Exception as e:
        raise Exception(f"Error writing to logfile: {e}")

main()