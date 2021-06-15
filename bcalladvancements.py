#!/usr/bin/env python3

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
                self._section = self.ADVANCEMENT_NETHER

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

    BACAP_LIST=["blazeandcave:bacap/root",\
                "blazeandcave:bacap/getting_wood",\
                "minecraft:story/root",\
                "blazeandcave:bacap/time_to_mine",\
                "blazeandcave:bacap/time_to_strike",\
                "blazeandcave:bacap/time_to_chop",\
                "blazeandcave:bacap/time_to_dig",\
                "blazeandcave:bacap/time_to_farm",\
                "blazeandcave:bacap/mining_milestone",\
                "blazeandcave:bacap/building_milestone",\
                "blazeandcave:bacap/farming_milestone",\
                "blazeandcave:bacap/animal_milestone",\
                "blazeandcave:bacap/monsters_milestone",\
                "blazeandcave:bacap/weaponry_milestone",\
                "blazeandcave:bacap/biomes_milestone",\
                "blazeandcave:bacap/adventure_milestone",\
                "blazeandcave:bacap/redstone_milestone",\
                "blazeandcave:bacap/enchanting_milestone",\
                "blazeandcave:bacap/statistics_milestone",\
                "blazeandcave:bacap/nether_milestone",\
                "blazeandcave:bacap/potion_milestone",\
                "blazeandcave:bacap/end_milestone",\
                "blazeandcave:bacap/challenges_milestone",\
                "blazeandcave:bacap/advancement_legend"]

    MINING_LIST=["blazeandcave:mining/root",
                "minecraft:story/mine_stone",
                "blazeandcave:mining/aww_it_broke",
                "blazeandcave:mining/spelunker",
                "blazeandcave:mining/heart_of_darkness",
                "blazeandcave:mining/my_work_here_is_done",
                "blazeandcave:mining/nananananananana",
                "blazeandcave:mining/filthy_lich",
                "blazeandcave:mining/thats_the_point",
                "blazeandcave:mining/particle_fan",
                "blazeandcave:mining/deep_slate_nine",
                "blazeandcave:mining/tuff_stuff",
                "blazeandcave:mining/rock_bottom",
                "blazeandcave:mining/moss_maker",
                "blazeandcave:mining/iggy",
                "blazeandcave:mining/lush_hour",
                "blazeandcave:mining/dungeons_and_spawners",
                "blazeandcave:mining/this_is_mine_now",
                "blazeandcave:mining/eeuuwww",
                "blazeandcave:mining/steals_on_wheels",
                "blazeandcave:mining/a_shiny_treat",
                "blazeandcave:mining/gold_mine",
                "minecraft:story/upgrade_tools",
                "blazeandcave:mining/moar_tools",
                "blazeandcave:mining/chestful_of_cobblestone",
                "blazeandcave:mining/bulldozer",
                "blazeandcave:mining/meet_the_flintstones",
                "blazeandcave:mining/flint_miner",
                "blazeandcave:mining/strike_a_light",
                "blazeandcave:mining/bonfire_night",
                "blazeandcave:mining/fossil_fuel",
                "blazeandcave:mining/coal_miner",
                "blazeandcave:mining/master_coal_miner",
                "blazeandcave:mining/hot_topic",
                "blazeandcave:mining/renewable_energy",
                "blazeandcave:mining/smokin_hot",
                "blazeandcave:mining/youll_never_take_me_alive_copper",
                "blazeandcave:mining/budget_channeling",
                "minecraft:adventure/lightning_rod_with_villager_no_fire",
                "blazeandcave:mining/called_shot",
                "blazeandcave:mining/dont_come_a_copper",
                "minecraft:husbandry/wax_on",
                "minecraft:husbandry/wax_off",
                "blazeandcave:mining/the_statue_of_liberty",
                "blazeandcave:mining/sly_copper_the_copper_heist",
                "blazeandcave:mining/copper_miner",
                "blazeandcave:mining/master_copper_miner",
                "minecraft:story/smelt_iron",
                "blazeandcave:mining/not_chicken_mcnuggets",
                "minecraft:story/iron_tools",
                "minecraft:story/obtain_armor",
                "blazeandcave:mining/iron_man",
                "blazeandcave:mining/iron_miner",
                "blazeandcave:mining/master_iron_miner",
                "blazeandcave:mining/gold_rush",
                "blazeandcave:mining/living_like_kings",
                "blazeandcave:mining/the_mistake",
                "blazeandcave:mining/gold_miner",
                "blazeandcave:mining/master_gold_miner",
                "blazeandcave:mining/bling_bling_gone",
                "blazeandcave:mining/weve_broken_our_last_shovel",
                "blazeandcave:mining/moar_broken_tools",
                "blazeandcave:mining/where_are_all_your_clothes",
                "blazeandcave:mining/diam_oh_wait_no",
                "blazeandcave:mining/lapis_lazuli_miner",
                "blazeandcave:mining/seeing_red",
                "blazeandcave:mining/the_way_to_spawn",
                "blazeandcave:mining/whats_the_time_mr_wolf",
                "blazeandcave:mining/redstone_miner",
                "blazeandcave:mining/gi_geode",
                "blazeandcave:mining/good_for_your_bones",
                "blazeandcave:mining/galileo_figaro",
                "blazeandcave:mining/pixel_perfect",
                "blazeandcave:mining/blackout",
                "blazeandcave:mining/amethyst_miner",
                "minecraft:story/mine_diamond",
                "blazeandcave:mining/iconic_merchandising_prop",
                "blazeandcave:mining/stabcraft",
                "blazeandcave:mining/even_moar_tools",
                "blazeandcave:mining/rest_in_pickaxes",
                "minecraft:story/shiny_gear",
                "blazeandcave:mining/diamond_clad",
                "blazeandcave:mining/diamond_miner",
                "blazeandcave:mining/diamonds_to_you",
                "blazeandcave:mining/mineral_collection",
                "blazeandcave:mining/master_diamond_miner",
                "blazeandcave:mining/mr_bean",
                "blazeandcave:mining/emerald_miner",
                "blazeandcave:mining/oresome",
                "minecraft:story/lava_bucket",
                "minecraft:story/form_obsidian",
                "minecraft:story/enchant_item",
                "minecraft:story/enter_the_nether",
                "blazeandcave:mining/obsidian_miner"]

    BUILDING_LIST=["blazeandcave:building/root",
                    "blazeandcave:building/your_door_was_locked",
                    "blazeandcave:building/cut_in_half",
                    "blazeandcave:building/stairs_no",
                    "blazeandcave:building/slabs_for_days",
                    "blazeandcave:building/ah_my_old_enemy",
                    "minecraft:adventure/sleep_in_bed",
                    "blazeandcave:building/change_of_sheets",
                    "blazeandcave:building/rainbow_dreams",
                    "blazeandcave:building/insomniac",
                    "blazeandcave:building/ladder_climbers_inc",
                    "blazeandcave:building/its_a_trap",
                    "blazeandcave:building/and_open",
                    "blazeandcave:building/en_garde",
                    "blazeandcave:building/the_walls",
                    "blazeandcave:building/crazy_walls",
                    "blazeandcave:building/stationary_storage",
                    "blazeandcave:building/its_a_sign",
                    "blazeandcave:building/colors_of_the_wind",
                    "blazeandcave:building/barrel_rider",
                    "blazeandcave:building/writers_block",
                    "blazeandcave:building/a_masterpiece",
                    "blazeandcave:building/mannequin",
                    "blazeandcave:building/armor_display",
                    "blazeandcave:building/art_gallery",
                    "blazeandcave:building/display_your_items_for_all_to_see",
                    "blazeandcave:building/raise_the_flag",
                    "blazeandcave:building/no_banner_only_color",
                    "blazeandcave:building/prepare_to_meet_your_loom",
                    "blazeandcave:building/fruit_of_the_looms",
                    "blazeandcave:building/torched",
                    "blazeandcave:building/camping_out",
                    "blazeandcave:building/delicious_hot_schmoes",
                    "blazeandcave:building/spawn_camping",
                    "blazeandcave:building/halloween",
                    "blazeandcave:building/one_pickle_two_pickle_sea_pickle_four",
                    "blazeandcave:building/setting_up_the_mood",
                    "blazeandcave:building/the_ritual_begins",
                    "blazeandcave:building/happy_birthday",
                    "blazeandcave:building/festival_of_lights",
                    "blazeandcave:building/glowing",
                    "blazeandcave:building/electric",
                    "blazeandcave:building/shroom_lightyear",
                    "blazeandcave:building/cerulean",
                    "blazeandcave:building/expensive",
                    "blazeandcave:building/fluorescent",
                    "blazeandcave:building/let_there_be_light",
                    "blazeandcave:building/barking_mad",
                    "blazeandcave:building/lost_its_bark",
                    "blazeandcave:building/professor_oak",
                    "blazeandcave:building/spruce_lee",
                    "blazeandcave:building/professor_birch",
                    "blazeandcave:building/the_jungler",
                    "blazeandcave:building/the_acacia_king",
                    "blazeandcave:building/professor_dark_oak",
                    "blazeandcave:building/yay_i_got_my_wood",
                    "blazeandcave:building/stripper",
                    "blazeandcave:building/master_logger",
                    "blazeandcave:building/i_dont_like_sand",
                    "blazeandcave:building/pathways",
                    "blazeandcave:building/grass_type",
                    "blazeandcave:building/skyblock",
                    "blazeandcave:building/classy_glassy",
                    "blazeandcave:building/what_a_pane",
                    "blazeandcave:building/translucence",
                    "blazeandcave:building/pane_in_the_glass",
                    "blazeandcave:building/rainbow_sand",
                    "blazeandcave:building/concrete_evidence",
                    "blazeandcave:building/the_rainbow_you_always_wanted",
                    "blazeandcave:building/clay_dough",
                    "blazeandcave:building/bricks",
                    "blazeandcave:building/pot_planter",
                    "blazeandcave:building/harry_potter",
                    "blazeandcave:building/the_terracotta_army",
                    "blazeandcave:building/the_glazed_terracotta_army",
                    "blazeandcave:building/rock_collection",
                    "blazeandcave:building/rock_polish",
                    "blazeandcave:building/fake_stronghold",
                    "blazeandcave:building/jailhouse_block",
                    "blazeandcave:building/creepers_and_withers",
                    "blazeandcave:building/deepslate_conspiracy",
                    "blazeandcave:building/fake_fortress",
                    "blazeandcave:building/greek_art_decor",
                    "blazeandcave:building/fake_monument",
                    "blazeandcave:building/no_chain_no_gain",
                    "blazeandcave:building/blackstonehenge",
                    "blazeandcave:building/its_original_form",
                    "blazeandcave:building/smooth_dude",
                    "blazeandcave:building/blast_it",
                    "blazeandcave:building/sharpening_station",
                    "blazeandcave:building/classic_pocket_edition_block",
                    "blazeandcave:building/agent_smithing_table",
                    "blazeandcave:building/bubble_bubble_toil_and_trouble",
                    "blazeandcave:building/washing_machine"]

    FARMING_LIST=["blazeandcave:farming/root",
                    "blazeandcave:farming/care_for_the_environment",
                    "blazeandcave:farming/bapple",
                    "blazeandcave:farming/trimming_the_treetops",
                    "blazeandcave:farming/foilage",
                    "blazeandcave:farming/yay_deadbush",
                    "blazeandcave:farming/ultra_hardcore",
                    "blazeandcave:farming/ecologist",
                    "blazeandcave:farming/an_apple_a_day",
                    "blazeandcave:farming/berry_nice",
                    "blazeandcave:farming/disen_berry_berry_bad",
                    "blazeandcave:farming/shrooms",
                    "blazeandcave:farming/mushroom_mushroom",
                    "blazeandcave:farming/mega_mushroom",
                    "blazeandcave:farming/suspicious_looking_stew",
                    "blazeandcave:farming/im_gonna_be_sick",
                    "blazeandcave:farming/sugar_sugar",
                    "blazeandcave:farming/its_full_of_ink",
                    "blazeandcave:farming/write_your_thoughts",
                    "blazeandcave:farming/an_amazing_story",
                    "blazeandcave:farming/kelp_me",
                    "blazeandcave:farming/aquatic_biofuel",
                    "blazeandcave:farming/undersea_gardener",
                    "blazeandcave:farming/castaway",
                    "blazeandcave:farming/its_a_cactus",
                    "blazeandcave:farming/spikey",
                    "minecraft:husbandry/plant_seed",
                    "blazeandcave:farming/souperman",
                    "blazeandcave:farming/bake_bread",
                    "blazeandcave:farming/the_lie",
                    "blazeandcave:farming/hay_there",
                    "blazeandcave:farming/must_be_your_birthday",
                    "blazeandcave:farming/its_where_nutella_comes_from",
                    "blazeandcave:farming/me_love_cookie",
                    "blazeandcave:farming/naturally_carved",
                    "blazeandcave:farming/the_pie",
                    "blazeandcave:farming/olaf",
                    "blazeandcave:farming/unmasked",
                    "blazeandcave:farming/pumpa_kungen",
                    "blazeandcave:farming/the_melon_the_melon_the_melon",
                    "blazeandcave:farming/scientific_inaccuracy",
                    "blazeandcave:farming/the_meloncholy_dane",
                    "blazeandcave:farming/die_potato",
                    "blazeandcave:farming/not_today",
                    "blazeandcave:farming/24_carrot_gold",
                    "blazeandcave:farming/the_garbage_will_do",
                    "blazeandcave:farming/natural_fertiliser",
                    "blazeandcave:farming/one_course_meal",
                    "blazeandcave:farming/combine_harvester",
                    "blazeandcave:farming/whats_new_with_composting",
                    "blazeandcave:farming/come_to_the_countryside",
                    "minecraft:husbandry/break_diamond_hoe",
                    "blazeandcave:farming/full_stomach",
                    "blazeandcave:farming/vegetarian",
                    "blazeandcave:farming/meat_lovers",
                    "minecraft:husbandry/balanced_diet",
                    "blazeandcave:farming/a_gluttonous_diet"]

    ANIMAL_LIST=["minecraft:husbandry/root",
                    "blazeandcave:animal/bacon",
                    "blazeandcave:animal/pork_chop",
                    "blazeandcave:animal/when_pigs_used_to_fly",
                    "blazeandcave:animal/pig_slaughterer",
                    "blazeandcave:animal/swine_sailing",
                    "blazeandcave:animal/rabbit_season",
                    "blazeandcave:animal/theyre_breeding_like_rabbits",
                    "blazeandcave:animal/lucky_charm",
                    "blazeandcave:animal/humble_bundle",
                    "blazeandcave:animal/getting_into_a_stew",
                    "blazeandcave:animal/in_a_hole_there_lived_a_rabbit",
                    "blazeandcave:animal/bunny_lover",
                    "blazeandcave:animal/fractal",
                    "blazeandcave:animal/going_down_the_rabbit_hole",
                    "blazeandcave:animal/just_keeps_going",
                    "blazeandcave:animal/cow_tipper",
                    "blazeandcave:animal/high_steaks",
                    "minecraft:husbandry/breed_an_animal",
                    "blazeandcave:animal/milk_does_your_body_good",
                    "blazeandcave:animal/true_cow_tipper",
                    "blazeandcave:animal/mooshroom_kingdom",
                    "blazeandcave:animal/super_mooshroom",
                    "blazeandcave:animal/milkshroom",
                    "blazeandcave:animal/mushroom_scientist",
                    "minecraft:husbandry/bred_all_animals",
                    "blazeandcave:animal/cool_kids",
                    "blazeandcave:animal/fashion_statement",
                    "blazeandcave:animal/shoe_shed",
                    "blazeandcave:animal/tickle_time",
                    "blazeandcave:animal/so_good",
                    "blazeandcave:animal/which_came_first",
                    "blazeandcave:animal/feeding_the_chickens",
                    "blazeandcave:animal/chicken_cooper",
                    "blazeandcave:animal/chatterbox",
                    "minecraft:adventure/spyglass_at_parrot",
                    "blazeandcave:animal/birdkeeper",
                    "blazeandcave:animal/wooly",
                    "blazeandcave:animal/feeling_sheepish",
                    "blazeandcave:animal/mary_had_a_little_lamb",
                    "blazeandcave:animal/have_a_shearful_day",
                    "blazeandcave:animal/sheariously",
                    "blazeandcave:animal/live_and_let_dye",
                    "blazeandcave:animal/rainbow_collection",
                    "blazeandcave:animal/fuzzy_feet",
                    "blazeandcave:animal/goat_out_of_here",
                    "blazeandcave:animal/billy_the_kid",
                    "blazeandcave:animal/goat_simulator",
                    "minecraft:husbandry/ride_a_boat_with_a_goat",
                    "blazeandcave:animal/screaming_milk",
                    "blazeandcave:animal/ya_like_jazz",
                    "minecraft:husbandry/safely_harvest_honey",
                    "blazeandcave:animal/hive_mind",
                    "blazeandcave:animal/not_the_bees",
                    "minecraft:husbandry/silk_touch_nest",
                    "blazeandcave:animal/honey_im_home",
                    "blazeandcave:animal/nest_quick",
                    "blazeandcave:animal/winnie_the_pooh",
                    "minecraft:adventure/honey_block_slide",
                    "blazeandcave:animal/wheres_the_honey_lebowski",
                    "blazeandcave:animal/cowboy",
                    "blazeandcave:animal/horse_armorer",
                    "blazeandcave:animal/colorful_cavalry",
                    "blazeandcave:animal/foal_play",
                    "blazeandcave:animal/so_hungry_i_could_eat_a_horse",
                    "blazeandcave:animal/a_horse_in_shining_armor",
                    "blazeandcave:animal/are_we_there_yet",
                    "blazeandcave:animal/artificial_selection",
                    "blazeandcave:animal/master_farrier",
                    "blazeandcave:animal/stay_calmer",
                    "blazeandcave:animal/so_i_got_that_going_for_me",
                    "blazeandcave:animal/llama_llama_duck_king",
                    "blazeandcave:animal/llama_festival",
                    "blazeandcave:animal/heavy_duty_caravan",
                    "blazeandcave:animal/blistering_barnacles",
                    "blazeandcave:animal/lead_the_way",
                    "blazeandcave:animal/beeloons",
                    "blazeandcave:animal/you_lead_ill_follow",
                    "blazeandcave:animal/follow_the_leader",
                    "minecraft:husbandry/tame_an_animal",
                    "blazeandcave:animal/puppies_yipe",
                    "blazeandcave:animal/what_does_the_fox_say",
                    "blazeandcave:animal/snow_fox_64",
                    "blazeandcave:animal/foxy_thievery",
                    "minecraft:husbandry/fishy_business",
                    "blazeandcave:animal/direct_fishing",
                    "blazeandcave:animal/grinding_nemo",
                    "blazeandcave:animal/cephalight",
                    "minecraft:husbandry/make_a_sign_glow",
                    "blazeandcave:animal/flashy_items",
                    "blazeandcave:animal/iceologer_shouldve_won",
                    "minecraft:husbandry/tactical_fishing",
                    "blazeandcave:animal/aquarium",
                    "blazeandcave:animal/tropical_collection",
                    "minecraft:husbandry/axolotl_in_a_bucket",
                    "minecraft:husbandry/kill_axolotl_target",
                    "blazeandcave:animal/thanks_a_lotl",
                    "blazeandcave:animal/axolittle",
                    "blazeandcave:animal/axolotl_of_them",
                    "blazeandcave:animal/axeolotl",
                    "blazeandcave:animal/delicious_fish",
                    "blazeandcave:animal/sushi",
                    "blazeandcave:animal/salmonella_poisoning",
                    "blazeandcave:animal/catching_nemo",
                    "blazeandcave:animal/what_a_piece_of_junk",
                    "blazeandcave:animal/treasure_hunter",
                    "blazeandcave:animal/someones_been_here_before",
                    "blazeandcave:animal/master_angler",
                    "blazeandcave:animal/totally_not_an_afk_fisher",
                    "blazeandcave:animal/poacher",
                    "blazeandcave:animal/hey_look_mom",
                    "blazeandcave:animal/scuttler",
                    "blazeandcave:animal/turtle_soldier",
                    "blazeandcave:animal/save_the_turtles",
                    "blazeandcave:animal/turtle_army"]

    MONSTERS_LIST=["blazeandcave:monsters/root",
                    "minecraft:adventure/kill_a_mob",
                    "blazeandcave:monsters/dead_dont_die",
                    "blazeandcave:monsters/there_has_to_be_another_way",
                    "blazeandcave:monsters/iron_belly",
                    "blazeandcave:monsters/desert_nomad",
                    "blazeandcave:monsters/zombie_slayer",
                    "blazeandcave:monsters/dead_really_dont_die",
                    "blazeandcave:monsters/freezing",
                    "blazeandcave:monsters/still_talking",
                    "blazeandcave:monsters/family_reunion",
                    "blazeandcave:monsters/custom_boss_fight",
                    "blazeandcave:monsters/trick_or_treat",
                    "blazeandcave:monsters/handsome_jack",
                    "blazeandcave:monsters/a_watery_grave",
                    "blazeandcave:monsters/tridented_shield",
                    "blazeandcave:monsters/because_im_aquaman",
                    "blazeandcave:monsters/mollusc_man",
                    "blazeandcave:monsters/captain_etho",
                    "blazeandcave:monsters/ooh_baby",
                    "blazeandcave:monsters/baby_baby_baby_noo",
                    "blazeandcave:monsters/poultry_boy",
                    "blazeandcave:monsters/spooky_skeleton",
                    "blazeandcave:monsters/boned",
                    "minecraft:story/deflect_arrow",
                    "blazeandcave:monsters/frosty",
                    "blazeandcave:monsters/skeleton_smiter",
                    "blazeandcave:monsters/paleontologist",
                    "blazeandcave:monsters/the_undead_cavalry",
                    "blazeandcave:monsters/melting",
                    "blazeandcave:monsters/spooky_skulls",
                    "blazeandcave:monsters/bone_to_party",
                    "blazeandcave:monsters/ew_ew_ew",
                    "blazeandcave:monsters/poisonous_ew",
                    "blazeandcave:monsters/spider_smasher",
                    "blazeandcave:monsters/spider_skeleton",
                    "blazeandcave:monsters/the_ghastly_eyes",
                    "blazeandcave:monsters/pupil_poppers",
                    "blazeandcave:monsters/what_a_creep",
                    "blazeandcave:monsters/keep_your_distance",
                    "blazeandcave:monsters/blast_shield",
                    "blazeandcave:monsters/controlled_detonation",
                    "blazeandcave:monsters/aww_man",
                    "blazeandcave:monsters/creeper_killer",
                    "blazeandcave:monsters/creepy_heads",
                    "blazeandcave:monsters/camouflage",
                    "blazeandcave:monsters/the_ender_of_ender",
                    "blazeandcave:monsters/ender_worm",
                    "blazeandcave:monsters/tele_morph",
                    "blazeandcave:monsters/enderman_destroyer",
                    "blazeandcave:monsters/plane_walker",
                    "blazeandcave:monsters/impossible",
                    "blazeandcave:monsters/basketblock_championship",
                    "blazeandcave:monsters/witch",
                    "blazeandcave:monsters/miracle_drink",
                    "blazeandcave:monsters/taste_of_your_own_medicine",
                    "blazeandcave:monsters/gelatinous_cube",
                    "blazeandcave:monsters/trampoline",
                    "blazeandcave:monsters/slime_squisher",
                    "blazeandcave:monsters/iskallium_collector",
                    "blazeandcave:monsters/termite_control",
                    "blazeandcave:monsters/the_phantom_menace",
                    "blazeandcave:monsters/ricochet_swoop",
                    "blazeandcave:monsters/phantom_slayer",
                    "blazeandcave:monsters/anti_air",
                    "minecraft:adventure/two_birds_one_arrow",
                    "blazeandcave:monsters/well_handle_this",
                    "blazeandcave:monsters/night_runner",
                    "blazeandcave:monsters/hell_hunter",
                    "blazeandcave:monsters/void_ender",
                    "blazeandcave:monsters/dungeon_crawler",
                    "minecraft:adventure/kill_all_mobs"]

    WEAPONRY_LIST=[ "blazeandcave:weaponry/root",
                    "minecraft:adventure/shoot_arrow",
                    "blazeandcave:weaponry/that_is_so_fletch",
                    "blazeandcave:weaponry/point_blank",
                    "blazeandcave:weaponry/bow_spammer",
                    "minecraft:adventure/sniper_duel",
                    "blazeandcave:weaponry/the_mighty_hunter",
                    "blazeandcave:weaponry/x_bow",
                    "minecraft:adventure/ol_betsy",
                    "minecraft:adventure/whos_the_pillager_now",
                    "blazeandcave:weaponry/artillery",
                    "blazeandcave:weaponry/fireworks_display",
                    "blazeandcave:weaponry/pyrotechnic",
                    "blazeandcave:weaponry/explosive_fire",
                    "blazeandcave:weaponry/my_eyes",
                    "blazeandcave:weaponry/who_ya_gonna_call",
                    "blazeandcave:weaponry/sir_knight",
                    "blazeandcave:weaponry/shield_luck",
                    "blazeandcave:weaponry/flying_colors",
                    "blazeandcave:weaponry/master_shieldsman",
                    "blazeandcave:weaponry/viking",
                    "blazeandcave:weaponry/axeman",
                    "blazeandcave:weaponry/shovel_knight",
                    "blazeandcave:weaponry/multiclassed",
                    "minecraft:adventure/throw_trident",
                    "blazeandcave:weaponry/king_of_the_sea",
                    "blazeandcave:weaponry/the_aquatic_hunter",
                    "blazeandcave:weaponry/poseidon_vs_hades",
                    "blazeandcave:weaponry/bombs_away",
                    "blazeandcave:weaponry/revenge",
                    "blazeandcave:weaponry/demolitions_expert",
                    "blazeandcave:weaponry/pig_fishing_tournament",
                    "blazeandcave:weaponry/indiana_jones",
                    "blazeandcave:weaponry/when_pigs_finally_fly",
                    "blazeandcave:weaponry/snowball_fight",
                    "blazeandcave:weaponry/a_snowballs_chance_in_hell",
                    "blazeandcave:weaponry/backfire",
                    "blazeandcave:weaponry/egging_dude",
                    "blazeandcave:weaponry/theres_yolk_on_my_head",
                    "blazeandcave:weaponry/expelliarmus",
                    "blazeandcave:weaponry/slapfish",
                    "blazeandcave:weaponry/diemonds",
                    "blazeandcave:weaponry/inspector_gadget",
                    "blazeandcave:weaponry/rock_paper_shears",
                    "blazeandcave:weaponry/its_time_consuming",
                    "blazeandcave:weaponry/loser",
                    "blazeandcave:weaponry/half_heart_life"]

    BIOMES_LIST=["blazeandcave:biomes/root",
                    "blazeandcave:biomes/for_you_my_sweet",
                    "blazeandcave:biomes/theres_a_zombie_on_the_lawn",
                    "blazeandcave:biomes/enchanted_forest",
                    "blazeandcave:biomes/flower_power",
                    "blazeandcave:biomes/the_mighty_jungle",
                    "blazeandcave:biomes/tarzan",
                    "blazeandcave:biomes/lion_hunter",
                    "blazeandcave:biomes/simba",
                    "blazeandcave:biomes/bamboom",
                    "blazeandcave:biomes/construction_worker",
                    "blazeandcave:biomes/top_of_the_world",
                    "blazeandcave:biomes/zoologist",
                    "blazeandcave:biomes/kung_fu_panda",
                    "blazeandcave:biomes/edge_of_the_jungle",
                    "blazeandcave:biomes/qinling",
                    "blazeandcave:biomes/pandamonium",
                    "blazeandcave:biomes/smooth_operator",
                    "blazeandcave:biomes/this_snow_is_snowier",
                    "minecraft:adventure/walk_on_powder_snow_with_leather_boots",
                    "blazeandcave:biomes/powder_full",
                    "blazeandcave:biomes/thin_ice",
                    "blazeandcave:biomes/spike_ice",
                    "blazeandcave:biomes/thick_ice",
                    "blazeandcave:biomes/everybody_loves_ice",
                    "blazeandcave:biomes/barbearian",
                    "blazeandcave:biomes/just_keep_swimming",
                    "blazeandcave:biomes/the_sea_calls_you",
                    "blazeandcave:biomes/boaty_mcboatface",
                    "blazeandcave:biomes/dolphin_dasher",
                    "blazeandcave:biomes/so_long_and_thanks_for_all_the_fish",
                    "blazeandcave:biomes/free_diver",
                    "blazeandcave:biomes/sleep_with_the_fishes",
                    "blazeandcave:biomes/the_great_blocky_reef",
                    "blazeandcave:biomes/in_a_pickle",
                    "blazeandcave:biomes/just_a_sample",
                    "blazeandcave:biomes/no_reefing",
                    "blazeandcave:biomes/echolocation",
                    "blazeandcave:biomes/pushed_around",
                    "blazeandcave:biomes/atlantis",
                    "blazeandcave:biomes/get_ship_rekt",
                    "blazeandcave:biomes/boatception",
                    "blazeandcave:biomes/titanic",
                    "blazeandcave:biomes/x_marks_the_spot",
                    "blazeandcave:biomes/moskstraumen",
                    "blazeandcave:biomes/kilometre_walk",
                    "blazeandcave:biomes/ten_thousand_blocks",
                    "blazeandcave:biomes/voyage",
                    "blazeandcave:biomes/one_with_the_forest",
                    "blazeandcave:biomes/cold_feet",
                    "blazeandcave:biomes/warm_feet",
                    "blazeandcave:biomes/snow_feet",
                    "blazeandcave:biomes/overgrown",
                    "blazeandcave:biomes/wet_feet",
                    "minecraft:adventure/adventuring_time"]

    ADVENTURE_LIST=[ "minecraft:adventure/root",
                    "blazeandcave:adventure/i_hereby_dub_thee",
                    "blazeandcave:adventure/i_just_want_to_make_toast",
                    "blazeandcave:adventure/whats_up_doc",
                    "blazeandcave:adventure/nyan_sheep",
                    "blazeandcave:adventure/slenderman",
                    "blazeandcave:adventure/the_one_and_true_johnny",
                    "blazeandcave:adventure/beethoven",
                    "blazeandcave:adventure/music_to_my_ears",
                    "blazeandcave:adventure/disc_jockey",
                    "blazeandcave:adventure/overpowered",
                    "blazeandcave:adventure/now_youre_thinking_with_portals",
                    "blazeandcave:adventure/grave_robber",
                    "blazeandcave:adventure/tomb_raider",
                    "blazeandcave:adventure/witchcraft",
                    "blazeandcave:adventure/secret_of_the_igloo",
                    "blazeandcave:adventure/raidin_master",
                    "blazeandcave:adventure/out_of_posts",
                    "blazeandcave:adventure/riot_shield",
                    "minecraft:adventure/voluntary_exile",
                    "blazeandcave:adventure/redemption_arc",
                    "blazeandcave:adventure/were_being_attacked",
                    "blazeandcave:adventure/its_so_beast_like",
                    "blazeandcave:adventure/i_am_ravager_hear_me_roar",
                    "blazeandcave:adventure/picador",
                    "blazeandcave:adventure/feeling_ill",
                    "minecraft:adventure/hero_of_the_village",
                    "blazeandcave:adventure/superhero_of_the_village",
                    "blazeandcave:adventure/justice",
                    "blazeandcave:adventure/buy_low_sell_high",
                    "blazeandcave:adventure/war_is_coming",
                    "blazeandcave:adventure/veteran_of_the_village",
                    "blazeandcave:adventure/travelling_merchant",
                    "blazeandcave:adventure/shady_deals",
                    "blazeandcave:adventure/florist",
                    "blazeandcave:adventure/this_dirt_is_dirtier",
                    "blazeandcave:adventure/leaflet_drop",
                    "blazeandcave:adventure/rebuilding_the_oceans",
                    "blazeandcave:adventure/deals_off",
                    "blazeandcave:adventure/do_you_want_to_trade",
                    "blazeandcave:adventure/oh_look_it_dings",
                    "blazeandcave:adventure/prime_specimen",
                    "minecraft:adventure/trade",
                    "blazeandcave:adventure/crazy_cat_lady",
                    "blazeandcave:adventure/if_only_cats_grew_into_kittens",
                    "minecraft:husbandry/complete_catalogue",
                    "minecraft:adventure/summon_iron_golem",
                    "blazeandcave:adventure/your_daily_fix",
                    "blazeandcave:adventure/murderer",
                    "blazeandcave:adventure/rekt",
                    "blazeandcave:adventure/you_are_the_pillager",
                    "blazeandcave:adventure/all_chained_up",
                    "blazeandcave:adventure/retro_future_knight",
                    "blazeandcave:adventure/filthy_rich",
                    "blazeandcave:adventure/filthy_stinkin_rich",
                    "blazeandcave:adventure/hey_you_two_should_kiss",
                    "blazeandcave:adventure/traveller",
                    "blazeandcave:adventure/village_settler",
                    "blazeandcave:adventure/town_planner",
                    "blazeandcave:adventure/workaholic",
                    "blazeandcave:adventure/professional",
                    "blazeandcave:adventure/businessman",
                    "blazeandcave:adventure/the_tribal_villagers",
                    "blazeandcave:adventure/lilypad_hatter",
                    "blazeandcave:adventure/council_of_crafters",
                    "blazeandcave:adventure/master_trader",
                    "blazeandcave:adventure/knowledge_is_power",
                    "blazeandcave:adventure/rare_candy_shop",
                    "blazeandcave:adventure/mapmaker",
                    "blazeandcave:adventure/mapmakers_table",
                    "blazeandcave:adventure/im_not_lost_anymore",
                    "blazeandcave:adventure/treasure_map",
                    "blazeandcave:adventure/monumental",
                    "blazeandcave:adventure/laser_sharks",
                    "blazeandcave:adventure/spear_fishing",
                    "blazeandcave:adventure/guardian_destroyer",
                    "blazeandcave:adventure/the_deep_end",
                    "blazeandcave:adventure/dry_spell",
                    "blazeandcave:adventure/sponge_miner",
                    "blazeandcave:adventure/house_of_psychos",
                    "blazeandcave:adventure/heres_johnny",
                    "blazeandcave:adventure/the_shielding",
                    "blazeandcave:adventure/ghostbuster",
                    "blazeandcave:adventure/wololo",
                    "minecraft:adventure/totem_of_undying"]

    REDSTONE_LIST=["blazeandcave:redstone/root",
                    "blazeandcave:redstone/under_pressure",
                    "blazeandcave:redstone/pressure_detector",
                    "blazeandcave:redstone/metal_plate",
                    "blazeandcave:redstone/bling_plate",
                    "blazeandcave:redstone/space_hopper",
                    "blazeandcave:redstone/space_dropper",
                    "blazeandcave:redstone/dispense_with_this",
                    "blazeandcave:redstone/target_acquired",
                    "blazeandcave:redstone/target_practise",
                    "minecraft:adventure/bullseye",
                    "blazeandcave:redstone/tripping_over",
                    "blazeandcave:redstone/troll_chest",
                    "blazeandcave:redstone/mozart",
                    "blazeandcave:redstone/take_notes",
                    "blazeandcave:redstone/noteworthy",
                    "blazeandcave:redstone/travelling_bard",
                    "blazeandcave:redstone/powerful_light",
                    "blazeandcave:redstone/repeating_repeater",
                    "blazeandcave:redstone/quirky_quartz",
                    "blazeandcave:redstone/quartz_miner",
                    "blazeandcave:redstone/comparing_comparator",
                    "blazeandcave:redstone/solar_power",
                    "blazeandcave:redstone/observer_buddy",
                    "blazeandcave:redstone/vibe_check",
                    "blazeandcave:redstone/on_a_rail",
                    "blazeandcave:redstone/fuel_engine",
                    "blazeandcave:redstone/electric_rails",
                    "blazeandcave:redstone/railwayman",
                    "blazeandcave:redstone/moving_storage",
                    "blazeandcave:redstone/moving_moving_storage",
                    "blazeandcave:redstone/mobile_explosion",
                    "blazeandcave:redstone/moving_parts",
                    "blazeandcave:redstone/sticky_parts",
                    "blazeandcave:redstone/engineer",
                    "blazeandcave:redstone/master_engineer"]

    ENCHANTING_LIST=["blazeandcave:enchanting/root",
                    "blazeandcave:enchanting/librarian",
                    "blazeandcave:enchanting/magical_stockpile",
                    "blazeandcave:enchanting/bow_down_to_me",
                    "blazeandcave:enchanting/to_infinity_and_beyond",
                    "blazeandcave:enchanting/super_efficient",
                    "blazeandcave:enchanting/fortunate_son",
                    "blazeandcave:enchanting/pick_like_silk",
                    "blazeandcave:enchanting/needle_sharp",
                    "blazeandcave:enchanting/undead_slayer",
                    "blazeandcave:enchanting/bane_of_one_shotting_spiders",
                    "blazeandcave:enchanting/newtons_flaming_laser_sword",
                    "blazeandcave:enchanting/a_rather_pointy_fence_post",
                    "blazeandcave:enchanting/overkill",
                    "blazeandcave:enchanting/over_overkill",
                    "blazeandcave:enchanting/shotbow",
                    "blazeandcave:enchanting/machine_bow",
                    "minecraft:adventure/arbalistic",
                    "blazeandcave:enchanting/boomerang",
                    "blazeandcave:enchanting/do_a_barrel_roll",
                    "blazeandcave:enchanting/zeus",
                    "minecraft:adventure/very_very_frightening",
                    "blazeandcave:enchanting/like_a_cat",
                    "blazeandcave:enchanting/armor_for_the_masses",
                    "blazeandcave:enchanting/knocking_your_socks_off",
                    "blazeandcave:enchanting/scuba_gear",
                    "blazeandcave:enchanting/fiery",
                    "blazeandcave:enchanting/gotta_go_fast",
                    "blazeandcave:enchanting/complete_enchanter",
                    "blazeandcave:enchanting/master_enchanter",
                    "blazeandcave:enchanting/heavy_metal",
                    "blazeandcave:enchanting/curses",
                    "blazeandcave:enchanting/handmade_blinding",
                    "blazeandcave:enchanting/let_it_go",
                    "blazeandcave:enchanting/this_name_sounds_cooler",
                    "blazeandcave:enchanting/ill_be_back",
                    "blazeandcave:enchanting/god_of_thunder",
                    "blazeandcave:enchanting/unbreakable",
                    "blazeandcave:enchanting/master_miner",
                    "blazeandcave:enchanting/master_digger",
                    "blazeandcave:enchanting/master_axeman",
                    "blazeandcave:enchanting/master_farmer",
                    "blazeandcave:enchanting/master_knight",
                    "blazeandcave:enchanting/master_sniper",
                    "blazeandcave:enchanting/master_arbalist",
                    "blazeandcave:enchanting/master_armorer",
                    "blazeandcave:enchanting/master_fisher",
                    "blazeandcave:enchanting/master_tridenteer"]

    STATISTICS_LIST=[ "blazeandcave:statistics/root",
                    "blazeandcave:statistics/out_for_a_stroll",
                    "blazeandcave:statistics/who_needs_cars",
                    "blazeandcave:statistics/i_enjoy_long_walks_and_playing_minecraft",
                    "blazeandcave:statistics/marathon",
                    "blazeandcave:statistics/your_legs_must_be_tired",
                    "blazeandcave:statistics/did_you_just_run_across_earth",
                    "blazeandcave:statistics/spring_in_your_step",
                    "blazeandcave:statistics/boing_boing",
                    "blazeandcave:statistics/jumping_jacks",
                    "blazeandcave:statistics/sneaky_snitch",
                    "blazeandcave:statistics/black_belt_ninja",
                    "blazeandcave:statistics/ancient_kung_fu_master",
                    "blazeandcave:statistics/laps_in_the_pool",
                    "blazeandcave:statistics/olympic_athlete",
                    "blazeandcave:statistics/olympic_gold_medallist",
                    "blazeandcave:statistics/minecart_rider",
                    "blazeandcave:statistics/i_like_trains",
                    "blazeandcave:statistics/global_railway_network",
                    "blazeandcave:statistics/pig_training",
                    "blazeandcave:statistics/snout_500",
                    "blazeandcave:statistics/lightning_mcpig",
                    "blazeandcave:statistics/horse_training",
                    "blazeandcave:statistics/sheriff_firearm",
                    "blazeandcave:statistics/scourge_of_the_west",
                    "blazeandcave:statistics/luxury_cruise",
                    "blazeandcave:statistics/pirate_captain",
                    "blazeandcave:statistics/sailor_of_the_seven_seas",
                    "blazeandcave:statistics/taking_it_in_stride",
                    "blazeandcave:statistics/who_needs_boats",
                    "blazeandcave:statistics/this_ride_is_lit_yo",
                    "blazeandcave:statistics/take_to_the_skies",
                    "blazeandcave:statistics/supersonic",
                    "blazeandcave:statistics/frequent_flyer",
                    "blazeandcave:statistics/mob_hunter",
                    "blazeandcave:statistics/bloodthirsty",
                    "blazeandcave:statistics/kill_or_be_killed",
                    "blazeandcave:statistics/the_parrots_and_the_bats",
                    "blazeandcave:statistics/cupid",
                    "blazeandcave:statistics/two_by_two",
                    "blazeandcave:statistics/the_haggler",
                    "blazeandcave:statistics/big_spender",
                    "blazeandcave:statistics/stonks",
                    "blazeandcave:statistics/novice_enchanter",
                    "blazeandcave:statistics/journeyman_enchanter",
                    "blazeandcave:statistics/elderly_enchanter",
                    "blazeandcave:statistics/level_up",
                    "blazeandcave:statistics/overlevelling",
                    "blazeandcave:statistics/xp_grinder",
                    "blazeandcave:statistics/the_first_night",
                    "blazeandcave:statistics/passing_the_time",
                    "blazeandcave:statistics/happy_new_year"]

    NETHER_LIST=["minecraft:nether/root",
                    "blazeandcave:nether/stem_research",
                    "blazeandcave:nether/what_a_fungi",
                    "blazeandcave:nether/i_am_root",
                    "blazeandcave:nether/dont_blink",
                    "blazeandcave:nether/twisted",
                    "blazeandcave:nether/what_about_corruption_planks",
                    "blazeandcave:nether/welcome_to_warp_zone",
                    "minecraft:nether/explore_nether",
                    "blazeandcave:nether/hell_botanist",
                    "blazeandcave:nether/spreading_corruption",
                    "blazeandcave:nether/the_struggle_nether_ends",
                    "blazeandcave:nether/roadhog",
                    "blazeandcave:nether/when_hoglins_breed",
                    "blazeandcave:nether/whole_hog",
                    "blazeandcave:nether/giddy_up",
                    "blazeandcave:nether/zork_chop",
                    "minecraft:nether/distract_piglin",
                    "blazeandcave:nether/cultural_misunderstandings",
                    "minecraft:nether/find_bastion",
                    "blazeandcave:nether/brute_force",
                    "blazeandcave:nether/et_tu_brute",
                    "minecraft:nether/loot_bastion",
                    "blazeandcave:nether/gilty",
                    "blazeandcave:nether/wub_wub_wub",
                    "blazeandcave:nether/we_got_a_live_one",
                    "blazeandcave:nether/when_piglins_fly",
                    "blazeandcave:nether/a_piglins_best_friend",
                    "blazeandcave:nether/hot_reels",
                    "minecraft:nether/ride_strider",
                    "blazeandcave:nether/bobbleheads",
                    "blazeandcave:nether/this_ones_mine",
                    "blazeandcave:nether/jenga",
                    "blazeandcave:nether/from_whence_it_came",
                    "blazeandcave:nether/ancient_restoration",
                    "minecraft:nether/obtain_crying_obsidian",
                    "blazeandcave:nether/anchorman",
                    "minecraft:nether/charge_respawn_anchor",
                    "blazeandcave:nether/the_tribal_snouts",
                    "blazeandcave:nether/high_temperature_fluid_monster",
                    "blazeandcave:nether/legend_of_hell_chicken_riders",
                    "blazeandcave:nether/magma_cube_squisher",
                    "blazeandcave:nether/giant_floating_jellyfish",
                    "blazeandcave:nether/fire_blast_shield",
                    "minecraft:adventure/spyglass_at_ghast",
                    "minecraft:nether/return_to_sender",
                    "blazeandcave:nether/bring_down_the_beast",
                    "blazeandcave:nether/ghast_slayer",
                    "minecraft:nether/uneasy_alliance",
                    "blazeandcave:nether/electrifying_alliance",
                    "blazeandcave:nether/hells_bells",
                    "blazeandcave:nether/hot_spring",
                    "blazeandcave:nether/polar_opposites",
                    "blazeandcave:nether/nugget_in_a_biscuit",
                    "blazeandcave:nether/stepping_on_legos",
                    "blazeandcave:nether/dark_ages",
                    "blazeandcave:nether/nether_rock_collection",
                    "blazeandcave:nether/quicksand",
                    "blazeandcave:nether/burnt_right_into_your_soul",
                    "blazeandcave:nether/a_soul_for_a_soul",
                    "blazeandcave:nether/seeing_stars",
                    "blazeandcave:nether/glows_in_the_dark",
                    "blazeandcave:nether/glowstone_miner",
                    "blazeandcave:nether/the_descent",
                    "minecraft:nether/obtain_ancient_debris",
                    "blazeandcave:nether/holy_scrap",
                    "blazeandcave:nether/diamonds_are_not_forever",
                    "blazeandcave:nether/moar_upgraded_tools",
                    "minecraft:nether/netherite_armor",
                    "blazeandcave:nether/soul_runnings",
                    "blazeandcave:nether/fool_me_twice",
                    "blazeandcave:nether/netherite_miner",
                    "blazeandcave:nether/master_netherite_miner",
                    "blazeandcave:nether/netherite_mad_lad",
                    "blazeandcave:nether/get_a_lode_of_this",
                    "minecraft:nether/use_lodestone",
                    "blazeandcave:nether/lodes_of_applications",
                    "blazeandcave:nether/im_in_lava_with_you",
                    "blazeandcave:nether/limbo_walker",
                    "minecraft:nether/fast_travel",
                    "blazeandcave:nether/let_me_out",
                    "blazeandcave:nether/inception",
                    "minecraft:nether/find_fortress",
                    "blazeandcave:nether/the_hunt_begins",
                    "minecraft:nether/get_wither_skull",
                    "minecraft:nether/summon_wither",
                    "blazeandcave:nether/decaying_beauty",
                    "minecraft:nether/create_beacon",
                    "minecraft:nether/create_full_beacon",
                    "blazeandcave:nether/instant_mining",
                    "blazeandcave:nether/beacon_overlord",
                    "minecraft:nether/obtain_blaze_rod",
                    "blazeandcave:nether/the_nethers_shield",
                    "blazeandcave:nether/blaze_extinguisher",
                    "blazeandcave:nether/time_to_fire_back",
                    "blazeandcave:nether/basis_of_brewing",
                    "minecraft:nether/brew_potion",
                    "blazeandcave:nether/enders_chest",
                    "minecraft:story/follow_ender_eye",
                    "minecraft:story/enter_the_end"]
                    
    POTION_LIST=["blazeandcave:potion/root",
                    "blazeandcave:potion/failed_concoctions",
                    "blazeandcave:potion/death_by_magic",
                    "blazeandcave:potion/performance_enhancing_drugs",
                    "blazeandcave:potion/super_strength",
                    "blazeandcave:potion/a_weak_brew",
                    "minecraft:story/cure_zombie_villager",
                    "blazeandcave:potion/mad_scientist",
                    "blazeandcave:potion/medic",
                    "blazeandcave:potion/hyper_healing",
                    "blazeandcave:potion/nocturnal",
                    "blazeandcave:potion/the_invisible_player",
                    "blazeandcave:potion/true_feather_falling",
                    "blazeandcave:potion/tank",
                    "minecraft:end/dragon_breath",
                    "blazeandcave:potion/noxious_fumes",
                    "blazeandcave:potion/gas",
                    "blazeandcave:potion/poison_dart",
                    "blazeandcave:potion/furious_ammunition",
                    "blazeandcave:potion/stayin_frosty",
                    "blazeandcave:potion/marine_marauder",
                    "blazeandcave:potion/hopping_mad",
                    "minecraft:nether/all_potions",
                    "blazeandcave:potion/a_much_more_doable_challenge",
                    "blazeandcave:potion/a_furious_test_subject",
                    "blazeandcave:potion/gas_bomb"]

    END_LIST=[ "minecraft:end/root",
                    "blazeandcave:end/dragon_shield",
                    "minecraft:adventure/spyglass_at_dragon",
                    "minecraft:end/kill_dragon",
                    "blazeandcave:end/the_actual_end",
                    "blazeandcave:end/the_point_of_no_return",
                    "blazeandcave:end/event_horizon",
                    "blazeandcave:end/cow_jumped_over_the_moon",
                    "minecraft:end/dragon_egg",
                    "blazeandcave:end/the_start_of_something",
                    "minecraft:end/respawn_dragon",
                    "blazeandcave:end/what_for",
                    "blazeandcave:end/ring_of_the_end",
                    "blazeandcave:end/the_beginning",
                    "minecraft:end/enter_end_gateway",
                    "blazeandcave:end/end_bricks",
                    "blazeandcave:end/getting_chorus",
                    "blazeandcave:end/extrabiologist",
                    "blazeandcave:end/purpurfect",
                    "blazeandcave:end/a_wizards_breakfast",
                    "blazeandcave:end/void_walker",
                    "blazeandcave:end/in_your_face_neil_armstrong",
                    "blazeandcave:end/im_coming_back_murph",
                    "blazeandcave:end/no_dont_let_me_leave_murph",
                    "minecraft:end/find_end_city",
                    "blazeandcave:end/for_mother_clarence",
                    "blazeandcave:end/portable_storage",
                    "blazeandcave:end/organizational_wizard",
                    "blazeandcave:end/somewhere_over_the_rainbow",
                    "blazeandcave:end/shouldnt_my_shield_levitate_too",
                    "blazeandcave:end/shulker_breaker",
                    "minecraft:end/levitate",
                    "blazeandcave:end/anti_gravity_generator",
                    "blazeandcave:end/good_luck_getting_this_one",
                    "blazeandcave:end/off_with_his_head",
                    "blazeandcave:end/dragon_vs_dragon",
                    "minecraft:end/elytra",
                    "blazeandcave:end/some_breakthrough",
                    "blazeandcave:end/rocketman",
                    "blazeandcave:end/sky_high",
                    "blazeandcave:end/uh_houston_we_have_a_problem"]
                    
    CHALLENGES_LIST=["blazeandcave:challenges/root",
                    "blazeandcave:challenges/all_the_blocks",
                    "blazeandcave:challenges/all_the_items",
                    "blazeandcave:challenges/stack_all_the_blocks",
                    "blazeandcave:challenges/stack_all_the_items",
                    "blazeandcave:challenges/telescopic",
                    "blazeandcave:challenges/highway_to_hell",
                    "blazeandcave:challenges/endergeddon",
                    "blazeandcave:challenges/potion_master",
                    "blazeandcave:challenges/biological_warfare",
                    "blazeandcave:challenges/nuclear_fusion",
                    "blazeandcave:challenges/zombie_apocalypse",
                    "blazeandcave:challenges/rise_of_the_skeletons",
                    "blazeandcave:challenges/creepergeddon",
                    "blazeandcave:challenges/dragon_army",
                    "blazeandcave:challenges/constellation",
                    "blazeandcave:challenges/warlock",
                    "blazeandcave:challenges/hearts_of_the_stack",
                    "blazeandcave:challenges/abyss_lord",
                    "blazeandcave:challenges/were_in_the_endgame_now",
                    "blazeandcave:challenges/dragon_vs_dragon_ii_electric_boogaloo",
                    "blazeandcave:challenges/dragon_vs_wither_the_pre_sequel",
                    "blazeandcave:challenges/the_perfect_run",
                    "blazeandcave:challenges/i_am_loot",
                    "blazeandcave:challenges/the_world_is_ending",
                    "blazeandcave:challenges/immortal",
                    "blazeandcave:challenges/death_from_all",
                    "blazeandcave:challenges/ad_astra",
                    "blazeandcave:challenges/im_in_space",
                    "blazeandcave:challenges/the_devils_distance",
                    "blazeandcave:challenges/a_million_blocks_away",
                    "blazeandcave:challenges/explorer_of_worlds",
                    "blazeandcave:challenges/ultimate_enchanter",
                    "blazeandcave:challenges/stockbroker",
                    "blazeandcave:challenges/global_vaccination",
                    "minecraft:nether/all_effects"]








    def __init__(self, minecraftdir="/media/local/Minecraft/server", servername="fury", worldname="fury"):

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
            if(advancement_file.endswith(".json")):
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

        self.PrintMilestone("Total Potion Advancements:    ","blazeandcave:bacap/potion_milestone",len(self._potion_advancements))
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

    def DiffMilestone(self, name, milestone_json, advancements, sheetslist):

        milestone_filename = self._bacadvancement_dirname+milestone_json
        advancement_file = open(milestone_filename,'r')
        advancement_info = json.load(advancement_file)
        milestonelist = []
        for i in advancement_info["criteria"]:
            key = next(iter(advancement_info["criteria"][i]["conditions"]["player"]["player"]["advancements"]))
            milestonelist.append(key)
        print(f"{name:10}: {len(milestonelist):3} - ",end="")
        print(f"{len(advancements):3} - ",end="")
        print(f"{len(sheetslist):3}  ",end="")
        if(len(advancements)<len(milestonelist)):
            differences = list(set(milestonelist)-set(advancements))
        else:
           differences = list(set(advancements)-set(milestonelist))
        if(len(sheetslist)<len(milestonelist)):
            differences = list(set(milestonelist)-set(sheetslist))
        else:
            differences = list(set(sheetslist)-set(milestonelist))
        print(differences)



    def SaveReportAdvancement(self,advancement,reportfile):
        if advancement in self._advancements:
            stillneeded = list(set(self._advancements[advancement]._criteria)-set(self._advancements[advancement]._finished))
            if(self._advancements[advancement]._completed==BCAdvancement.ADVANCEMENT_COMPLETED):
                reportfile.write(f"{self._advancements[advancement]._completed},")
            else:
                reportfile.write(f" ,")
            reportfile.write(f"{advancement},")
            reportfile.write(f"{self._advancements[advancement]._title},")
            if(self._advancements[advancement]._completed==BCAdvancement.ADVANCEMENT_NOTCOMPLETED):
                first=True
                for item in stillneeded:
                    if(first):
                        reportfile.write(f"{item}")
                        first=False
                    else:
                        reportfile.write(f" {item}")
