from random import randrange
from os import system

while True:
    sectorname = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    starspectrum = "YTLLMMMmKKKKkGGGGGgFFFFfAAAaBBbOoD2Ø"
    starspecifications = {"Y":["Sub-brown Dwarf", "Brown Dwarf", "no"],
                          "T":["Methane Star", "Brown Dwarf", "infrared"],
                          "L":["Luminous Brown Dwarf", "Brown Dwarf", "red"],
                          "M":["Red Star", "Main Sequence Star", "red"],
                          "m":["Red Giant Star", "Giant Star", "red"],
                          "K":["Orange Star", "Main Sequence Star", "orange"],
                          "k":["Orange Giant Star", "Giant Star", "orange"],
                          "G":["Yellow Star", "Main Sequence Star", "yellow"],
                          "g":["Yellow Giant Star", "Giant Star", "yellow"],
                          "F":["White Star", "Main Sequence Star", "white"],
                          "f":["White Giant Star", "Giant Star", "white"],
                          "A":["White Star", "Main Sequence Star", "blue-white"],
                          "a":["White Giant Star", "Giant Star", "blue-white"],
                          "B":["Blue Star", "Main Sequence Star", "blue"],
                          "b":["Blue Giant Star", "Giant Star", "blue"],
                          "O":["Blue Star", "Main Sequence Star", "ultraviolet"],
                          "o":["Blue Giant Star", "Giant Star", "ultraviolet"],
                          "D":["White Dwarf", "Degenerate Star", "white"],
                          "II":["Neutron Star", "Degenerate Star", "ultraviolet"],
                          "Ø":["Black Hole", "Degenerate Star", "no"]}
    sec_x = sectorname[randrange(len(sectorname))]
    sec_y = sectorname[randrange(len(sectorname))]
    starclass = starspectrum[randrange(len(starspectrum))]
    starid = randrange(100000)
    if starclass == "2":
        starclass = "II"
    starname = f"{sec_x}{sec_y}{str.upper(starclass)}{starid}"
    print(f"Star: {starname} - {starspecifications[starclass][0]}\n    A {starspecifications[starclass][1]} that emits {starspecifications[starclass][2]} light.")

    orbits = randrange(11)
    hot_orbits = 0
    temperate_orbits = 0
    cold_orbits = 0
    if orbits > 3:
        hot_orbits = randrange(max(orbits//3,1))
        cold_orbits = randrange(max(orbits//2,1))
        temperate_orbits = orbits - hot_orbits - cold_orbits
    if 3 >= orbits > 0:
        ln = randrange(orbits)+1
        if ln == 1:
            cold_orbits = randrange(max(orbits//2,1))
            if orbits - cold_orbits > 0:
                ln = randrange(orbits - cold_orbits)+1
                if ln == 1:
                    temperate_orbits = orbits - cold_orbits
                else:
                    hot_orbits = orbits - cold_orbits
        if ln == 2:
            hot_orbits = randrange(max(orbits//2,1))
            if orbits - hot_orbits > 0:
                ln = randrange(orbits - hot_orbits)+1
                if ln == 1:
                    temperate_orbits = orbits - hot_orbits
                else:
                    cold_orbits = orbits - hot_orbits
    print(f"    Has {orbits} planet(s).\n")
    planetspectrum = "AAAAAABBBBBBCCCCCCCCDDDDDEEEFFFGGGHHHHHIIIIJJJJJJKKKKLLLMMMNNNNOOOOPPPPPPPPQSTXYZ"
    #Temperature: Tuple temperature range, 0 to 15. Determines where in the system planets can form.
      #0: Absolute zero, 0K (Cold)
      #1: Boiling point of hydrogen, 20K (Cold)
      #2: Boiling point of oxygen, 90K (Cold)
      #3: Sublimation point of methane, 111K (Cold)
      #4: Boiling point of ammonia and chlorine, 239K (Temperate)
      #5: Melting point of water, 273K (Temperate)
      #6: Room Temp, 293K (Temperate)
      #7: Boiling point of water, 373K (Hot)
      #8: Boiling point of sulphur, 717K (Hot)
      #9: 1000K (Hot)
      #10: 1250K (Hot)
      #11: 1500K (Hot)
      #12: 1750K (Hot)
      #13: Melting point of quartz, 1986K (Hot)
      #14: 2500K
      #15: >3000K
    #Materials: name, (melting point, boiling point)
    materials = [["H2", (0,1)],
                 ["He", (0,0)],
                 ["C", (15,15)], ["CO", (2,2)], ["CO2", (4,4)], ["CH4", (3,3)],
                 ["N2", (2,2)], ["NH3", (3,4)],
                 ["O2", (1,2)], ["H2O", (5,7)],
                 ["F2", (1,2)],
                 ["Ne", (1,1)],
                 ["Na", (7,10)],
                 ["SiO2", (13,15)],
                 ["S8", (7,8)], ["SO2", (4,5)], ["SO3", (6,7)], ["H2SO4", (6,8)],
                 ["Cl2", (3,4)],
                 ["Fe2O3", (12,15)]
                 ]

    #planet type, surface, temperature, atmosphere, hydrosphere, habitability, description
    #Planet Type: The name tied to the class.
    #Surface: Terrestrial, Oceanic, or Gaseous.
    
    #Atmosphere: Tuple thickness range, 0 to 10.
      #0: Void
      #3: Mars-like
      #5: Earth-like
      #7: Venus-like
      #10: Jupiter-like
    planetspectrumspecifications = {
        "A" : ["Geothermal Planet", "Terrestrial", (8,10), (1,3), True, False, "A small world with rampant volcanic activity."],
        "B" : ["Geomorteus Planet", "Terrestrial", (7,9), (0,2), True, False, "A small, hot, dead world."],
        "C" : ["Geoinactive Planet", "Terrestrial", (1,6), (0,0), False, False, "A small, cold, dead world."],
        "D" : ["Dwarf Planet", "Terrestrial", (0,15), (0,0), False, False, "A tiny rock floating in the void."],
        "E" : ["Geoplastic Planet", "Terrestrial", (8,15), (1,3), True, False, "A planet which is completely molten."],
        "F" : ["Geometallic Planet", "Terrestrial", (4,8), (2,5), True, True, "A planet whose crust has recently formed."],
        "G" : ["Geocrystalline Planet", "Terrestrial", (3,8), (2,7), True, True, "A planet which has cooled down enough to support life."],
        "H" : ["Desert Planet", "Terrestrial", (3,7), (3,6), True, True, "A planet whose surface is mostly parched."],
        "I" : ["Gas Supergiant Planet", "Gaseous", (3,4), (9,10), False, False, "A massive planet made of gas."],
        "J" : ["Gas Giant Planet", "Gaseous", (3,6), (7,10), False, False, "A large gaseous planet."],
        "K" : ["Adaptable Planet", "Terrestrial", (3,7), (1,4), False, True, "A barren world that can host life with slight alterations."],
        "L" : ["Marginal Planet", "Terrestrial", (3,7), (2,6), True, True, "A dry world that seems to have flora but no fauna."],
        "M" : ["Minshara Planet", "Terrestrial", (4,6), (4,6), True, True, "A lush planet that is teeming with life."],
        "N" : ["Reducing Planet", "Terrestrial", (6,8), (6,9), True, False, "A planet with a thick, acidic atmosphere."],
        "O" : ["Pelagic Planet", "Oceanic", (4,6), (4,6), True, True, "A planet whose surface is mostly liquid."],
        "P" : ["Glaciated Planet", "Terrestrial", (3,5), (4,6), True, True, "An ice ball, which gets a band of melt around the equator every summer."],
        "Q" : ["Variable Planet", "Terrestrial", (2,10), (2,7), True, True, "A planet with an eccentric orbit. Temperatures vary wildly throughout the year."],
        "R" : ["Rogue Planet", "Terrestrial", (0,1), (0,0), False, False, "An orphaned planet who by some means lost its host star."],
        "S" : ["Ultragiant Planet", "Gaseous", (2,3), (10,10), False, False, "A very massive planet made of gas."],
        "T" : ["Hypergiant Planet", "Gaseous", (2,5), (10,10), False, False, "An extremely massive planet that has never undergone fusion."],
        "U" : ["Ice Giant Planet", "Oceanic", (2,4), (6,9), True, False, "A cold ball of ice and liquid hydrogen compounds, enveloped in a thick atmosphere."],
        "V" : ["Tachyon Planet", "Terrestrial", (1,8), (0,8), True, False, "A strange world whose core composed of superluminal particles warps space-time around it."],
        "W" : ["Stygian Planet", "Terrestrial", (1,2), (0,0), False, False, "A planet that survived its own star's death. Its surface is scorched, and any atmosphere or hydrosphere has long since been torn away."],
        "X" : ["Chthonian Planet", "Terrestrial", (7,10), (0,0), False, False, "The naked core of a gas giant whose atmosphere was blown away by its star."],
        "Y" : ["Demon Planet", "Terrestrial", (1,10), (5,7), True, False, "A planet designed specifically to kill anything on it. The atmosphere is thick, toxic, and turbulent, and the surface is bombarded constantly by various forms of radiation."],
        "Z" : ["Erratic Planet", "Terrestrial", (0,12), (0,8), True, False, "A planet with a highly eccentric orbit. Temperatures vary wildly throughout the year. In the winter, the atmosphere freezes, and in the summer, the rocks melt."],
        "α" : ["Strange Planet", "Terrestrial", (1,10), (6,10), True, False, "An extremely dense planet made of strange matter, which forms when a chunk of strange matter from an exploding neutron star collides with a planet."]
        }

    #TODO: Create randomizer that chooses planets from the above chart depending on orbit
    #TODO: Create randomizer that chooses atmos, hydros, and lithos elements depending on temperature and bools

    hot_ptypes = [["Geomorteus Planet", "Terrestrial", "n airless", "uninhabitable"],
                  ["Geomorteus Planet", "Terrestrial", "n airless", "uninhabitable"],
                  ["Reducing Planet", "Terrestrial", " choking, toxic", "uninhabitable"],
                  ["Puffed Gas Planet", "Gaseous", " sparse, thick", "uninhabitable"]]
    temp_ptypes = [["Desert Planet", "Terrestrial", " thin", "barely habitable"],
                  ["Minshara Planet", "Terrestrial", "n oxygenated", "habitable"],
                  ["Pelagic Planet", "Oceanic", " humid, oxygenated", "habitable"],
                  ["Gas Planet", "Gaseous", " thick, stormy", "uninhabitable"]]
    cold_ptypes = [["Desert Planet", "Terrestrial", " thin", "barely habitable"],
                  ["Geoinactive Planet", "Terrestrial", "n airless", "uninhabitable"],
                  ["Glaciated Planet", "Oceanic", " thin, stormy", "barely habitable"],
                  ["Ice Giant Planet", "Gaseous", " thick, stormy", "uninhabitable"]]
    moons_spread = [0, 0, 1, 1, 1, 2, 2, 3, 4, 5]
    orbit_no = 1
    for h in range(hot_orbits):
        randomizer = randrange(4)
        moon_ct = moons_spread[randrange(len(moons_spread))]
        ptype = hot_ptypes[randomizer]
        print(f"{starname}-{orbit_no} - {ptype[0]}\n    A hot, {ptype[3]} {ptype[1]} planet with a{ptype[2]} atmosphere.\n    Has {moon_ct} major moon(s).\n")
        orbit_no += 1
    for t in range(temperate_orbits):
        randomizer = randrange(4)
        moon_ct = moons_spread[randrange(len(moons_spread))]
        ptype = temp_ptypes[randomizer]
        print(f"{starname}-{orbit_no} - {ptype[0]}\n    A temperate, {ptype[3]} {ptype[1]} planet with a{ptype[2]} atmosphere.\n    Has {moon_ct} major moon(s).\n")
        orbit_no += 1
    for c in range(cold_orbits):
        randomizer = randrange(4)
        moon_ct = moons_spread[randrange(len(moons_spread))]
        ptype = cold_ptypes[randomizer]
        print(f"{starname}-{orbit_no} - {ptype[0]}\n    A cold, {ptype[3]} {ptype[1]} planet with a{ptype[2]} atmosphere.\n    Has {moon_ct} major moon(s).\n")
        orbit_no += 1
        
    input("\n\nPress Enter to generate a new system.\n")
    system("cls")
