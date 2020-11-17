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


def find_center(x1, y1, x2, y2, angle, r1, r2):
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
  # get center on the right side
  div = -2 if (round(r1%(2*math.pi),4)==0 or round(r2%(2*math.pi),4)==round(math.pi,4)) else 2
  if r2 - r1 < 0:
    div = -div
  
  d_perp = round(d_chord/(2*math.tan(angle/div)), 4)

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
  radius = round(dist/(2*math.sin(angle/2)), 4) if 2*math.sin(angle/2) != 0 else 0
  
  if r1 == r2:
    # Go straight
    tmpNumOFElem = round(numOfElem*0.7)
    dX, dZ = (x2-x1)/tmpNumOFElem, (z2-z1)/tmpNumOFElem
    for i in range(tmpNumOFElem+1):
      posList.append((x1+(dX*i), y1, z1+(dZ*i), r2))
  else:
    # Go in circle
    # Get center of circle
    xC, zC = find_center(x1, z1, x2, z2, angle, r1, r2)

    # get start angle
    startAngle = round(math.acos((x1 - xC)/radius), 4)
    dAngle = round((math.acos((x2 - xC)/radius) - startAngle)/numOfElem, 4)

    # print('-- center ({},{}), radius {}, angle {}, startAngle {}, dAngle {}'.format(xC, zC, radius, angle, startAngle, dAngle))
    # Generate positions
    for i in range(numOfElem+1):
      if round(r1%(2*math.pi), 4) == 0 or round(r2%(2*math.pi), 4) == 0:
        newX = round(xC+(radius*math.cos(startAngle+(dAngle*i))), 4)
        newZ = round(zC+(radius*math.sin(startAngle+(dAngle*i))), 4)
      else:
        newX = round(xC+(radius*math.cos(-startAngle-(dAngle*i))), 4)
        newZ = round(zC+(radius*math.sin(-startAngle-(dAngle*i))), 4)
      newY = round(y1+(dY*i), 4)
      newR = round(r1+(dR*i), 4)

      posList.append((newX, newY, newZ, newR))
  
  return posList


def getTrainTracks(x1, y1, z1, r1, x2, y2, z2, r2, trainTrackName=''):
  print('Get Train Track')
  outStr = '\n# Train Track\n'

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


def createRailWaysFromPoints(pointList, trainTrackName):
  outStr = ''
  for i in range(len(pointList)-1):
    print(i, pointList[i], pointList[i+1])
    # Add Train Track (x1, y1, z1, r1, x2, y2, z2, r2, trainTrackName='') r1/r2 - rotation in radian (Y axis)
    outStr += getTrainTracks(pointList[i][0], pointList[i][1], pointList[i][2], pointList[i][3], pointList[i+1][0], pointList[i+1][1], pointList[i+1][2], pointList[i+1][3], trainTrackName)
  
  return outStr


# Generator main function
def generateVRMLString():
  # Original generator - to use it comment all other lines
  # strVRML = originalGenerator.generateOriginalModel()

  # Init
  strVRML = '#VRML V2.0 utf8\n'

  # Add Green Plane
  strVRML += getPlane(200, 0.05, 200)

  # Train Tracks
  # Define Train Track object
  tmpStr, trainTrackName = defineTrainTrackGroup('traintrack')
  strVRML += tmpStr

  # Declare rounded pi
  pi = round(math.pi, 4)
  # Path to generate (x, y, z, r)
  # pointList = [(30, 0.1, 10, 0), (40, 0.1, 0, pi/2), (30, 0.1, -10, pi), (20, 0.1, -20, pi/2), \
  #   (20, 0.1, -30, pi/2), (10, 0.1, -40, pi), (0, 0.1, -40, pi), (-10, 0.1, -30, 3/2*pi), \
  #   (-10, 0.1, -10, 3/2*pi), (-20, 0.1, 0, pi), (-30, 0.1, 0, pi), (-40, 0.1, 10, 3/2*pi), \
  #   (-40, 0.1, 30, 3/2*pi), (-30, 0.1, 40, 2*pi), (-10, 0.1, 40, 2*pi), (0, 0.1, 30, 5/2*pi), \
  #   (0, 0.1, 20, 5/2*pi), (10, 0.1, 10, 2*pi), (30, 0.1, 10, 2*pi)]
  
  pointList = [(-30, 0.1, 80, pi), (-80, 0.1, 30, pi/2), (-80, 0.1, -20, pi/2), (-60, 0.1, -40, 0), \
    (-40, 0.1, -20, -pi/2), (-40, 0.1, 50, -pi/2), (-20, 0.1, 70, 0), (60, 0.1, 70, 0), \
    (70, 0.1, 60, pi/2), (60, 0.1, 50, pi), (10, 0.1, 50, pi), (0, 0.1, 40, pi/2), \
    (10, 0.1, 30, 0), (70, 0.1, 30, 0), (80, 0.1, 20, pi/2), (70, 0.1, 10, pi), \
    (40, 0.1, 10, pi), (-20, 0.1, -50, pi/2), (-20, 0.1, -60, pi/2), (10, 0.1, -90, 0), \
    (60, 0.1, -40, -pi/2), (80, 0.1, -20, 0), (90, 0.1, -10, -pi/2), (90, 0.1, 60, -pi/2), \
    (70, 0.1, 80, -pi), (-30, 0.1, 80, -pi)]
  strVRML += createRailWaysFromPoints(pointList, trainTrackName)

  # Add Viewpoints
  strVRML += originalGenerator.getViewpoints(-20, 0)
  
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