#                       reportfile.write(f",")
            reportfile.write(f"\n") 

    def SaveReportFile(self):
        reportfilename = self._minecraftdir+"/bclogs/advancement_report.csv"
        reportfile = open(reportfilename, "w")

        reportfile.write("BAC Advancements\n")
        for item in self.BACAP_LIST:
            self.SaveReportAdvancement(item,reportfile)

        reportfile.write("\nMining\n")
        for item in self.MINING_LIST:
            self.SaveReportAdvancement(item,reportfile)

        reportfile.write("\nBuilding\n")
        for item in self.BUILDING_LIST:
            self.SaveReportAdvancement(item,reportfile)

        reportfile.write("\nFarming\n")
        for item in self.FARMING_LIST:
            self.SaveReportAdvancement(item,reportfile)

        reportfile.write("\nAnimal\n")
        for item in self.ANIMAL_LIST:
            self.SaveReportAdvancement(item,reportfile)

        reportfile.write("\nMonsters\n")
        for item in self.MONSTERS_LIST:
            self.SaveReportAdvancement(item,reportfile)

        reportfile.write("\nWeaponry\n")
        for item in self.WEAPONRY_LIST:
            self.SaveReportAdvancement(item,reportfile)

        reportfile.write("\nBiomes\n")
        for item in self.BIOMES_LIST:
            self.SaveReportAdvancement(item,reportfile)

        reportfile.write("\nAdventure\n")
        for item in self.ADVENTURE_LIST:
            self.SaveReportAdvancement(item,reportfile)

        reportfile.write("\nRedstone\n")
        for item in self.REDSTONE_LIST:
            self.SaveReportAdvancement(item,reportfile)

        reportfile.write("\nEnchanting\n")
        for item in self.ENCHANTING_LIST:
            self.SaveReportAdvancement(item,reportfile)

        reportfile.write("\nStatistics\n")
        for item in self.STATISTICS_LIST:
            self.SaveReportAdvancement(item,reportfile)

        reportfile.write("\nNether\n")
        for item in self.NETHER_LIST:
            self.SaveReportAdvancement(item,reportfile)

        reportfile.write("\nPotion\n")
        for item in self.POTION_LIST:
            self.SaveReportAdvancement(item,reportfile)

        reportfile.write("\nEnd\n")
        for item in self.END_LIST:
            self.SaveReportAdvancement(item,reportfile)

        reportfile.write("\nChallenges\n")
        for item in self.CHALLENGES_LIST:
            self.SaveReportAdvancement(item,reportfile)


