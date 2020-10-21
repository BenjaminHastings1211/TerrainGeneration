# TerrainGeneration
Requirements:<br/>
Noise -> ```pip3 install noise```<br/>

To run:<br/>

In terminal or cmd use terrain.py [presetname] to run the program with a specific preset<br/>

Ex in terminal)<br/>

```
python3 terrain.py swamps
```
<br/>

Presets:<br/>

Presets can be created using the following syntax<br/>

normal                (name of preset)<br/>
screen -> 800         (size of window)<br/>
cells -> 400          (number of cells per row and column)<br/>
seed -> random        (seed for the noise generator, can be a number or 'random')<br/>
mag -> 0.015          (the magnitude of the perlin noise, lower number = flatter terrain)<br/>
extraMag -> 0.045     (the magnitude of the second layer of perlin noise)<br/>
weight -> 0.75        (a percentage used when finding the weighted average of the two noise maps)<br/>
passes -> 2           (passes made by the noise function, only 1 or 2 is needed)<br/>
sea -> 47             (sea level for the terrain)<br/>
fp -> 100             (freezing point)<br/>
moutain -> 80         (the level where mountains will begin to appear)<br/>
outline -> False      (if the tiles should be outlined in black or not)<br/>

--                    (end with a '--' to declare the end of a preset)<br/>
