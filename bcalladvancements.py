from os import listdir
from pathlib import Path
from time import sleep
import json

class BCAdvancement():

    ADVANCEMENT_EMPTY = 0
    ADVANCEMENT_ADVENTURE = 1 
    ADVANCEMENT_ANIMAL=2
    ADVANCEMENT_BACAP=3
    ADVANCEMENT_BIOMES=4
    ADVANCEMENT_BUILDING=5
    ADVANCEMENT_CHALLENGES=6
    ADVANCEMENT_ENCHANTING=7
    ADVANCEMENT_END=8
    ADVANCEMENT_FARMING=9
    ADVANCEMENT_MINING=10
    ADVANCEMENT_MONSTERS=11
    ADVANCEMENT_NETHER=12
    ADVANCEMENT_POTION=13
    ADVANCEMENT_REDSTONE=14
    ADVANCEMENT_STATISTICS=15
    ADVANCEMENT_WEAPONRY=16

    REQUIREMENT_ALL = 0
    REQUIREMENT_ANY = 1

    ADVANCEMENT_NOTCOMPLETED = 0
    ADVANCEMENT_COMPLETED = 1

    def __init__(self, name, filename):

        self._name = name
        self._filename = filename
        self._title = ""
        self._parent = ""
        self._criteria = []
        self._finished = []
        self._completed = self.ADVANCEMENT_NOTCOMPLETED
        self._requirement = self.REQUIREMENT_ALL

        self._section = self.ADVANCEMENT_EMPTY
        if(name.startswith("blazeandcave:adventure")):
            self._section = self.ADVANCEMENT_ADVENTURE
        elif(name.startswith("blazeandcave:animal")):
            self._section = self.ADVANCEMENT_ANIMAL
        elif(name.startswith("blazeandcave:bacap")):
            self._section = self.ADVANCEMENT_BACAP
        elif(name.startswith("blazeandcave:biomes")):
            self._section = self.ADVANCEMENT_BIOMES
        elif(name.startswith("blazeandcave:building")):
            self._section = self.ADVANCEMENT_BUILDING
        elif(name.startswith("blazeandcave:challenges")):
            self._section = self.ADVANCEMENT_CHALLENGES
        elif(name.startswith("blazeandcave:enchanting")):
            self._section = self.ADVANCEMENT_ENCHANTING
        elif(name.startswith("blazeandcave:end")):
            self._section = self.ADVANCEMENT_END
        elif(name.startswith("blazeandcave:farming")):
            self._section = self.ADVANCEMENT_FARMING
        elif(name.startswith("blazeandcave:mining")):
            self._section = self.ADVANCEMENT_MINING
        elif(name.startswith("blazeandcave:monsters")):
            self._section = self.ADVANCEMENT_MONSTERS
        elif(name.startswith("blazeandcave:nether")):
            self._section = self.ADVANCEMENT_NETHER
        elif(name.startswith("blazeandcave:potion")):
            self._section = self.ADVANCEMENT_POTION
        elif(name.startswith("blazeandcave:redstone")):
            self._section = self.ADVANCEMENT_REDSTONE
        elif(name.startswith("blazeandcave:statistics")):
            self._section = self.ADVANCEMENT_STATISTICS
        elif(name.startswith("blazeandcave:weaponry")):
            self._section = self.ADVANCEMENT_WEAPONRY

    def ReadAdvancement(self):

        advancement_file = open(self._filename,'r')
        advancement_info = json.load(advancement_file)
        advancement_file.close()

        if 'display' not in advancement_info:
#            print ("No Display")
            pass
        elif 'title' not in advancement_info['display']:
#            print ("No Title")
            pass
        elif 'translate' not in advancement_info['display']['title']:
#            print ("No Translate")
            pass
        else:
            self._title = advancement_info['display']['title']['translate']
 
        if 'parent' not in advancement_info:
