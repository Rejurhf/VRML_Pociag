import originalGenerator


# Generator main function
def generateVRMLString():
  # Init
  strVRML = '#VRML V2.0 utf8\n'

  # Add Green Plane
  strVRML += originalGenerator.getPlane()

  # Add Train Tracks Underlay
  strVRML += originalGenerator.getTrainTracksUnderlay(-100, 0.1, 0)

  # Add Railways
  strVRML += originalGenerator.getRailways()

  # Add Viewpoints
  strVRML += originalGenerator.getViewpoints(-100, 0)

  # Add Random Trees
  strVRML += originalGenerator.getRandomTrees(100, 'tree1.wrl')
  strVRML += originalGenerator.getRandomTrees(90, 'tree2.wrl')
  strVRML += originalGenerator.getRandomTrees(160, 'tree3.wrl')

  # Add Terrain
  strVRML += originalGenerator.getTerrain(130, 'terrain1.wrl')

  # Add Train
  strVRML += originalGenerator.getTrain()
  
  return strVRML

# Write to file
def writeToFile(str, fileName):
  print('Write to file', fileName)
  fileVRML = open(fileName, 'w')
  fileVRML.write(str)
  fileVRML.close()

# Main
if __name__ == '__main__':
  print('Start')

  # Init
  strVRML = generateVRMLString()

  # Write
  writeToFile(strVRML, 'model.wrl')

  print('End')
