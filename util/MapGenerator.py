from PIL import Image
from perlin_noise import PerlinNoise

#from util.SLHandle import *

quadrants = {"A": [0,0],
             "B": [26,0],
             "G": [26,26],
             "D": [0,26]}
sectors = {"A":0, "B":1, "C":2, "D":3,
           "E":4, "F":5, "G":6, "H":7,
           "I":8, "J":9, "K":10, "L":11,
           "M":12, "N":13, "O":14, "P":15,
           "Q":16, "R":17, "S":18, "T":19,
           "U":20, "V":21, "W":22, "X":23,
           "Y":24, "Z":25}

def clamp(minimum, var, maximum):
    return max(minimum, min(var, maximum))

def seedTranslator(quadrant, sector, subsector, system, star=None, planet=None):
    sect = list(map(int.__add__, quadrant, sector))
    seed = f"{sect[0]}".rjust(2,"0") + f"{sect[1]}".rjust(2,"0") + \
        f"{subsector[0]*10+system[0]}".rjust(3,"0") + f"{subsector[1]*10+system[1]}".rjust(3,"0")
    if star is not None: seed += str(star)
    if planet is not None: seed += str(planet).rjust(2,"0")
    seed = int(seed)
    if (system[0]%2, system[1]%2) == (0,0):
        seed = int(round(seed * 3.1415926535879))
    if (system[0]%2, system[1]%2) == (0,1):
        seed = int(round(seed * 1.618033988749))
    if (system[0]%2, system[1]%2) == (1,0):
        seed = int(round(seed * 2.71828182845))
    if (system[0]%2, system[1]%2) == (1,1):
        seed = int(round(seed * 1.1235813213455))
    return seed