#            print ("No Parent")
            pass
        else:
            self._parent = advancement_info['parent']

        if(self._section==self.ADVANCEMENT_EMPTY):
            if(self._parent.startswith("blazeandcave:adventure")):
                self._section = self.ADVANCEMENT_ADVENTURE
            elif(self._parent.startswith("blazeandcave:animal")):
                self._section = self.ADVANCEMENT_ANIMAL
            elif(self._parent.startswith("blazeandcave:bacap")):
                self._section = self.ADVANCEMENT_BACAP
            elif(self._parent.startswith("blazeandcave:biomes")):
                self._section = self.ADVANCEMENT_BIOMES
            elif(self._parent.startswith("blazeandcave:building")):
                self._section = self.ADVANCEMENT_BUILDING
            elif(self._parent.startswith("blazeandcave:challenges")):
                self._section = self.ADVANCEMENT_CHALLENGES
            elif(self._parent.startswith("blazeandcave:enchanting")):
                self._section = self.ADVANCEMENT_ENCHANTING
            elif(self._parent.startswith("blazeandcave:end")):
                self._section = self.ADVANCEMENT_END
            elif(self._parent.startswith("blazeandcave:farming")):
                self._section = self.ADVANCEMENT_FARMING
            elif(self._parent.startswith("blazeandcave:mining")):
                self._section = self.ADVANCEMENT_MINING
            elif(self._parent.startswith("blazeandcave:monsters")):
                self._section = self.ADVANCEMENT_MONSTERS
            elif(self._parent.startswith("blazeandcave:nether")):
                self._section = self.ADVANCEMENT_NETHER
            elif(self._parent.startswith("blazeandcave:potion")):
                self._section = self.ADVANCEMENT_POTION
            elif(self._parent.startswith("blazeandcave:redstone")):
                self._section = self.ADVANCEMENT_REDSTONE
            elif(self._parent.startswith("blazeandcave:statistics")):
                self._section = self.ADVANCEMENT_STATISTICS
            elif(self._parent.startswith("blazeandcave:weaponry")):
                self._section = self.ADVANCEMENT_WEAPONRY

            elif(self._name=="minecraft:adventure/root"):
                self._section = self.ADVANCEMENT_ADVENTURE
            elif(self._name=="minecraft:end/root"):
                self._section = self.ADVANCEMENT_END
            elif(self._name=="minecraft:husbandry/root"):
                self._section = self.ADVANCEMENT_ANIMAL
            elif(self._name=="minecraft:nether/root"):
                self._section = self.ADVANCEMENT_ANIMAL

        if 'criteria'  not in advancement_info:
            print(f"No criteria for {self._name}")
            pass
        else:
            for criteria in advancement_info['criteria']:
                if criteria not in self._criteria:
                    self._criteria.append(criteria)

        if 'requirement'  in advancement_info:
            self._requirement = self.REQUIREMENT_ANY



    def PrintAdvancement(self):
        print(f"Advancement Name:      {self._name}")
        print(f"Advancement Filename:  {self._filename}")
        print(f"Advancement Title:     {self._title}")
        print(f"Advancement Parent:    {self._parent}")

        if(self._requirement==self.REQUIREMENT_ANY):
            print(f"Advancement Required:  ANY")
        else:
            print(f"Advancement Required:  ALL")

        print(f"Advancement Criteria:  ", end='')
        print(f"({len(self._criteria)}) ", end='')
        for criteria in self._criteria:
            print(f"{criteria} ", end='')
        print()

        print(f"Advancement Finished:  ", end='')
        print(f"({len(self._finished)}) ", end='')
        for criteria in self._finished:
            print(f"{criteria} ", end='')
        print()

        if(self._completed==self.ADVANCEMENT_COMPLETED):
            print(f"Advancement Completed: TRUE")
        else:
            print(f"Advancement Completed: FALSE")

