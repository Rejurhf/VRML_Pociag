import originalGenerator
import math


def getPlane(x, y, z):
  print('Get Green Plane')
  return ('\n# Green Plane\n'
    'Shape {\n'
    '  appearance Appearance { material Material { diffuseColor 0 1 0 } }\n'
    '  geometry Box { size ' + '{} {} {}'.format(x, y, z) + '}\n'
    '}\n')


def defineTrainTracksUnderlayShape(underlayName):
  print('Define Train Tracks Underlay object', )
  outStr = '\n# Train Tracks Underlay Object Definition\n'
  outStr += ('Transform {\n'
    ' translation 0 -1 0\n'
    ' children [\n'
    '   DEF ' + underlayName +' Shape {\n'
    '     appearance Appearance {\n'
    '       material Material { diffuseColor 1 0.5 0.25 }\n'
    '     }\n'
    '     geometry Box {\n'
    '       size 0.3 0.2 2.5\n'
    '     }\n' 
    '   }\n'
    ' ]\n' 
    '}\n')
  return outStr, underlayName


def find_center(x1, y1, x2, y2, angle):
  # Slope of the line through the chord
  slope = (y1-y2)/(x1-x2)

  # Slope of a line perpendicular to the chord
  new_slope = -1/slope

  # Point on the line perpendicular to the chord
  # Note that this line also passes through the center of the circle
  xm, ym = (x1+x2)/2, (y1+y2)/2

  # Distance between p1 and p2
  d_chord = math.sqrt((x1-x2)**2 + (y1-y2)**2)

  # Distance between xm, ym and center of the circle (xc, yc)
  d_perp = d_chord/(2*math.tan(angle))

  # Equation of line perpendicular to the chord: y-ym = new_slope(x-xm)
  # Distance between xm,ym and xc, yc: (yc-ym)^2 + (xc-xm)^2 = d_perp^2
  # Substituting from 1st to 2nd equation for y,
  #   we get: (new_slope^2+1)(xc-xm)^2 = d^2

  # Solve for xc:
  xc = (d_perp)/math.sqrt(new_slope**2+1) + xm

  # Solve for yc:
  yc = (new_slope)*(xc-xm) + ym

  return round(xc, 4), round(yc, 4)


def generatePositionList(x1, y1, z1, r1, x2, y2, z2, r2):  
  # Get number of elements to create
  numOfElem = max(abs(x2-x1), abs(y2-y1), abs(z2-z1)) * 2
  # Get elem delta
  dX, dY, dZ, dR = (x2-x1)/numOfElem, (y2-y1)/numOfElem, (z2-z1)/numOfElem, (r2-r1)/numOfElem 
  posList = []

  # Calculate angle for radius
  # Distance between points
  dist = math.sqrt((x2-x1)**2+(z2-z1)**2)
  # radius/distance from center to points
  radius = abs(x2-x1) if abs(x2-x1) > abs(z2-z1) else abs(z2-z1)
  p = dist/2 + radius
  area = math.sqrt(p*(p-radius)*(p-radius)*(p-dist))
  angle = math.asin((2*area)/(radius*radius))
  # Get center of circle
  xC, zC = find_center(x1, z1, x2, z2, angle)

  # get start angle
  startAngle = math.acos((x1 - xC)/radius)

  # Generate positions
  for i in range(numOfElem+1):
    posList.append((x1+(dX*i), y1+(dY*i), z1+(dZ*i), r1+(dR*i)))
  
  return posList



def getTrainTracksUnderlay(x1, y1, z1, r1, x2, y2, z2, r2, underlayName='', desc=''):
  print('Get Train Tracks Underlay', desc)
  outStr = '\n# Train Tracks Underlay {}\n'.format(desc)

  # Generate list of underlay positions
  posList = generatePositionList(x1, y1, z1, r1, x2, y2, z2, r2)

  if underlayName:
    for e in posList:
      outStr += ('Transform {\n'
        ' translation ' + '{} {} {}'.format(e[0], e[1], e[2]) + '\n'
        ' rotation 0 1 0 ' + str(e[3]) + '\n'
        ' children [ USE ' + underlayName + ' ]\n' 
        '}\n')
  else:
    for e in posList:
      outStr += ('Transform {\n'
        ' translation ' + '{} {} {}'.format(e[0], e[1], e[2]) + '\n'
        ' children [\n'
        '   Shape {\n'
        '     appearance Appearance { material Material { diffuseColor 1 0.5 0.25 } }\n'
        '     geometry Box { size 0.3 0.2 2.5 }\n' 
        '   }\n'
        ' ]\n' 
        '}\n')

  return outStr


# Generator main function
def generateVRMLString():
  # Original generator - to use it comment all other lines
  # strVRML = originalGenerator.generateOriginalModel()

  # Init
  strVRML = '#VRML V2.0 utf8\n'

  # Add Green Plane
  strVRML += getPlane(100, 0.05, 100)

  # Train Tracks Underlay
  # Define underlay object
  tmpStr, underlayName = defineTrainTracksUnderlayShape('underlay')
  strVRML += tmpStr
  # Add underlay (x1, y1, z1, r1, x2, y2, z2, r2, underlayName='', desc='') r1/r2 - rotation in radian (Y axis)
  strVRML += getTrainTracksUnderlay(-10, 0.1, -10, 0, 10, 0.1, 15, -1.57, underlayName, 'opis')

  # Add Viewpoints
  strVRML += originalGenerator.getViewpoints(0, 0)
  
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
