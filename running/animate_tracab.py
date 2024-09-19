import bz2
import os
import shutil
import moviepy.video.io.ImageSequenceClip as moviepy
import pandas as pd
import json
import xml.etree.ElementTree as ET
from time import time
from os.path import exists
import mplsoccer as mpls
import matplotlib.pyplot as plt
from tqdm.auto import tqdm

# --- Plotting params --- #
colors = ['#db2c2c', '#2e68c7'] # define colors of your teams [home, away]

plt.rcParams.update({'font.family': 'sans-serif'})
plt.rcParams.update({'font.sans-serif': 'yu gothic'})
plt.rcParams.update({'font.size': 20})
plt.rcParams.update({'mathtext.fontset': 'dejavuserif'})
plt.rcParams.update({'figure.autolayout': True})

figsize = {'horiz': (17, 12), 'vert': (12, 17)}

# --- Class for data import (based on snippet $??? but adapted) --- #
class Tracab:

    provider = 'tracab'
    pitch_dims = (2*5250, 2*3400)

    def __init__(self, path, team_names, competition_stage, xy_only=False):

        self.path = path
        self.teams = team_names
        self.competition_stage = competition_stage
        self.match_folder = '../running/'           # path+competition_stage+'/'+team_names[0]+' v '+team_names[1]+'/'
        self.match_name = team_names[0]+' v '+team_names[1]

        tic = time()

        if xy_only and exists(self.match_folder+'xy.csv'):
            self.XY = pd.read_csv(self.match_folder + 'xy.csv', parse_dates=[0])
            self.obj_info = self.get_obj_info()
        else:
            match = self.load_match()
            self.matchID = int(match.attrib['id'])
            self.matchNr = int(match.attrib['matchNumber'])
            assert int(match[1].attrib['pitchLength']) == self.pitch_dims[0]
            assert int(match[1].attrib['pitchWidth']) == self.pitch_dims[1]
            self.phases = [self.Phase(phase) for phase in match[2]]
            self.frames = [self.Frame(frame) for frame in match[3]]
            self.standardize_data()
            self.obj_info = self.get_obj_info()
            self.XY = self.position_dfs()

        toc = time()
        print(f"Loading the Tracab data took {toc - tic} seconds.")

    def load_match(self):
        return ET.parse('dataAvN.xml').getroot()[0]

    def standardize_data(self):
        """Removes frames which lie outside the playing time
        and puts teams always on the same side of the pitch"""
        standardized_frames = []
        for frame in self.frames:
            for phase in self.phases:
                if phase.start <= frame.time <= phase.end:
                    if phase.leftTeamID != self.phases[0].leftTeamID:
                        for obj in frame.trackingObjs:
                            obj.x *= -1
                            obj.y *= -1
                    standardized_frames.append(frame)
                    break
        self.frames = standardized_frames

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
            self.trackingObjs = [self.TrackingObj(obj) for obj in frame[0]]

        class TrackingObj:
            def __init__(self, obj):
                self.type = obj.attrib['type']
                self.id = obj.attrib['id']
                self.x = int(obj.attrib['x'])
                self.y = int(obj.attrib['y'])
                self.sampling = obj.attrib['sampling']

    def get_obj_info(self):
        if exists('obj_info.json'):
            f = open('obj_info.json','r')
            obj_info = json.load(f)
        else:
            obj_info = {}
            for frame in self.frames:
                for obj in frame.trackingObjs:
                    if obj.id not in obj_info.keys():
                        obj_info[obj.id]['type'] = obj.type
                    else:
                        continue
            with open('obj_info.json', 'w') as f:
                json.dump(obj_info, f, indent=4)
        return obj_info

    def position_dfs(self):

        columns = ['time', 'ballInPlay', 'ballPossession'] + \
                  [id+'.x' for id in self.obj_info.keys()] + \
                  [id+'.y' for id in self.obj_info.keys()]
        index = list(range(len(self.frames)))

        xy = pd.DataFrame(columns=columns, index=index)

        for i, frame in enumerate(self.frames):
            xy.at[i, 'time'] = frame.time
            xy.at[i, 'ballInPlay'] = frame.ballInPlay
            xy.at[i, 'ballPossession'] = frame.ballPossession
            for obj in frame.trackingObjs:
                xy.at[i, obj.id+'.x'] = obj.x
                xy.at[i, obj.id+'.y'] = obj.y

        xy.to_csv(self.match_folder+'xy.csv', index=False)
        xy = pd.read_csv(self.match_folder + 'xy.csv', parse_dates=[0])
        return xy


