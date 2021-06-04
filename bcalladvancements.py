from os import listdir
import json

class BCAdvancement():

    def __init__(self, filename, parent=None):

        self._filename = filename
        self._parent = parent

    def ReadAdvancement(self):
        advfile = open(self._filename,'r')
        criteria = json.load(advfile)
        print(f"Title {criteria['display']['title']}")

class BCAllAdvancements():

    def __init__(self, minecraftdir="/media/local/Minecraft/server", servername="snapshot", worldname="snapshot"):

        self._minecraftdir=minecraftdir
        self._servername=servername
        self._worldname=worldname

    def BuildAdvancementTree(self):
        advancement_dirname = self._minecraftdir+"/"+self._servername+"/"+self._worldname+"/datapacks/bac_advancements"
        for advancementfile in listdir(advancement_dirname+"/data/blazeandcave/advancements/bacap"):
            if(advancementfile!="root.json"):
                adv=BCAdvancement(advancement_dirname+"/data/blazeandcave/advancements/bacap/"+advancementfile)
                adv.ReadAdvancement()

#        bacap = BCAdvancement(advancement_filename+"/bacap/time_to_farm.json")
#        bacap.ReadAdvancement()


def main():

    print("BCAllAdvancements: Unit Testing")
    bcgame = BCAllAdvancements()
    bcgame.BuildAdvancementTree()


if __name__ == '__main__':
    main()