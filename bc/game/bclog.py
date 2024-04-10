#!/usr/bin/env python3
from pathlib import Path
class BCLog():

    def __init__(self, minecraftdir="/media/local/Minecraft", servername="fury"):

        self._minecraftdir = minecraftdir
        self._servername = servername
        self._seed = None
        
        self._bclog_file = None
        self._game_time = 0
        self._current_bclog_event = 0

    def bclog_filename(self):
        result = ""
        if(self._seed is not None):
            result = self._minecraftdir+"/bclogs/"+self._servername+"_"+self._seed+".log"
        return(result)

    def bclog_symlink(self):
        if(self._seed is not None):
            link = Path(self._minecraftdir+"/bclogs/latest_"+self._servername+".log")
            if(link.is_symlink()):
                link.unlink()
            link.symlink_to(self.bclog_filename())

    def read_existing_bclog(self, bclogpath):
        filehandle = open(bclogpath)
        for line in filehandle:
            if "LevelUpdate:" in line:
                self._game_time = int(line.split(',')[0].split()[-1])
            if "LogEvent:" in line:
                self._current_bclog_event = int(line.split(',')[0].split()[-1])

        filehandle.close()

    def close(self):
        if(self._bclog_file):
            self._bclog_file.close()


    def open(self, seed):

        if(self._bclog_file and seed is self._seed):
            return()

        if(self._bclog_file and seed is not self._seed):
            self._bclog_file.close()
            self._bclog_file = None

        if(seed is None):
            self._seed = None
        else:
            self._seed = seed
            self._game_time = 0
            self._current_bclog_event = 0
            bclog_path = Path(self.bclog_filename())
            if(bclog_path.exists()):
                self.read_existing_bclog(bclog_path)
            self._bclog_file = open(self.bclog_filename(),'a')
            self.bclog_symlink()

    def bclog_results(self):
        pass
#        if self._seed != levelfile.seed():
#            self.open(levelfile.seed())
#        if self._current_bclog_event < logfiles.num_log_events() and self._outfile:
#            while self._current_bclog_event < logfiles.num_log_events():
#                self._outfile.write(f"{logfiles.get_log_event(self._currentlogevent)}\n")
#                self._currentlogevent=self._currentlogevent+1
#            self._outfile.flush()
#        if self._gametime != levelfile.game_time() and self._outfile:
#            self._outfile.write(f"{datetime.fromtimestamp(levelfile.level_file_last_update()).strftime('%Y-%m-%d %H:%M:%S')}")
#            self._outfile.write(f" LevelUpdate: ")
#            self._outfile.write(f"{levelfile.game_time()},")
#            self._outfile.write(f"{levelfile.day_time()},")
#            self._outfile.write(f"{levelfile.clear_weather_time()},")
#            self._outfile.write(f"{levelfile.raining()},")
#            self._outfile.write(f"{levelfile.rain_time()},")
#            self._outfile.write(f"{levelfile.thundering()},")
#            self._outfile.write(f"{levelfile.thunder_time()},")
#            self._outfile.write(f"{levelfile.wandering_trader_spawn_delay()},")
#            self._outfile.write(f"{levelfile.wandering_trader_spawn_chance()},")
#            self._outfile.write(f"{levelfile.wandering_trader_id()}\n")
#            self._outfile.flush()
#            self._gametime = levelfile.game_time()

    def flush(self):
        if(self._bclog_file):
            self._bclog_file.flush()

def main():
    print("BCLog: Unit Testing")
    bclog = BCLog()

if __name__ == '__main__':
    main()