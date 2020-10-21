from tkinter import *
import random, noise, sys
import fileReader

preset = fileReader.getInfo(sys.argv[1])
W,H = int(preset['screen']),int(preset['screen'])
CPL = int(preset['cells']) # 200

print(preset['seed'])

# 70 just good
# 34 also good
# 54 same

terrainData = {
    'mag'           :float(preset['mag']), # 0.015
    'extraMag'      :float(preset['extraMag']), # 0.08
    'weight'        :float(preset['weight']), # 0.7
    'passes'        :int(preset['passes']),
    'seed'          :int(preset['seed'])
}
biomeData = {
    'mag'           :0.03,
    'swampMag'      :0.02,
    'passes'        :10,
    'seed'          :int(random.randint(-100,100)),
    'seaLevel'      :int(preset['sea']),
    'fp'            :int(preset['fp']),
    'moutain'       :int(preset['moutain'])
}

color = {
    'beach' : ['#dcac17'],
    'desert': ['yellow'],
    'ice'   : ['#40bdc5'],
    'tree'  : ['#006400'],
    'swamp' : ['#013220','#011f14','#013220','#013220']
}
def mapVal(s,a1,a2,b1,b2):
    return int(b1 + ((s - a1)*(b2-b1))/(a2-a1))

def rgb_to_hex(*value):
    return '#%02x%02x%02x' %value


class Tile():
    def __init__(self,cnv,pos,size,value,biomeData,temp,swampData):
        self.biomeData = biomeData
        self.value = value
        self.swampData = swampData
        self.moisture = value - self.biomeData['seaLevel']
        self.temp = temp
        c = mapVal(swampData,0,100,0,255)
        self.color = rgb_to_hex(c,c,c)
        self.color = self.setColor(value)
        outline = self.color
        if preset['outline'] == 'True':
            outline = 'black'

        self.Obj = cnv.create_rectangle(
            pos[1]*size,
            pos[0]*size,
            (pos[1]*size)+size,
            (pos[0]*size)+size,
            fill=self.color,
            outline=outline,
        )

    def setColor(self,elevation):
        sea = self.biomeData['seaLevel']
        if (elevation <= sea):
            if (self.temp <= self.biomeData['fp'] and self.moisture >= -5):
                return random.choice(color['ice'])
            else:
                return rgb_to_hex(0,0,mapVal(elevation,0,100,0,255))
        elif self.blend(self.swampData,38,5,2) == True and self.blend(self.temp,200,5,2) == False and self.blend(self.moisture,5,5,1) == True:
            return random.choice(color['swamp'])
        elif (self.moisture <= 3):
            if (self.blend(self.temp,self.biomeData['fp'],15,5) == True):
                val = mapVal(elevation,sea,self.biomeData['moutain'],200,255)
                return rgb_to_hex(val,val,val)
            else:
                return random.choice(color['beach'])
        elif (elevation >= self.biomeData['moutain']):
            val = mapVal(elevation,self.biomeData['moutain'],100,100,255)
            return rgb_to_hex(val,val,val)
        elif (self.blend(self.temp,self.biomeData['fp'],15,5) == True):
            val = mapVal(elevation,sea,self.biomeData['moutain'],200,255)
            return rgb_to_hex(val,val,val)
        elif (self.temp >= self.biomeData['fp']+40 and self.moisture <= 12):
            if random.randint(0,2) == 0:
                return random.choice(color['tree'])
            else:
                return self.setGrass()
        # elif (self.temp >= 180):
        #     return random.choice(color['desert'])
        else:
            return self.setGrass()

    def blend(self,value,threshold,maxDif,base):
        if (value <= threshold):
            return True
        else:
            dif = value - threshold
            if (dif <= maxDif):
                if (random.randint(0,dif) <= base):
                    return True
                return False
            return False

    def setGrass(self):
        elevation = (100 - self.value)
        return rgb_to_hex(0,mapVal(self.value,0,100,0,255),0)

class Terrain():
    def __init__(self,noiseData,biomeData):
        self.terrain = Canvas(root,width=W,height=H,bd=0,highlightthickness=0)
        self.terrain.pack()
        self.tiles = self.generate_terrain()
        self.noiseData = noiseData
        self.biomeData = biomeData
        self.tempMap = self.getTemp()
        self.swamp = self.swampMap()
        for r in self.tiles:
            for tile in r:
                pass


    def generate_terrain(self):
        size = int(H/CPL)
        for y in range(CPL):
            yield self.generate_row(size,y)

    def generate_row(self,size,y):
        for x in range(CPL):
            e = mapVal(noise.pnoise2(
                x*self.noiseData['mag'],
                y*self.noiseData['mag'],
                octaves=int(self.noiseData['passes']),
                base=int(self.noiseData['seed']),
                ),-1,1,0,100
            )
            extra = e
            if self.noiseData['extraMag'] != False:
                extra = mapVal(noise.pnoise2(
                    x*self.noiseData['extraMag'],
                    y*self.noiseData['extraMag'],
                    octaves=int(self.noiseData['passes']),
                    base=int(self.noiseData['seed']),
                    ),-1,1,0,100
                )
            yield Tile(self.terrain,[y,x],size,self.weight(self.noiseData['weight'],e,extra),self.biomeData,self.tempMap[y][x],self.swamp[y][x])

    def getTemp(self):
        equator = int(CPL/2)
        tempRange = [10,200] # <- temp range
        tempFlux = [-45,45]
        tempMap = []
        for y in range(CPL):
            row = []
            for x in range(CPL):
                defaultTemp = mapVal(abs(equator-y),0,equator,tempRange[0],tempRange[1])
                tempNoise = mapVal(noise.pnoise2(
                    x*self.biomeData['mag'],
                    y*self.biomeData['mag'],
                    octaves=int(self.biomeData['passes']),
                    base=int(self.noiseData['seed']),
                    persistence=0.01
                ),-1,1,tempFlux[0],tempFlux[1])
                temp = defaultTemp+tempNoise
                row.append((tempRange[1]+tempFlux[1])-temp)
            tempMap.append(row)

        return tempMap


    def swampMap(self):
        m = []
        for y in range(CPL):
            row = []
            for x in range(CPL):
                n = mapVal(noise.pnoise2(
                    x*self.biomeData['swampMag'],
                    y*self.biomeData['swampMag'],
                    base=int(self.noiseData['seed']),
                ),-1,1,0,100)
                # row.append(n >= 60)
                row.append(n)
            m.append(row)
        return m

    def weight(self,weight,v1,v2):
        return int((v1*weight)+(v2*(1-weight)))




root = Tk()
root.geometry('%sx%s'%(W,H))
root.title("Terrain (preset: %s)"%sys.argv[1])
root.resizable(0,0)
root.wm_attributes('-topmost',1)

terrain = Terrain(terrainData,biomeData)

root.mainloop()
