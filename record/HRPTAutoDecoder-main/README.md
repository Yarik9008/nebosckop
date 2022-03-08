# HRPTAutoDecoder
Powered by MrFentazis


The application is designed to be used in conjunction with stations receiving meteorological satellite data in the L band. Checking the directory where the file with IQ data is expected to appear, it also checks whether the found file is being recorded right now. If the file is available, the decoding/demodulation process based on SatDump is started.
The default log of the application is saved in decoder.log next to main.py

List of satellites supported by default:
- 🛰 NOAA 18/19 🛰`
- 🛰 METOP-B/C 🛰
- 🛰 METEOR-M 2 🛰
- 🛰 METEOR-M2 2 🛰
- 🛰 FENGYUN 3B/C 🛰

If necessary, you can add others by specifying the parameters for processing in SatDump in the configuration file.
```python
"FENGYUN 3C": {
  "pipeline": "fengyun3_c_ahrpt",
  "samplerate": "6000000"
 },
 ```
## Technology stack

The list of dependencies is very short:

- [Python](https://www.python.org/) - main programming language Python 3.7 and newer 
- [SatDump](https://github.com/altillimity/SatDump) - A generic satellite data processing software

Python 3.7 is caused by the use of string interpolation (f-string). If desired , you can replace them with formatting via % or .format and the application can be run on almost any version of python..

## Installation and Configuration

Before using it, you need to install SatDump, according to the author's instructions for your system.

`Linux` and `Windows` are fully supported. `MAC OS` is not supported, because I have no equipment on this operating system and it is not possible to test it. To enable support for other operating systems, you will need to make sure that SatDump is working correctly and add a clarification for the SatDump executable file to the AutoDecoder.__init__:
```python
class AutoDecoder:
    """
    A class that monitors and automatically decodes satellite images
    """
    def __init__(self, dataPath="", satDumpPath="", configPath="", logPath="*", checkDirInterval=1) -> None:
        ...
        # Platform check
        if platform == "linux":
            self.executableFile = "satdump"
        elif platform == "win32":
            self.executableFile = "satdump.exe"
        elif platform == "...":
            self.executableFile = "..."
```
The correct name of your operating system for python.sys you can see it [here](https://stackoverflow.com/questions/446209/possible-values-from-sys-platform).

Then you can proceed with the installation:
```sh
git clone https://gitlab.com/lpmrfentazis/HRPTAutoDecoder.git
cd HRPTAutoDecoder
python main.py
```
By default, the application expects that the folder with satellite data and satDump are located next to main.py and are called `data` and `SatDump` respectively.

If necessary, this can be changed in config.json:
```python
 "satDumpPath": "/mnt/files/iq/test/satdump/build",
 "dataPath": "/mnt/files/iq/test/data",
```
You can specify both a relative and an absolute path.

It is also important to specify the data type that is used in the .iq file, by default it is f32 (float 32 bit):
```python
"bf": "f32",
```
P.S. Decoded files are saved in <data path>/decoded, each iq file is supplied with a folder with decoded data with the same name. In a situation where no images were received after decoding, the folder is deleted, as is the empty iq itself (you can enable the keepBadIQ parameter)
```python
"keepBadIQ": true
```

## Use as a module
The class constructor accepts the following parameters:
```python
class AutoDecoder:
    """
    A class that monitors and automatically decodes satellite images
    """
    def __init__(self, dataPath="", satDumpPath="", configPath="", logPath="*", checkDirInterval=1) -> None:
        ...
```
- dataPath - Path to the satellite data folder
- satDumpPath - Path to the folder with the satDump executable file
- configPath - Path to the folder with the config.json configuration file
- logPath - Path to the folder with the log file (set * to write next to main.py and distinguish the path to CWD)
- checkDirInterval - Interval for checking the data folder (It is impossible to set less than 0.1, 0.1 is added to the specified value in the code)

The latter was done to avoid a situation where the check cycle takes up 100% of the processor core.

#### Usage example:
```python
if __name__ == "__main__":
    decoder = AutoDecoder(satDumpPath="C:\\Lorett_lband\\satDump", dataPath="D:\\data")
    decoder.run()
```



