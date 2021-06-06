from os import listdir
import json

class BCAdvancement():

    def __init__(self, name, filename):
        self._name = name
        self._filename = filename
        self._title = ""
        self._parent = ""

    def ReadAdvancement(self):
        advancement_file = open(self._filename,'r')
        advancement_info = json.load(advancement_file)
        if 'display' not in advancement_info:
            print ("No Display")
        elif 'title' not in advancement_info['display']:
            print ("No Title")
        elif 'translate' not in advancement_info['display']['title']:
            print ("No Translate")
        else:
            self._title = advancement_info['display']['title']['translate']
        if 'parent' not in advancement_info:
            print ("No Parent")
        else:
            self._parent = advancement_info['parent']
        
class BCAllAdvancements():

    def __init__(self, minecraftdir="/media/local/Minecraft/server", servername="snapshot", worldname="snapshot"):

        self._minecraftdir=minecraftdir
        self._servername=servername
        self._worldname=worldname

        self._bacadvancement_dirname=""
        self._standardadvancement_dirname=""

        self._advancements={}

        self._adventure_advancements={}
        self._animal_advancements={}
        self._bacap_advancements={}
        self._mining_advancements={}

    def BuildAdvancements(self, type, name, dirname):
        advancement_dir = dirname + "/" + name
        for advancement_file in listdir(advancement_dir):
            advancement_name = type+":"+name+"/"+advancement_file.rsplit(".",1)[0]
            if advancement_name not in self._advancements:
                self._advancements[advancement_name] = BCAdvancement(advancement_name, advancement_dir+"/"+advancement_file)
            advancement: BCAdvancement = self._advancements[advancement_name]
            advancement.ReadAdvancement()

    def BuildBACAdvancements(self, name):
        self.BuildAdvancements("blazeandcave",name,self._bacadvancement_dirname)

    def BuildStandardAdvancements(self, name):
        self.BuildAdvancements("minecraft",name,self._standardadvancement_dirname)

    def BuildAllAdvancements(self):
        self._bac_dirname = self._minecraftdir+"/"+self._servername+"/"+self._worldname+"/datapacks/bac_advancements"
        self._bacadvancement_dirname = self._bac_dirname + "/data/blazeandcave/advancements"
        self._standardadvancement_dirname = self._bac_dirname + "/data/minecraft/advancements"

        self.BuildBACAdvancements("adventure")
        self.BuildBACAdvancements("animal")
        self.BuildBACAdvancements("bacap")
        self.BuildBACAdvancements("biomes")

        self.BuildBACAdvancements("building")
        self.BuildBACAdvancements("challenges")
        self.BuildBACAdvancements("enchanting")
        self.BuildBACAdvancements("end")

        self.BuildBACAdvancements("farming")
        self.BuildBACAdvancements("mining")
        self.BuildBACAdvancements("monsters")
        self.BuildBACAdvancements("nether")

        self.BuildBACAdvancements("potion")
        self.BuildBACAdvancements("redstone")
        self.BuildBACAdvancements("statistics")
        self.BuildBACAdvancements("weaponry")

        self.BuildStandardAdvancements("adventure")
        self.BuildStandardAdvancements("end")
        self.BuildStandardAdvancements("husbandry")
        self.BuildStandardAdvancements("nether")
        self.BuildStandardAdvancements("story")

    def SortAllAdvancements(self):
        for advancement in self._advancements:

            if(advancement.startswith("blazeandcave:adventure") or\
                (advancement.startswith("minecraft") and\
                self._advancements[advancement]._parent.startswith("blazeandcave:adventure"))):
                if advancement not in self._adventure_advancements:
                    self._adventure_advancements[advancement] = self._advancements[advancement]

            if(advancement.startswith("minecraft:adventure/summon") or\
                advancement.startswith("minecraft:adventure/root")):
                if advancement not in self._adventure_advancements:
                    self._adventure_advancements[advancement] = self._advancements[advancement]

            if(advancement.startswith("blazeandcave:bacap") or \
                self._advancements[advancement]._parent.startswith("blazeandcave:bacap")):
                if advancement not in self._bacap_advancements:
                    self._bacap_advancements[advancement] = self._advancements[advancement]


    def PrintAllAdvancements(self):

        print(f"Total Advancements: {len(self._advancements)}")
        print(f"Total Adventure Advancements: {len(self._adventure_advancements)}")
        print(f"Total Bacap Advancements: {len(self._bacap_advancements)}")

        i=1
        for advancement in sorted(self._adventure_advancements):
            print(f"{i}:{advancement}")
            i+=1



def main():

    print("BCAllAdvancements: Unit Testing")
    bcgame = BCAllAdvancements()
    bcgame.BuildAllAdvancements()
    bcgame.SortAllAdvancements()
    bcgame.PrintAllAdvancements()


if __name__ == '__main__':
    main()