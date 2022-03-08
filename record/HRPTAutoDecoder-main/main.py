import json
import logging
import subprocess

from os.path import exists, join
from os import listdir, mkdir, chdir, remove, stat
from pprint import pformat
from shutil import rmtree
from sys import platform
from time import sleep
from queue import Queue
from datetime import datetime

from threading import Thread

__version__ = "1.0.1"



# dataPath="/mnt/files/iq/test/data", satDumpPath="/mnt/files/iq/test/satdump/build"
config = {
    "satDumpPath": "satDump",
    "dataPath": "data",
    
    "FENGYUN 3B":{"pipeline": "fengyun3_ab_ahrpt", "samplerate": "6000000"},
    "FENGYUN 3C":{"pipeline": "fengyun3_c_ahrpt", "samplerate": "6000000"},

    "METOP-B":{"pipeline": "metop_ahrpt", "samplerate": "6000000"},
    "METOP-C":{"pipeline": "metop_ahrpt", "samplerate": "6000000"},

    "NOAA 18":{"pipeline": "noaa_hrpt", "samplerate": "6000000"},
    "NOAA 19":{"pipeline": "noaa_hrpt", "samplerate": "6000000"},

    "METEOR-M2":{"pipeline": "meteor_hrpt", "samplerate": "6000000"},
    "METEOR-M2 2":{"pipeline": "meteor_hrpt", "samplerate": "6000000"},
    
    "bf": "f32",
    "keepBadIQ": False
}