#        for advancement in sorted(self._monsters_advancements):
#            print(f"{self._advancements[advancement]._title},{advancement}")

        reportfile.close

def main():

    print("BCAllAdvancements: Unit Testing")
    bcgame = BCAllAdvancements()

    bcgame.UpdateAdvancements()
    bcgame.PrintAllAdvancements()
    bcgame.SaveReportFile()

    bcgame.DiffMilestone("Mining", "/bacap/mining_milestone.json", bcgame._mining_advancements, bcgame.MINING_LIST)
    bcgame.DiffMilestone("Building","/bacap/building_milestone.json", bcgame._building_advancements, bcgame.BUILDING_LIST)
    bcgame.DiffMilestone("Farming","/bacap/farming_milestone.json", bcgame._farming_advancements, bcgame.FARMING_LIST)
    bcgame.DiffMilestone("Animal","/bacap/animal_milestone.json", bcgame._animal_advancements, bcgame.ANIMAL_LIST)

    bcgame.DiffMilestone("Monsters","/bacap/monsters_milestone.json", bcgame._monsters_advancements, bcgame.MONSTERS_LIST)
    bcgame.DiffMilestone("Weaponry","/bacap/weaponry_milestone.json", bcgame._weaponry_advancements, bcgame.WEAPONRY_LIST)
    bcgame.DiffMilestone("Biomes","/bacap/biomes_milestone.json", bcgame._biomes_advancements, bcgame.BIOMES_LIST)
    bcgame.DiffMilestone("Adventure","/bacap/adventure_milestone.json", bcgame._adventure_advancements, bcgame.ADVENTURE_LIST)

    bcgame.DiffMilestone("Redstone","/bacap/redstone_milestone.json", bcgame._redstone_advancements, bcgame.REDSTONE_LIST)
    bcgame.DiffMilestone("Enchanting","/bacap/enchanting_milestone.json", bcgame._enchanting_advancements, bcgame.ENCHANTING_LIST)
    bcgame.DiffMilestone("Statistics","/bacap/statistics_milestone.json", bcgame._statistics_advancements, bcgame.STATISTICS_LIST)
    bcgame.DiffMilestone("Nether","/bacap/nether_milestone.json", bcgame._nether_advancements, bcgame.NETHER_LIST)

    bcgame.DiffMilestone("Potion","/bacap/potion_milestone.json", bcgame._potion_advancements, bcgame.POTION_LIST)
    bcgame.DiffMilestone("End","/bacap/end_milestone.json", bcgame._end_advancements, bcgame.END_LIST)
    bcgame.DiffMilestone("Challenges","/bacap/challenges_milestone.json", bcgame._challenges_advancements, bcgame.CHALLENGES_LIST)

#    bcgame._advancements["blazeandcave:bacap/advancement_legend"].PrintAdvancement()
    
#    while True:
#        sleep(2)
#        print()
#        bcgame.UpdateAdvancements()
#        bcgame.PrintAllAdvancements()
#        bcgame._advancements["blazeandcave:bacap/advancement_legend"].PrintAdvancement()

if __name__ == '__main__':
    main()