class BCAllAdvancements():

    def __init__(self, minecraftdir="/media/local/Minecraft/server", servername="snapshot", worldname="snapshot"):

        self._minecraftdir=minecraftdir
        self._servername=servername
        self._worldname=worldname

        self._bacadvancement_dirname=""
        self._standardadvancement_dirname=""
        self._lastupdatetime=0

        self._advancements={}

        self._adventure_advancements={}
        self._animal_advancements={}
        self._bacap_advancements={}
        self._biomes_advancements={}

        self._building_advancements={}
        self._challenges_advancements={}
        self._enchanting_advancements={}
        self._end_advancements={}

        self._farming_advancements={}
        self._mining_advancements={}
        self._monsters_advancements={}
        self._nether_advancements={}

        self._potion_advancements={}
        self._redstone_advancements={}
        self._statistics_advancements={}
        self._weaponry_advancements={}

        self.BuildAllAdvancements()
        self.SortAllAdvancements()


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
        self._useradvancements_dirname = self._minecraftdir+"/"+self._servername+"/"+self._worldname+"/advancements"
        self._useradvancements_filename = self._useradvancements_dirname + "/0204da8b-0edd-47ad-8890-ac5ee611b575.json"

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

    def ParentSection(self,advancement):
        if self._advancements[advancement]._section != BCAdvancement.ADVANCEMENT_EMPTY:
            return self._advancements[advancement]._section
        else:
            parent = self._advancements[advancement]._parent
            if parent in self._advancements:
                return self.ParentSection(parent)
        return BCAdvancement.ADVANCEMENT_EMPTY

    def SortAllAdvancements(self):
        for advancement in self._advancements:
            if self._advancements[advancement]._section == BCAdvancement.ADVANCEMENT_EMPTY:
                self._advancements[advancement]._section = self.ParentSection(advancement)

            if self._advancements[advancement]._section == BCAdvancement.ADVANCEMENT_ADVENTURE:
                if advancement not in self._adventure_advancements:
                    self._adventure_advancements[advancement] = self._advancements[advancement]
            elif self._advancements[advancement]._section == BCAdvancement.ADVANCEMENT_ANIMAL:
                if advancement not in self._animal_advancements:
                    self._animal_advancements[advancement] = self._advancements[advancement]
            elif self._advancements[advancement]._section == BCAdvancement.ADVANCEMENT_BACAP:
                if advancement not in self._bacap_advancements:
                    self._bacap_advancements[advancement] = self._advancements[advancement]
            elif self._advancements[advancement]._section == BCAdvancement.ADVANCEMENT_BIOMES:
                if advancement not in self._biomes_advancements:
                    self._biomes_advancements[advancement] = self._advancements[advancement]

            elif self._advancements[advancement]._section == BCAdvancement.ADVANCEMENT_BUILDING:
                if advancement not in self._building_advancements:
                    self._building_advancements[advancement] = self._advancements[advancement]
            elif self._advancements[advancement]._section == BCAdvancement.ADVANCEMENT_CHALLENGES:
                if advancement not in self._challenges_advancements:
                    self._challenges_advancements[advancement] = self._advancements[advancement]
            elif self._advancements[advancement]._section == BCAdvancement.ADVANCEMENT_ENCHANTING:
                if advancement not in self._enchanting_advancements:
                    self._enchanting_advancements[advancement] = self._advancements[advancement]
            elif self._advancements[advancement]._section == BCAdvancement.ADVANCEMENT_END:
                if advancement not in self._end_advancements:
                    self._end_advancements[advancement] = self._advancements[advancement]

            elif self._advancements[advancement]._section == BCAdvancement.ADVANCEMENT_FARMING:
                if advancement not in self._farming_advancements:
                    self._farming_advancements[advancement] = self._advancements[advancement]
            elif self._advancements[advancement]._section == BCAdvancement.ADVANCEMENT_MINING:
                if advancement not in self._mining_advancements:
                    self._mining_advancements[advancement] = self._advancements[advancement]
            elif self._advancements[advancement]._section == BCAdvancement.ADVANCEMENT_MONSTERS:
                if advancement not in self._monsters_advancements:
                    self._monsters_advancements[advancement] = self._advancements[advancement]
            elif self._advancements[advancement]._section == BCAdvancement.ADVANCEMENT_NETHER:
                if advancement not in self._nether_advancements:
                    self._nether_advancements[advancement] = self._advancements[advancement]

            elif self._advancements[advancement]._section == BCAdvancement.ADVANCEMENT_POTION:
                if advancement not in self._potion_advancements:
                    self._potion_advancements[advancement] = self._advancements[advancement]
            elif self._advancements[advancement]._section == BCAdvancement.ADVANCEMENT_REDSTONE:
                if advancement not in self._redstone_advancements:
                    self._redstone_advancements[advancement] = self._advancements[advancement]
            elif self._advancements[advancement]._section == BCAdvancement.ADVANCEMENT_STATISTICS:
                if advancement not in self._statistics_advancements:
                    self._statistics_advancements[advancement] = self._advancements[advancement]
            elif self._advancements[advancement]._section == BCAdvancement.ADVANCEMENT_WEAPONRY:
                if advancement not in self._weaponry_advancements:
                    self._weaponry_advancements[advancement] = self._advancements[advancement]


    def UpdateAdvancements(self):

        useradvancement_filepath = Path(self._useradvancements_filename)
        if useradvancement_filepath.exists() and self._lastupdatetime != useradvancement_filepath.stat().st_mtime:
        # file has changed so lets save the previous results
            self._lastupdatetime = useradvancement_filepath.stat().st_mtime
            advancement_file = useradvancement_filepath.open('r')
            completed_info = json.load(advancement_file)
            advancement_file.close()

            for i in completed_info:
                if not i.startswith("minecraft:recipes") and not i == "DataVersion":
                    if i in self._advancements:
                        if 'done' in completed_info[i] and completed_info[i]['done'] == True:
                            self._advancements[i]._completed = BCAdvancement.ADVANCEMENT_COMPLETED
                        if 'criteria' in completed_info[i]:
                            for criteria in completed_info[i]['criteria']:
                                if criteria not in self._advancements[i]._finished:
                                    self._advancements[i]._finished.append(criteria)


    def GetMilestone(self,name):
        total_advancements = total_advancements_completed = 0
        if name in self._advancements:
            total_advancements = len(self._advancements[name]._criteria)
            total_advancements_completed = len(self._advancements[name]._finished)
        milestone = f"{total_advancements_completed:3}({total_advancements:3})"
        return milestone


    def PrintMilestone(self, title, name, num ):

        total_advancements = total_advancements_completed = 0
        if name in self._advancements:
            total_advancements = len(self._advancements[name]._criteria)
            total_advancements_completed = len(self._advancements[name]._finished)
        print(f"{title} {total_advancements_completed:3} out of {total_advancements:3} ({num})")

    def PrintAllAdvancements(self):

        self.PrintMilestone("Total Advancements:            ","blazeandcave:bacap/advancement_legend",len(self._advancements))
        print()

