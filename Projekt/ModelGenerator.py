import originalGenerator
import math


def getPlane(x, y, z):
  print('Get Green Plane')
  return ('\n# Green Plane\n'
    'Shape {\n'
    '  appearance Appearance { material Material { diffuseColor 0 1 0 } }\n'
    '  geometry Box { size ' + '{} {} {}'.format(x, y, z) + '}\n'
    '}\n')


def defineTrainTrackGroup(trainTrackName):
  print('Define Train Track object', trainTrackName)
  outStr = '\n# Train Track Object Definition\n'
  outStr += ('Transform {\n'
    ' translation 0 -1 0\n'
    ' children [\n'
    '   DEF ' + trainTrackName + ' Group {\n'
    '     children [\n'
    '       Transform {\n'
    '         translation 0 0.1 0\n'
    '         children [\n'
    '           DEF underlay Shape {\n'
    '             appearance Appearance {\n'
    '               material Material { diffuseColor 1 0.5 0.25 }\n'
    '             }\n'
    '             geometry Box {\n'
    '               size 0.3 0.2 2.5\n'
    '             }\n'
    '           }\n'
    '         ]\n'
    '       }\n'
    '       Transform {\n'
    '         translation 0 0.3 -1\n'
    '         children [\n'
    '           DEF railway Shape {\n'
    '             appearance Appearance {\n'
    '               material Material { diffuseColor 0.25 0.25 0.25 }\n'
    '             }\n'
    '             geometry Box {\n'
    '               size 1 0.2 0.1\n'
    '             }\n'
    '           }\n'
    '         ]\n'
    '       }\n'
    '       Transform {\n'
    '         translation 0 0.3 1\n'
    '         children   [ USE railway ]\n'
    '       }\n'
    '     ]\n'
    '   }\n'
    ' ]\n'
    '}\n')
  return outStr, trainTrackName


def find_center(x1, y1, x2, y2, angle):
  # Slope of the line through the chord
  slope = (y1-y2)/(x1-x2) if x1-x2 != 0 else 0 

  # Slope of a line perpendicular to the chord
  new_slope = -1/slope if slope != 0 else 0

  # Point on the line perpendicular to the chord
  # Note that this line also passes through the center of the circle
  # Center between points
  xm, ym = (x1+x2)/2, (y1+y2)/2

  # Distance between p1 and p2
  d_chord = math.sqrt((x1-x2)**2 + (y1-y2)**2)

  # Distance between xm, ym and center of the circle (xc, yc)
  # d_perp = d_chord/(2*math.tan(angle))
  d_perp = round(d_chord/(2*math.tan(angle/-2)), 4)

  # Equation of line perpendicular to the chord: y-ym = new_slope(x-xm)
  # Distance between xm,ym and xc, yc: (yc-ym)^2 + (xc-xm)^2 = d_perp^2
  # Substituting from 1st to 2nd equation for y,
  #   we get: (new_slope^2+1)(xc-xm)^2 = d^2

  # Solve for xc:
  if y1-y2 == 0:
    xc = round(xm, 4)
    yc = round(ym + d_perp, 4)
  elif x1-x2 == 0:
    xc = round(xm + d_perp, 4)
    yc = round(ym, 4)
  else:
    xc = round((d_perp)/math.sqrt(new_slope**2+1) + xm, 4)
    yc = round((new_slope)*(xc-xm) + ym, 4)
  
  # print('(x1,y1) ({},{}), (x2,y2) ({},{}), angle {}, slope {}, new_slope {}, (xm,ym) ({},{}), d_chord {}, d_perp {}, (xc,yc) ({},{})'.format(x1, y1, x2, y2, angle, slope, new_slope, xm, ym, d_chord, d_perp, xc, yc))

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
  angle = round(r2 - r1, 4)
  radius = round(dist/(2*math.sin(angle/2)), 4)
  # radius = abs(x2-x1) if abs(x2-x1) > abs(z2-z1) else abs(z2-z1)
  # p = dist/2 + radius
  # area = math.sqrt(p*(p-radius)*(p-radius)*(p-dist))
  # angle = math.asin((2*area)/(radius*radius))
  
  # Get center of circle
  xC, zC = find_center(x1, z1, x2, z2, angle)

  # get start angle
  if x2-x1 == 0:
    startAngle = round(math.asin((z1 - zC)/radius), 4)
    dAngle = round((math.asin((z2 - zC)/radius) - startAngle)/numOfElem, 4)
  else:
    startAngle = round(math.acos((x1 - xC)/radius), 4)
    dAngle = round((math.acos((x2 - xC)/radius) - startAngle)/numOfElem, 4)

  # print('center {}, radius {}, angle {}, startAngle {}, dAngle {}'.format(xC, zC, radius, angle, startAngle, dAngle))

  # Generate positions
  for i in range(numOfElem+1):
    newX = round(xC+(radius*math.cos(startAngle+(dAngle*i))), 4)
    newY = round(y1+(dY*i), 4)
    newZ = round(zC+(radius*math.sin(startAngle+(dAngle*i))), 4)
    newR = round(r1+(dR*i), 4)

    posList.append((newX, newY, newZ, newR))
  
  return posList


def getTrainTracks(x1, y1, z1, r1, x2, y2, z2, r2, trainTrackName='', desc=''):
  print('Get Train Track', desc)
  outStr = '\n# Train Track {}\n'.format(desc)

  # Generate list of Train Tracks positions
  posList = generatePositionList(x1, y1, z1, r1, x2, y2, z2, r2)

  if trainTrackName:
    for e in posList:
      outStr += ('Transform {\n'
        ' translation ' + '{} {} {}'.format(e[0], e[1], e[2]) + '\n'
        ' rotation 0 1 0 ' + str(e[3]) + '\n'
        ' children [ USE ' + trainTrackName + ' ]\n' 
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

  # Train Tracks
  # Define Train Track object
  tmpStr, trainTrackName = defineTrainTrackGroup('traintrack')
  strVRML += tmpStr
  # Add Train Track (x1, y1, z1, r1, x2, y2, z2, r2, trainTrackName='', desc='') r1/r2 - rotation in radian (Y axis)
  strVRML += getTrainTracks(0, 0.1, 10, 0, 10, 0.1, 0, 1.57, trainTrackName, 'opis')

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