def generate(quadrant, sector, subsector, system=None, star=None, planet=None):
    """
Quadrant: ABGD
Sector: (x,y) range A-Z
Subsector: (x,y) range 0-59
System: (x,y) range 0-9
"""
    quadrant = quadrants[quadrant]
    sector = [sectors[sector[0]], sectors[sector[1]]]
    density = 0
    
    sect = list(map(int.__add__, quadrant, sector))
    #galaxyDensityMap = Image.open(".\\data\\galaxyDensityMap.png")
    galaxyDensityMap = Image.open("B:\\zako3\\assets\\maps\\galaxyDensityMap.png")
    sectorColor = galaxyDensityMap.getpixel(tuple(sect))
    density = sectorColor[0]//16 #the galaxy map is grayscale, it doesn't matter if the index is 0, 1, or 2.
    
    starClasses = "Y,T,L,M,K,G,F,A,D,B,n,O,Ø,W,Ð,X".split(",")
    hotPlanets = "A,B,D,E,F,H,N,X,Y".split(",")
    tempPlanets = "C,D,G,H,I,J,K,L,M,O,S,T,Y".split(",")
    coldPlanets = "C,D,H,P,U,W,Y,b".split(",")
        
    if system is None:
        #This loads a subsector.
        #This is the largest area that generate() will prepare.
        #Subsectors contain 10×10 systems.
        subsect = [[0,0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0,0]]
        for ycoord in range(len(subsect)):
            y = subsect[ycoord]
            for xcoord in range(len(y)):
                x = y[xcoord]
                system = list(map(int.__add__, subsector, [xcoord, ycoord]))
                systemSeed = seedTranslator(quadrant, sector, subsector, [xcoord, ycoord])
                subsect[ycoord][xcoord] = clamp(0, density-8+systemSeed%10, 5)

        for line in subsect:
            print(str(line).replace("[", "").replace(",", "").replace("]", ""))

    elif star is None:
        #This loads a system.
        #Systems contain 0-5 stars.
        systemSeed = seedTranslator(quadrant, sector, subsector, system)
        starCount = clamp(0, density-8+systemSeed%10, 5)
        sys = [["","","",""],
               ["","","",""],
               ["","","",""],
               ["","","",""]]
        for sol in range(starCount):
            starSeed = seedTranslator(quadrant, sector, subsector, system, sol)
            starType = clamp(0, starSeed%15, 15)
            starLocation = int(round(starSeed+sol*1.23513))%16
            while sys[starLocation//4][starLocation%4] != "":
                starLocation = int(round(starLocation+starSeed**sol*1.23513)) % 16
            sys[starLocation//4][starLocation%4] = starClasses[starType]

        for line in sys:
            print(str(line).replace("[", "").replace(",", "").replace("]", "").replace("''", "_").replace("'", ""))

    elif planet is None:
        starSeed = seedTranslator(quadrant, sector, subsector, system, star)
        starType = clamp(0, starSeed%15, 15)
        orbits = clamp(0, 5-density+starSeed%10, 10)
        orbitSpacing = clamp(10, 10-density+starSeed%15, 30)
        temperature = starType*10
        planets = []
        for rock in range(orbits):
            planetSeed = seedTranslator(quadrant, sector, subsector, system, star, rock)
            moons = int(round((planetSeed+rock)*1.379641633%5))
            planetType = None
            if temperature > 80:
                planetType = hotPlanets[clamp(0, (4-density+planetSeed)%8, 8)]
            if 80 >= temperature >= 50:
                planetType = tempPlanets[clamp(0, (6-density+planetSeed)%12, 12)]
            if 50 > temperature:
                planetType = coldPlanets[clamp(0, (3-density+planetSeed)%7, 7)]
            planets.append([planetType, moons])
            temperature -= orbitSpacing

        print(starClasses[starType])
        for rock in planets:
            print(str(rock).replace("[", "").replace(",", "").replace("]", "").replace("'", ""))

    else:
        planet -= 1
        planetSeed = seedTranslator(quadrant, sector, subsector, system, star, planet)
        starSeed = seedTranslator(quadrant, sector, subsector, system, star)
        starType = clamp(0, starSeed%15, 15)
        orbitSpacing = clamp(10, 10-density+starSeed%15, 30)
        temperature = starType*10 - orbitSpacing*planet
        if temperature > 80:
            planetType = hotPlanets[clamp(0, (4-density+planetSeed)%8, 8)]
        if 80 >= temperature >= 50:
            planetType = tempPlanets[clamp(0, (6-density+planetSeed)%12, 12)]
        if 50 > temperature:
            planetType = coldPlanets[clamp(0, (3-density+planetSeed)%7, 7)]
            
        octaves = 3
        xpix, ypix = 12*6*5, 6*6*5
        heights1 = PerlinNoise(seed=planetSeed*starSeed*planet%2**30, octaves=octaves)
        heights2 = PerlinNoise(seed=planetSeed*starSeed*planet%2**30, octaves=2*octaves)
        heights3 = PerlinNoise(seed=planetSeed*starSeed*planet%2**30, octaves=4*octaves)
        heights4 = PerlinNoise(seed=planetSeed*starSeed*planet%2**30, octaves=8*octaves)

        heightMap = []
        for i in range(xpix):
            row = []
            for j in range(ypix):
                noise_val = heights1([i/xpix, j/ypix])
                noise_val += 0.5 * heights2([i/xpix, j/ypix])
                noise_val += 0.25 * heights3([i/xpix, j/ypix])
                noise_val += 0.125 * heights4([i/xpix, j/ypix])
                row.append(noise_val)
            heightMap.append(row)
        
        temps1 = PerlinNoise(seed=planetSeed*starType*starType*planet%2**30, octaves=octaves)
        temps2 = PerlinNoise(seed=planetSeed*starType*starType*planet%2**30, octaves=2*octaves)
        temps3 = PerlinNoise(seed=planetSeed*starType*starType*planet%2**30, octaves=4*octaves)
        temps4 = PerlinNoise(seed=planetSeed*starType*starType*planet%2**30, octaves=8*octaves)
        
        tempMap = []
        for i in range(xpix):
            row = []
            for j in range(ypix):
                noise_val = temps1([i/xpix, j/ypix])
                noise_val += 0.5 * temps2([i/xpix, j/ypix])
                noise_val += 0.25 * temps3([i/xpix, j/ypix])
                noise_val += 0.125 * temps4([i/xpix, j/ypix])
                row.append(noise_val)
            tempMap.append(row)
        
        #tempMap = [[temps([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]
        
        worldMap = Image.new(mode="RGB", size=(xpix, ypix))
        worldMapEdit = worldMap.load()
        try: colorizer = Image.open(f"B:\\zako3\\assets\\maps\\planets\\{planetType}world.png")
        except Exception: colorizer = Image.open("B:\\zako3\\assets\\maps\\planets\\Cworld.png")

        for x in range(len(tempMap)):
            for y in range(len(tempMap[x])):
                localTemp = clamp(0, (tempMap[x][y] + 1)*128 * abs(y-ypix//2)/(ypix//4)-2, 255)
                localHeight = clamp(0, (heightMap[x][y] + 1)*128, 255)
                worldMapEdit[x,y] = colorizer.getpixel((localTemp, localHeight))
        worldMap.show()
