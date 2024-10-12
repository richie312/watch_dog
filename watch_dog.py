import time, os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, PatternMatchingEventHandler
import logging
import psutil

logging.basicConfig(filename='service.log', level=logging.INFO)


def log_process_info():
    pid = os.getpid()
    ppid = os.getppid()
    process = psutil.Process(pid)
    parent_process = psutil.Process(ppid)
    logging.info(f"Current PID: {pid}, Parent PID: {ppid}")
    logging.info(f"Current Process: {process.name()}, Parent Process: {parent_process.name()}")

log_process_info()
logging.info("Starting the Monitoring service...")

class Watcher:

    def __init__(self,DIRECTORY_TO_WATCH, file_type=["*.csv"]):
        self.observer = Observer()
        self.DIRECTORY_TO_WATCH = DIRECTORY_TO_WATCH
        self.file_type = file_type

    def run(self, commands_):
        event_handler = Handler(self.file_type,commands_)
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=False)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
            log_process_info()
            logging.info("Stopping the Monitoring service...")
        self.observer.join()

class Handler(PatternMatchingEventHandler, FileSystemEventHandler):
    def __init__(self, file_format, commands_):
        # setting parameters for 'PatternMatchingEventHandler'
        super(Handler, self).__init__(patterns=file_format, ignore_patterns=["*~"], ignore_directories=True, case_sensitive=True)
        self.commands_ = commands_
    
    def on_any_event(self,event):
        if event.is_directory:
            return None
        elif event.event_type == 'created' or event.event_type == 'modified':
            # Run your Docker container
            log_process_info()
            logging.info(f"Received event - {event.event_type}: {event.src_path}")
            logging.info("running python script to update the html page...")
            subprocess.run(self.commands_)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='directory observer')
    parser.add_argument('--dir', type=str, help='directory path', default='.')
    parser.add_argument('--file_format', type=list, help='file_format, eg: csv, json, xml in list. ["*.csv",".xml"] ', default=["*.csv"])
    parser.add_argument('--commands_', type=list, help='command to execute on events of specific file format ', 
    default=['python', 'C:\\Users\\2307995\\Documents\\DataDrivenCVAutomation\\URI_DataTables\\datatable.py'])
    args = parser.parse_args()
    w = Watcher(args.dir)
    w.run(args.commands_)