# --- Functions to (1) draw a football pitch, (2) plot static player locations and (3) combine many of these images into a video --- #
def draw_pitch(data, orientation):

    if orientation in ['horiz', 'horizontal']:
        create_pitch = mpls.Pitch
        orientation = 'horiz'
    elif orientation in ['vert', 'vertical']:
        create_pitch = mpls.VerticalPitch
        orientation = 'vert'

    pitch = create_pitch(pitch_type='tracab', pitch_color='#aabb97', line_color='white', stripe_color='#c2d59d',
                         stripe=True, pitch_length=data.pitch_dims[0] / 100, pitch_width=data.pitch_dims[1] / 100, linewidth=4, spot_scale=0.004)
    fig, ax = pitch.draw(figsize=figsize[orientation])
    return fig, ax


def freeze_frame(tracab, time=None, show=True):

    frame = tracab.XY.loc[tracab.XY['time'] == time]
    fig, ax = draw_pitch(tracab, 'vert')

    for id in tracab.obj_info:
        obj = tracab.obj_info[id]
        if obj['type'] == '7':
            # ball
            color = 'white'
            markersize = 20
            txt = ''
        else:
            # player; type 0: home team, type 1: away team
            color = colors[int(obj['type'])]
            markersize = 50
            txt = obj['jersey number']

        loc = (frame[id+'.x'], frame[id+'.y'])
        ax.plot(loc[1], loc[0], marker='o', color=color,
                markersize=markersize, alpha=0.8, ls='', markeredgecolor=color, markeredgewidth=1)
        ax.annotate(txt, (loc[1], loc[0]), size=25, color='white', ha='center', va='center', weight='bold')

    if show:
        plt.show()
    return fig


def animate_tracab(tracab, start, end):
    # Series of all the timestamps to plot
    start, end = pd.to_datetime(start), pd.to_datetime(end)
    timestamps = tracab.XY['time'].loc[(start <= tracab.XY['time']) & (tracab.XY['time'] <= end)]
    # create folder for pngs
    path = tracab.match_folder + "video_buf/"
    try:
        os.mkdir(path)
    except OSError:
        print("Directory %s already exists." % path)
    else:
        print("Successfully created the directory %s." % path)
    # save freeze frame for each timestamp as png
    print("Create and save freeze frames...")
    for i, timestamp in enumerate(tqdm(timestamps)):
        fig = freeze_frame(tracab, time=timestamp, show=False)
        plt.figure(fig.number)
        img_name = "000000" + str(i)
        img_name = img_name[-6:]
        img_path = path + img_name + ".png"
        plt.savefig(img_path)
        plt.close()
    print("Combine freeze frames into video...")
    # combine all the created pngs into a video
    image_files = [path + img for img in os.listdir(path) if img.endswith(".png")]
    clip = moviepy.ImageSequenceClip(image_files, fps=25)
    clip.write_videofile(tracab.match_folder+str(time())[:8]+'.mp4')
    shutil.rmtree(path, ignore_errors=False, onerror=None)


# --- Create the tracab object and call the necessary functions
# it is assumed that the tracab data can be found at a location like "data/tracab/Group Stage/Denmark v Finland/"
tracab = Tracab("../data/tracab/",
                ['Austria', 'North Macedonia'],
                'Group Stage', 
                xy_only=True   # after importing the full data successfully once, this can be changed to "True" to speed up the future import process considerably
                )

# by default, video will be created using a vertical pitch orientation - if desired otherwise, the corresponding settings in "draw_pitch()" need to be changed
video_dimensions = figsize = {'horiz': (17, 12), 'vert': (12, 17)}

# define at which timestamps the video shall start and end
video_start_timestamp = '2021-06-13T16:06:17.293Z'
video_end_timestamp = '2021-06-13T16:06:17.853Z'
# start animation, video will be saved in current folder
# caution: animation can take multiple times the real game time, i.e. animating one minute of the match might take up to 10-20 min
animate_tracab(tracab, start=video_start_timestamp, end=video_end_timestamp)