#        print(f"Total Adventure Advancements: {len(self._adventure_advancements)}")
#        print(f"Total Animal Advancements: {len(self._animal_advancements)}")
#        print(f"Total Bacap Advancements: {len(self._bacap_advancements)}")
#        print(f"Total Biomes Advancements: {len(self._biomes_advancements)}")

#        print(f"Total Building Advancements: {len(self._building_advancements)}")
#        print(f"Total Challenges Advancements: {len(self._challenges_advancements)}")
#        print(f"Total Enchanting Advancements: {len(self._enchanting_advancements)}")
#        print(f"Total End Advancements: {len(self._end_advancements)}")

#        print(f"Total Farming Advancements: {len(self._farming_advancements)}")
#        print(f"Total Mining Advancements: {len(self._mining_advancements)}")
#        print(f"Total Monsters Advancements: {len(self._monsters_advancements)}")
#        print(f"Total Nether Advancements: {len(self._nether_advancements)}")

#        print(f"Total Potion Advancements: {len(self._potion_advancements)}")
#        print(f"Total Redstone Advancements: {len(self._redstone_advancements)}")
#        print(f"Total Statistics Advancements: {len(self._statistics_advancements)}")
#        print(f"Total Weaponry Advancements: {len(self._weaponry_advancements)}")

        self.PrintMilestone("Total Mining Advancements:     ","blazeandcave:bacap/mining_milestone",len(self._mining_advancements))
        self.PrintMilestone("Total Building Advancements:   ","blazeandcave:bacap/building_milestone",len(self._building_advancements))
        self.PrintMilestone("Total Farming Advancements:    ","blazeandcave:bacap/farming_milestone",len(self._farming_advancements))
        self.PrintMilestone("Total Animal Advancements:     ","blazeandcave:bacap/animal_milestone",len(self._animal_advancements))

        self.PrintMilestone("Total Monsters Advancements:   ","blazeandcave:bacap/monsters_milestone",len(self._monsters_advancements))
        self.PrintMilestone("Total Weaponry Advancements:   ","blazeandcave:bacap/weaponry_milestone",len(self._weaponry_advancements))
        self.PrintMilestone("Total Biomes Advancements:     ","blazeandcave:bacap/biomes_milestone",len(self._biomes_advancements))
        self.PrintMilestone("Total Adventure Advancements:  ","blazeandcave:bacap/adventure_milestone",len(self._adventure_advancements))

        self.PrintMilestone("Total Redstone Advancements:   ","blazeandcave:bacap/redstone_milestone",len(self._redstone_advancements))
        self.PrintMilestone("Total Enchanting Advancements: ","blazeandcave:bacap/enchanting_milestone",len(self._enchanting_advancements))
        self.PrintMilestone("Total Statistics Advancements: ","blazeandcave:bacap/statistics_milestone",len(self._statistics_advancements))
        self.PrintMilestone("Total Nether Advancements:     ","blazeandcave:bacap/nether_milestone",len(self._nether_advancements))

        self.PrintMilestone("Total Potion Advancements:     ","blazeandcave:bacap/potion_milestone",len(self._potion_advancements))
        self.PrintMilestone("Total End Advancements:        ","blazeandcave:bacap/end_milestone",len(self._end_advancements))
        self.PrintMilestone("Total Challenges Advancements: ","blazeandcave:bacap/challenges_milestone",len(self._challenges_advancements))

#        i=1
#        for advancement in sorted(self._building_advancements):
#            print(f"{i}:{advancement}\t\t{self._building_advancements[advancement]._parent}")
#            i+=1
            

#        i=1
#        for advancement in sorted(self._advancements):
#            if self._advancements[advancement]._section == BCAdvancement.ADVANCEMENT_EMPTY:
#                print(f"{i}:{advancement}\t\t\t{self._advancements[advancement]._parent}")
#                i+=1



def main():

    print("BCAllAdvancements: Unit Testing")
    bcgame = BCAllAdvancements()

    bcgame.UpdateAdvancements()
    bcgame.PrintAllAdvancements()
    bcgame._advancements["blazeandcave:bacap/advancement_legend"].PrintAdvancement()
    
    while True:
        sleep(2)
        print()
        bcgame.UpdateAdvancements()
        bcgame.PrintAllAdvancements()
        bcgame._advancements["blazeandcave:bacap/advancement_legend"].PrintAdvancement()

if __name__ == '__main__':
    main()