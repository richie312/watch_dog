import win32serviceutil
import win32service
import win32event
import servicemanager
import os
import sys
import time
import logging

logging.basicConfig(filename='service.log', level=logging.INFO)

class WatchDogService(win32serviceutil.ServiceFramework):
    _svc_name_ = "Important Urls WatchDogService"
    _svc_display_name_ = "Important Urls Data Folder Monitoring"
    _svc_description_ = "Service to run watch_dog.py script"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.running = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.running = False

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        logging.info('WatchDogService started')
        self.main()

    def main(self):
        while self.running:
            logging.info('Running watch_dog.py')
            os.system("python watch_dog.py --dir C:\\Users\\2307995\\Documents\\DataDrivenCVAutomation\\URI_DataTables\\data")
            time.sleep(5)  # Run every 60 seconds

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(WatchDogService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(WatchDogService)