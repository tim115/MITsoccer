import xml.etree.ElementTree as et  # parsing XML files
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.projections import get_projection_class
from matplotlib.patches import Arc


class Match:
    def __init__(self, match):
        self.matchID = int(match.attrib['id'])
        self.matchNr = int(match.attrib['matchNumber'])
        self.date = match.attrib['dateMatch']
        self.stadiumID = int(match[1].attrib['id'])
        self.stadiumName = match[1].attrib['name']
        self.pitchLength = int(match[1].attrib['pitchLength'])
        self.pitchWidth = int(match[1].attrib['pitchWidth'])
        self.phases = match[2]
        self.frames = match[3]


def load_frames(input_path: str, output_path: str):
    tree = et.parse(input_path).getroot()
    match = Match(tree[0])

    framedict = dict()
    for index, frame in enumerate(match.frames):
        time = frame.attrib["utc"]

        columns = dict()

        for id, obj in enumerate(frame[0]):
            columns['time'] = time
            if id == 0:  # ball
                for key, value in obj.attrib.items():
                    columns["ball_" + key] = value
            else:
                for key, value in obj.attrib.items():
                    columns["player" + str(id) + "_" + key] = value
        framedict[index] = columns

    df = pd.DataFrame.from_dict(framedict, orient='index')
    df.to_parquet(output_path, index=False)


def unzip_bz2(input_path: str, output_path: str):
    import bz2

    zipfile = bz2.BZ2File(input_path)
    data = zipfile.read()
    with open(output_path, 'wb') as f:
        f.write(data)

    print(f"Unzippped '{input_path}' to '{output_path}'")


def draw_pitch():
    fig, ax = plt.subplots(figsize=(10.5, 6.8), dpi=300)

    ax.plot([0, 0], [0, 80], color="black")
    ax.plot([0, 120], [80, 80], color="black")
    ax.plot([120, 120], [80, 0], color="black")
    ax.plot([120, 0], [0, 0], color="black")
    ax.plot([60, 60], [0, 80], color="black")

    # Left Penalty Area
    ax.plot([18, 18], [62, 18], color="black")
    ax.plot([0, 18], [62, 62], color="black")
    ax.plot([18, 0], [18, 18], color="black")

    # Right Penalty Area
    ax.plot([120, 102], [18, 18], color="black")
    ax.plot([102, 102], [18, 62], color="black")
    ax.plot([102, 120], [62, 62], color="black")
    # Left 6-yard Box
    ax.plot([0, 6], [30, 30], color="black")
    ax.plot([6, 6], [30, 50], color="black")
    ax.plot([0, 6], [50, 50], color="black")
    # Right 6-yard Box
    ax.plot([114, 120], [30, 30], color="black")
    ax.plot([114, 114], [30, 50], color="black")
    ax.plot([114, 120], [50, 50], color="black")

    # Prepare Circles
    centreCircle = plt.Circle((60, 40), 8.7, color="black", fill=False)
    centreSpot = plt.Circle((60, 40), 0.8, color="black")
    leftPenSpot = plt.Circle((12, 40), 0.8, color="black")
    rightPenSpot = plt.Circle((108, 40), 0.8, color="black")

    # Draw Circles
    ax.add_patch(centreCircle)
    ax.add_patch(centreSpot)
    ax.add_patch(leftPenSpot)
    ax.add_patch(rightPenSpot)

    # Prepare Arcs
    leftArc = Arc((12, 40), height=18.3, width=18.3, angle=0,
                  theta1=310, theta2=50, color="black")
    rightArc = Arc((108, 40), height=18.3, width=18.3, angle=0,
                   theta1=130, theta2=230, color="black")

    # Goals
    ax.plot([-3, 0], [44, 44], color="black")
    ax.plot([-3, -3], [44, 36], color="black")
    ax.plot([-3, 0], [36, 36], color="black")

    ax.plot([123, 120], [44, 44], color="black")
    ax.plot([123, 123], [44, 36], color="black")
    ax.plot([123, 120], [36, 36], color="black")

    # Draw Arcs
    ax.add_patch(leftArc)
    ax.add_patch(rightArc)

    ax.set_xticks([])
    ax.set_yticks([])

    return ax


# CODE FROM SNIPPET
# Snippe $396

""" 
Simple module to convert a xml file containing data in TRACAB format to a Match object
"""


class Match:
    def __init__(self, filePath):
        match = et.parse(filePath).getroot()[0]

        self.matchID = int(match.attrib['id'])
        self.matchNr = int(match.attrib['matchNumber'])
        self.date = match.attrib['dateMatch']
        self.stadiumID = int(match[1].attrib['id'])
        self.stadiumName = match[1].attrib['name']
        self.pitchLength = int(match[1].attrib['pitchLength'])
        self.pitchWidth = int(match[1].attrib['pitchWidth'])
        self.phases = [Phase(phase) for phase in match[2]]
        self.frames = [Frame(frame) for frame in match[3]]

        self.removeExcessFrames()

    def removeExcessFrames(self):
        keep = []
        for frame in self.frames:
            for phase in self.phases:
                if frame.time >= phase.start and frame.time <= phase.end:
                    keep.append(frame)
                    break

        self.frames = keep


class Phase:
    def __init__(self, phase):
        self.start = phase.attrib['start']
        self.end = phase.attrib['end']
        self.leftTeamID = int(phase.attrib['leftTeamID'])


class Frame:
    def __init__(self, frame):
        self.time = frame.attrib['utc']
        self.ballInPlay = frame.attrib['isBallInPlay']
        self.ballPossession = frame.attrib['ballPossession']
        self.trackingObjs = [TrackingObj(obj) for obj in frame[0]]


class TrackingObj:
    def __init__(self, obj):
        self.type = obj.attrib['type']
        self.id = obj.attrib['id']
        self.x = int(obj.attrib['x'])
        self.y = int(obj.attrib['y'])
        self.sampling = obj.attrib['sampling']
