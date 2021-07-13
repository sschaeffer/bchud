#!/usr/bin/env python3

from bclevelfile import BCLevelFile
from bclogfiles import BCLogFiles

from pathlib import Path
from datetime import datetime


class BCLog():

    def __init__(self, minecraftdir="/media/local/Minecraft/server", servername="snapshot"):

        self._minecraftdir = minecraftdir
        self._servername = servername
        self._seed = None
        
        self._outfile = None
        self._gametime = 0
        self._currentlogevent = 0

    def bclog_filename(self):
        result = ""
        if(self._seed is not None):
            result = self._minecraftdir+"/bclogs/"+self._servername+"_"+self._seed
        return(result)

    def bclog_symlink(self):
        if(self._seed is not None):
            link = Path(self._minecraftdir+"/bclogs/latest_"+self._servername)
            if(link.is_symlink()):
                link.unlink()
            link.symlink_to(self.bclog_filename())

    def read_existing_log(self, bclogpath):
        filehandle = open(bclogpath)
        for line in filehandle:
            if "LevelUpdate:" in line:
                self._gametime = int(line.split(',')[0].split()[-1])
            if "LogEvent:" in line:
                self._currentlogevent = int(line.split(',')[0].split()[-1])

        filehandle.close()

    def close(self):
        if(self._outfile):
            self._outfile.close()


    def open(self, seed):

        if(self._outfile and seed is self._seed):
#            print("Seed is the same and the file is already open")
            return()

        if(self._outfile and seed is not self._seed):
#            print(f"Closing file and opening with new seed {seed}:{self._seed}")
            self._outfile.close()
            self._outfile = None

        if(seed is None):
#            print("Seed is blank")
            self._seed = None
        else:
#            print(f"Opening new file with seed: {seed}")
            self._seed = seed
            self._gametime = 0
            self._currentlogevent = 0
            bclogpath = Path(self.bclog_filename())
            if(bclogpath.exists()):
                self.read_existing_log(bclogpath)
            self._outfile = open(self.bclog_filename(),'a')
            self.bclog_symlink()

    def log_results(self, levelfile: BCLevelFile, logfiles: BCLogFiles):
        if self._seed != levelfile.seed():
            self.open(levelfile.seed())
        if self._currentlogevent < logfiles.num_log_events() and self._outfile:
            while self._currentlogevent < logfiles.num_log_events():
                self._outfile.write(f"{logfiles.get_log_event(self._currentlogevent)}\n")
                self._currentlogevent=self._currentlogevent+1
            self._outfile.flush()
        if self._gametime != levelfile.game_time() and self._outfile:
            self._outfile.write(f"{datetime.fromtimestamp(levelfile.level_file_last_update()).strftime('%Y-%m-%d %H:%M:%S')}")
            self._outfile.write(f" LevelUpdate: ")
            self._outfile.write(f"{levelfile.game_time()},")
            self._outfile.write(f"{levelfile.day_time()},")
            self._outfile.write(f"{levelfile.clear_weather_time()},")
            self._outfile.write(f"{levelfile.raining()},")
            self._outfile.write(f"{levelfile.rain_time()},")
            self._outfile.write(f"{levelfile.thundering()},")
            self._outfile.write(f"{levelfile.thunder_time()},")
            self._outfile.write(f"{levelfile.wandering_trader_spawn_delay()},")
            self._outfile.write(f"{levelfile.wandering_trader_spawn_chance()},")
            self._outfile.write(f"{levelfile.wandering_trader_id()}\n")
            self._outfile.flush()
            self._gametime = levelfile.game_time()

    def flush(self):
        if(self._outfile):
            self._outfile.flush()

def main():
    print("BCLog: Unit Testing")
    bclog = BCLog()

if __name__ == '__main__':
    main()