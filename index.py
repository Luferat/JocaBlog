import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from subprocess import Popen, PIPE, call

appfile = 'app.py'


class MyHandler(FileSystemEventHandler):
    def __init__(self, process):
        self.process = process

    def on_modified(self, event):
        if event.src_path.endswith(appfile):
            print("Arquivo modificado, reiniciando o servidor...")
            self.process.terminate()
            self.process = Popen(['python', appfile], stdout=PIPE, stderr=PIPE)
            stdout, stderr = self.process.communicate()
            print(stdout.decode())
            print(stderr.decode())


if __name__ == '__main__':
    print("Iniciando o servidor...")
    process = Popen(['python', appfile], stdout=PIPE, stderr=PIPE)

    event_handler = MyHandler(process)
    observer = Observer()
    observer.schedule(event_handler, path='./', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        process.terminate()
    observer.join()
