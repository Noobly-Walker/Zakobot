from random import randrange
from PIL import Image, ImageFont, ImageDraw, ImageChops, ImageOps
from os import remove
from os.path import exists

class coinStacker:
    def __init__(self, coins:dict):
        #coins must be in the following format
        #{ value: (colorR, colorG, colorB) }
        self.coins = coins
        self.coinTypes = list(self.coins.keys())
        self.salt = id(self.coins) #salt
        self.stackUnit = []
        for i in self.coinTypes:
            self.stackUnit.append(0)

        #drawing coins
        for i in self.coinTypes:
            coin = Image.open(f".\\assets\\images\\coin.png").convert("RGBA")
            r, g, b, alpha = coin.split()
            gray = ImageOps.grayscale(coin)
            coin = ImageOps.colorize(gray, black=self.coins[i], white="#E0E0E0")
            coin.putalpha(alpha)
            coin.save(f".\\temp\\{self.salt}coin{i}.png")

    def trim(self, im):
        bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
        diff = ImageChops.difference(im, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        if bbox:
            return im.crop(bbox)

    def purge(self):
        #print("Removing generated images!")
        for i in self.coinTypes:
            remove(f".\\temp\\{self.salt}coin{i}.png")
            if exists(f".\\temp\\{self.salt}tencoin{i}.png"):
                remove(f".\\temp\\{self.salt}tencoin{i}.png")
        if exists(f".\\temp\\{self.salt}coinpile.png"):
            remove(f".\\temp\\{self.salt}coinpile.png")

    def createPile(self, coinCount):
        tick = 0
        pointer = 0
        stackReq = 5
        startCount = coinCount
        index = -1

        stack = [list(self.stackUnit)]

        while coinCount > 0:
            #debug
            #if tick%100 == 0: print(f"Placed {startCount-coinCount:,} of {startCount:,} coins ({(startCount-coinCount)/startCount*100:.2f}%)")

            #create the most valuable coin possible
            while coinCount < self.coinTypes[index]:
                index -= 1
            coinCount -= self.coinTypes[index]

            #add a coin to the pile
            stack[pointer][index] += 1
            #find a random location in the pile for the next coin
            if len(stack) > 1: pointer = randrange(len(stack))

            #if the coin pile is getting too high, make new stacks
            if sum(stack[-1]) >= stackReq:
                stack = [list(self.stackUnit), *stack, list(self.stackUnit)]
                stackReq += 0.01
                
            #debug
            #tick += 1
        
        #print("Stacking complete! Drawing pile!")
        #setting boundaries for drawing the pile
        stackWidth = 34
        coinMaxHeight = 21
        coinHeight = 4
        #buffer to prevent coins from clipping the edge
        xPointer = 2
        stackCounter = 1

        #checking height of pile
        highestPile = 0
        for pile in stack:
            if sum(pile) > highestPile: highestPile = sum(pile)

        #making large stacks to reduce rendering time
        if highestPile >= 20:
            images = []
            
            for i, c in enumerate(self.coinTypes):
                images.append(Image.new(mode="RGBA", size=(stackWidth+4, coinMaxHeight+10*coinHeight+8)))
                yPointer = 10*coinHeight+6
                for j in range(10):
                    #randomness to make stacks more interesting
                    xRandOffset = randrange(3)-1
                    yRandOffset = randrange(3)-1
                    #load the image of the coin we want to place
                    image = Image.open(f".\\temp\\{self.salt}coin{c}.png").convert("RGBA")
                    #paste the image with the offsets, using itself as a transparency filter
                    images[i].paste(image, (xPointer+xRandOffset, yPointer+yRandOffset), image)
                    #move the vertical pointer up to the next coin's position
                    yPointer -= coinHeight
                images[i] = self.trim(images[i])
                images[i].save(f".\\temp\\{self.salt}tencoin{c}.png")

        #prepare the image
        pileImg = Image.new(mode="RGBA", size=(stackWidth*len(stack)+4, coinMaxHeight+highestPile*coinHeight+8))
        for pile in stack:
            coin = len(pile)
            pile = reversed(pile)
            #reset the vertical pointer for this stack
            yPointer = highestPile*coinHeight+6
            #if stackCounter%10 == 0: print(f"Preparing stack {stackCounter:,} of {len(stack):,} ({stackCounter/len(stack)*100:.2f}%)")
            for coinstack in pile:
                coin -= 1
                while coinstack > 0:
                    #place stack of 10 coins to reduce rendering cost
                    if coinstack >= 10:
                        image = Image.open(f".\\temp\\{self.salt}tencoin{self.coinTypes[coin]}.png").convert("RGBA")
                        yPointer -= coinHeight*10
                        pileImg.paste(image, (xPointer+xRandOffset, yPointer+yRandOffset), image)
                        coinstack -= 10
                    else:
                        #randomness to make stacks more interesting
                        xRandOffset = randrange(3)-1
                        yRandOffset = randrange(3)-1
                        #load the image of the coin we want to place
                        image = Image.open(f".\\temp\\{self.salt}coin{self.coinTypes[coin]}.png").convert("RGBA")
                        #move the vertical pointer up to the next coin's position
                        yPointer -= coinHeight
                        #paste the image with the offsets, using itself as a transparency filter
                        pileImg.paste(image, (xPointer+xRandOffset, yPointer+yRandOffset), image)
                        coinstack -= 1
            #move the horizontal pointer to where the next stack will be
            xPointer += stackWidth
            stackCounter += 1
        #display the image and save it
        #print(f"Image compiled!")
        pileImg.save(f".\\temp\\{self.salt}coinpile.png")
        return f".\\temp\\{self.salt}coinpile.png"
