# Shots

The following section analyzes the shot attempts during the match. 

## Goal Clips with xG Values

(adapted from snippet $440)

### 1:0 for Austria by Stefan Lainer (18') - xG value 0.297 (wyscout)
![Goal1](./code/adi_shot_snippets_all/goals/5111384_0.297_1061.mp4)

### 1:1 for North Macedonia by Goran Pandev (28') - xG value 0.404 (wyscout)
![Goal2](./code/adi_shot_snippets_all/goals/5111384_0.404_1642.mp4)

### 2:1 for Austria by Michael Gregoritsch (78') - xG value 0.194 (wyscout)
![Goal3](./code/adi_shot_snippets_all/goals/5111384_0.194_4783.mp4)

### 3:1 for Austria by Marko Arnautović (89') - xG value 0.227 (wyscout)
![Goal4](./code/adi_shot_snippets_all/goals/5111384_0.227_5498.mp4)


## xG Graphs and Comparison

(adapted from snippet $435)

For the xG graph (over match time) we get

![xGwyscout](./code/adi_xggraph_plots/xg_plot_wyscout.png)

using wyscout, and

![xGstatsbomb](./code/adi_xggraph_plots/xg_plot_statsbomb.png)

using statsbomb instead. How the two data scources vary can be seen when comparing the plots:

![xGcompare](./code/adi_xggraph_plots/xg_plot_compare.png)

## Attempt Distribution

(adapted from snippet $451)

In the following, we plot the shot attempts made by each team (AUT: red, MKD: blue). The size of the respective circle is proportional to the xG value of this attempt. A filled circle marks a goal. Player names and minute of the match can be read off directly.

Using the wyscout data, we find
![distrW](./code/adi_shots_positions/plot_shots_wyscout_zoom.png)
Alternatively, we can generate the plot using the StatsBomb data:
![distrS](./code/adi_shots_positions/plot_shots_statsbomb_zoom.png)

For completeness, the following plot shows how the plots generated from the respective data sources vary:
![distrC](./code/adi_shots_positions/plot_shots_comparison.png)


## Shot Heatmap

(adapted from snippet $480)

By essentially smoothing the discrete datapoints from the previous plots, we can also draw the corresponding heatmaps of shot attempts:

![shotheat_a](./code/adi_shots_positions/heatmap_aut.png)

![shotheat_m](./code/adi_shots_positions/heatmap_mkd.png)

## Individual Shot Statistics

(adapted from snippet $444)

By querying the players who attempted a shot during the match, we can get the individual shot statistics for those players. Note that here, accuracy measures the proportion of attempts that are on target, and expected goals represents the cumulated xG value of a player.

### Austria

 |Player|Total shots|Shots on goal|Goals|Accuracy|Expected goals|
|---|---|---|---|---|---|
|Stefan Lainer|1|1|1|100.0%|0.16|
|Xaver Schlager|1|0|0|0.0%|0.05|
|Marcel Sabitzer|2|0|0|0.0%|0.07|
|Sasa Kalajdzic|2|1|0|50.0%|0.2|
|Christoph Baumgartner|1|1|0|100.0%|0.04|
|Michael Gregoritsch|2|2|1|100.0%|0.42|
|Marko Arnautović|1|1|1|100.0%|0.46|
|**Team**|10|6|3|60.0%|1.4|

### North Macedonia

|Player|Total shots|Shots on goal|Goals|Accuracy|Expected goals|
|---|---|---|---|---|---|
|Stefan Ristovski|1|0|0|0.0%|0.02|
|Boban Nikolov|2|1|0|50.0%|0.16|
|Ezgjan Alioski|1|0|0|0.0%|0.02|
|Eljif Elmas|1|0|0|0.0%|0.08|
|Goran Pandev|2|1|1|50.0%|0.41|
|**Team**|7|2|1|28.57%|0.69|

## Possession Before Shot

(adapted from snippet $439)

Going back to passing, we can also query the possession sequences immediately before a team scored. For the four goals of this match, they look as follows:

### 1:0 for Austria by Stefan Lainer (18') - xG value 0.297 (wyscout)
![g1-p](./code/adi_possession_chain_plots/goal01.png)

### 1:1 for North Macedonia by Goran Pandev (28') - xG value 0.404 (wyscout)
![g2-p](./code/adi_possession_chain_plots/goal02.png)

### 2:1 for Austria by Michael Gregoritsch (78') - xG value 0.194 (wyscout)
![g3-p](./code/adi_possession_chain_plots/goal03.png)

### 3:1 for Austria by Marko Arnautović (89') - xG value 0.227 (wyscout)
![g4-p](./code/adi_possession_chain_plots/goal04.png)

The full interactive map (for passing sequences prior to each attempt made) can be found [in this HTML file](./code/adi_possession_chain_plots/possession.html). 

## Other Snippets / Extensions

TBD

## Other Suggestions from Slides

TBD