import random

# Get Green Plane
def getPlane():
  print('Get Green Plane')
  return ('\n# Green Plane\n'
    'Shape {\n'
    '  appearance Appearance { material Material { diffuseColor 0 1 0 } }\n'
    '  geometry Box { size 200 0.05 50 }\n'
    '}\n')

# Get Train Tracks Underlay
def getTrainTracksUnderlay(x, y, z):
  print('Get Train Tracks Underlay')
  outStr = '\n# Train Tracks Underlay\n'
  while x <= 100:
    outStr += ('Transform {\n'
      ' translation ' + '{} {} {}'.format(x, y, z) + '\n'
      ' children [\n'
      '   Shape {\n'
      '     appearance Appearance { material Material { diffuseColor 1 0.5 0.25 } }\n'
      '     geometry Box { size 0.3 0.2 2.5 }\n' 
      '   }\n'
      ' ]\n' 
      '}\n')
    x += 0.5;

  return outStr

# Get Railways
def getRailways():
  print('Get Railways')
  zList = [-1, 1]
  outStr = '\n# Railways\n'
  for z in zList:
    outStr += ('Transform {\n'
      '  translation 0 0.3 ' + str(z) + '\n'
      '  children [\n'
      '    Shape {\n'
      '      appearance Appearance { material Material { diffuseColor 0.25 0.25 0.25 } }\n'
      '      geometry Box { size 200 0.2 0.1  }\n'
      '    }\n'
      '  ]\n' 
      '}\n')
  
  return outStr

# Get Viewpoints
def getViewpoints(x, i):
  print('Get Viewpoint')
  outStr = '\n# Viewpoints\n'
  while x <= 100:
    outStr += ('Viewpoint {\n'
      ' position ' + str(x) + ' 40 40\n'
      ' orientation 1 0 0 -0.785\n'
      ' description \"nr_' + str(i) + '\"\n'
      '}\n')
    x += 10
    i += 1

  return outStr

# Get Random Trees
def getRandomTrees(count, modelName):
  print('Get Random Trees', count, modelName)
  outStr = '\n# Get Random Trees\n'

  for i in range(count):
    x = random.randint(-100, 100)

    if random.randint(0, 1):
      z = 5 + random.randint(0, 20)
    else:
      z = -5 - random.randint(0, 20)

    outStr += ('Transform {\n'
      ' translation ' + str(x) + ' 0 ' + str(z) + '\n'
      ' children [\n'
      '   Inline { url \"' + modelName + '\"}\n'
      ' ]\n'
      '}\n')
  
  return outStr

# Get Terrain
def getTerrain(count, modelName):
  print('Get Terrain', count, modelName)
  outStr = '\n# Get Terrain\n'

  for i in range(count):
    x = random.randint(-100, 90)

    if random.randint(0, 1):
      z = 5 + random.randint(0, 10)
    else:
      z = -15 - random.randint(0, 10)

    outStr += ('Transform {\n'
      ' translation ' + str(x) + ' 0 ' + str(z) + '\n'
      ' children [\n'
      '   Inline { url \"' + modelName + '\"}\n'
      ' ]\n'
      '}\n')
  
  return outStr

# Get Train
def getTrain():
  print('Get Train')
  outStr = '\n# Get Train\n'
  outStr += ('DEF X TimeSensor {loop TRUE cycleInterval 10}\n'
    'DEF Y PositionInterpolator {\n'
    ' key [0, 0.5, 1]\n'
    ' keyValue [90 0 0, -90 0 0, 90 0 0]\n'
    '}\n'
    'Transform {\n'
    ' translation 0 0.9 0\n'
    ' children [\n'
    '   DEF Z Transform {\n'
    '     children [\n'
    '       Inline { url \"wagon1.wrl\"}\n'
    '     ]\n'
    '   }\n'
    ' ]\n'
    '}\n'
    'ROUTE X.fraction_changed TO Y.set_fraction\n'
    'ROUTE Y.value_changed TO Z.set_translation\n')

  return outStr

# Generate original model
def generateOriginalModel():
  # Init
  strVRML = '#VRML V2.0 utf8\n'

  # Add Green Plane
  strVRML += getPlane()

  # Add Train Tracks Underlay
  strVRML += getTrainTracksUnderlay(-100, 0.1, 0)

  # Add Railways
  strVRML += getRailways()

  # Add Viewpoints
  strVRML += getViewpoints(-100, 0)

  # Add Random Trees
  strVRML += getRandomTrees(100, 'tree1.wrl')
  strVRML += getRandomTrees(90, 'tree2.wrl')
  strVRML += getRandomTrees(160, 'tree3.wrl')

  # Add Terrain
  strVRML += getTerrain(130, 'terrain1.wrl')

  # Add Train
  strVRML += getTrain()

  return strVRML