class AutoDecoder:
    """
    A class that monitors and automatically decodes satellite images
    """
    def __init__(self, dataPath="", satDumpPath="", configPath="", logPath="*", checkDirInterval=1) -> None:
        self.dataPath = dataPath
        self.satDumpPath = satDumpPath
        self.decodeQueue = Queue()
        self.detectedFiles = []
        self.checkDirInterval = checkDirInterval
        self.configPath = configPath
        self.__version__ = __version__

        if logPath == "*":
            file_log = logging.FileHandler(join(__file__, "..", "decoder.log"))
        else:
            if exists(logPath):
                file_log = logging.FileHandler(join(logPath, "decoder.log"))
            else:
                print("logPath is not exists")
                raise SystemExit(1)

        console_out = logging.StreamHandler()
        logging.basicConfig(format="[%(asctime)s]  [%(levelname)s]: %(message)s", datefmt='%m/%d/%Y - %H:%M:%S', handlers=(file_log, console_out), level=logging.INFO)
        
        self.logger = logging.getLogger()

        # config check
        path = join(self.configPath, "config.json")
        if exists(path):
            with open(path) as file:
                self.config = json.load(file)

            if config.keys() == self.config.keys():
                self.logger.info(f"Config loaded from {path}")
                
            else:
                self.config = config
                self.logger.warning(f"Incorrect config in {path}")
                self.logger.info("Load default config")

                with open("config.json", 'w') as f:
                    f.write(json.dumps(config, indent=1))
        else:
            self.config = config
            self.logger.warning(f"Incorrect config in {path}")
            self.logger.info("Load default config")
            with open("config.json", 'w') as f:
                f.write(json.dumps(config, indent=4))

        if self.dataPath == "":
            self.dataPath = self.config["dataPath"] 
        if self.satDumpPath == "":
            self.satDumpPath = self.config["satDumpPath"]

        if not (exists(self.dataPath) or exists(self.satDumpPath)):
            logging.critical("Data or satDump folder is not exists")
            raise SystemExit(1)

        # Platform check
        if platform == "linux":
            self.executableFile = "satdump"
        elif platform == "win32":
            self.executableFile = "satdump.exe"
        else:
            logging.critical("The platform has not been identified. Exit")
            raise SystemExit(1)

        if not exists(join(self.satDumpPath, self.executableFile)):
            logging.critical("satDump executable file is not found. Exit")
            raise SystemExit(1)

        # Tracking already decoded files
        if not exists(join(self.dataPath, "decoded")):
            mkdir(join(self.dataPath, "decoded"))
            logging.warning("Created 'decoded' dir")
        else:
            self.detectedFiles += [i + ".iq" for i in listdir( join(self.dataPath, "decoded") ) if i[16:] in config.keys()]
        

    def checkDir(self) -> None:
        while self.work:
            try:
                # if If the file is .iq, it has not been decoded before and is not being written to the file now
                files = [i for i in listdir(self.dataPath) if (".iq" in i) and (i not in self.detectedFiles)]
                for file in files:
                    t =  stat(join(self.dataPath, file))

                    # if the file was modified earlier than 20 minutes ago
                    if (datetime.now() - datetime.fromtimestamp(t.st_mtime)).total_seconds() < 1200:
                        sleep(1)
                        # Check if there is no writing to the file now
                        # In linux, start.st_size changes as new data is written
                        # windows Explorer immediately allocates full space for the file being written,
                        # so only stat.st_mtime changes - the time of the last modification (Once per second)
                        if t != stat(join(self.dataPath, file)):
                            files.remove(file)
                            continue 

                    # Checking the write availability of the file
                    try:
                        open(file, 'w').close()
                    except IOError:
                        files.remove(file)
                        continue

                    if file.split(".")[0][16:] in config.keys():
                        logging.info(f"Found new file: '{file}'")
                        self.detectedFiles.append(file)
                        self.decodeQueue.put(file)

            except Exception as e:
                logging.error(f"Error at the time check dir: {str(e)}")
                
            sleep(self.checkDirInterval + .1)


    
    def decode(self) -> None:
        chdir(self.satDumpPath)
        while self.work:
            try:
                if self.decodeQueue.empty():
                    sleep(.1)
                    continue

                file = self.decodeQueue.get()
                satellite = file.split(".")[0][16:]

                output = join(self.dataPath, "decoded", file.split('.')[0])

                if not exists(output):
                    mkdir(output)
                    
                logging.info(f"Decode '{file}' is started")
                command = f'"{join(self.satDumpPath, self.executableFile)}" {config[satellite]["pipeline"]} baseband "{join(self.dataPath, file)}" products "{output}" -samplerate {config[satellite]["samplerate"]} -baseband_format {self.basebandFormat}'
                logging.info("Command:\n" + command)

                # Start satDump decode
                sleep(self.checkDirInterval)
                with subprocess.Popen(command, shell=True, stderr=subprocess.PIPE) as process:
                    code = process.wait()
                    _, stderrdata = process.communicate()

                    if stderrdata is None:
                        logging.error(f"'{file}' Decoding error")
                    else:  
                        for f in listdir(output):
                            # (MetOp and Fengyoun and Meteor) or Noaa
                            fileSize = stat(join(output, f)).st_size
                            if (f.endswith(".cadu") and (fileSize < 1024000)) or (f.endswith(".aip") and (fileSize < 10240)):
                                logging.warning(f"No data for {file}")
                                rmtree(output)

                                if not self.config["keepBadIQ"]:
                                    remove(join(self.dataPath, file))

                                break
                        else:
                            logging.info(f"'{file}' Decoding successfull")  
                            
            except Exception as e:
                self.work = 0
                logging.critical(f"Error: {e} in self.Decode")
                raise SystemExit(1)
                
            sleep(.01)

    
    def run(self) -> None:
        logging.info(f"Decoder {__version__} started")
        
        self.basebandFormat = self.config["bf"]
        
        self.logger.info("Config:\n" + pformat(self.config, width=120, compact=True, sort_dicts=False))

        self.checkDirThread = Thread(target=self.checkDir)
        self.decodeThread = Thread(target=self.decode)

        self.work = True

        self.checkDirThread.start()
        self.decodeThread.start()
    

    def stop(self) -> None:
        self.work = False
        logging.info("Decoder was turned off\n\n")

        
        
if __name__ == "__main__":
    decoder = AutoDecoder()
    decoder.run()