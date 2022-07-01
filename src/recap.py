import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
import jsonRW
import extra



class Weeks:

    def __init__(self, folder):
        self.folder = folder

        # Defining json to hold Weeks data
        json = jsonRW.read_json(folder)
        
        # Defining an empty list to hold strings that represent file locations
        weeks_files = []

        # For Loop to create strings that represent the file location of exported .csv files from Notion
        for x in range(1, 16):
            try:
                file = f"../weeks_data/{folder}/Week{str(x)}.csv"
                weeks_files.append(file)
            except:
                continue

        # Defining an empty list to hold Pandas Dataframe of the previously mentioned Notion .csv files
        self.weeks_df = []

        # For Loop to create, and clean multipe Dataframes to represent a week
        for x in range(15):
            try:
                df = pd.read_csv(weeks_files[x])
                time = pd.DataFrame(extra.military_time())
                df = df.drop(df.columns[[0]], axis=1)
                df = pd.concat([time, df], axis=1)
                df.set_index([0])
                df.replace(jsonRW.read_class_link(folder))
                self.weeks_df.append(df.fillna("Unknown"))
            except:
                continue

    def create_actions(self):

        # Defining an empty dictionary to file actions as keys and the number of times an action occured as its value (an action is an entry into a 15 minute block)
        actions = {}

        # Three Nested For Loops to collect all action in a day, for each day, for each week
        for x in self.weeks_df:
            for y in extra.week:
                for z in x[y]:
                    if actions.get(z) != None:
                        actions.update({z: (actions.get(z) + 1)})
                    else:
                        actions.update({z: 1})

        # Cleaning dictionary keys to translate from Notion hyperlinks to actual classes
        classes = jsonRW.read_class_link(self.folder)
        for x in classes:
            num = actions.get(x)
            actions.pop(x)
            act = classes.get(x)
            actions.update({act: num})

        total_actions = 0
        for x in actions:
            total_actions = total_actions + actions.get(x)

        analysis = {"actions":actions, "total_actions":total_actions}
        jsonRW.write_analysis(self.folder, analysis)

    # I/O Function to do Level One classification
    def level_one(self):
        print("Level One Classification \n Type: s for Sleep, w for Work, l for Life, or f for Food")
        # Level One: Classifying actions into three categories: Sleep, Work, Life, Food
        sleep = []
        work = []
        life = []
        food = []
        dict = jsonRW.read_json(self.folder)
        for x in dict['analysis']['actions']:
            print("Action to categorize: " + x)
            l1_cat = input("Classification: ")
            if l1_cat in ["s", "w", "l", "f"]:
                if l1_cat == "s":
                    sleep.append(x)
                if l1_cat == "w":
                    work.append(x)
                if l1_cat == "l":
                    life.append(x)
                if l1_cat == "f":
                    food.append(x)
        level_one = {"sleep":sleep, "work":work, "life":life, "food":food}
        jsonRW.write_level(self.folder, "level_one", level_one)
        


# [average_week(weeks_list)] returns a Pandas DataFrame of an 'average' week in which each time entry for each day is a list of all the actions done at that time, on that day through all
#   the weeks.  [weeks_list] must be a list of Pandas DataFrames.


def average_week(weeks_list, empty):
    for x in weeks_list:
        for y in extra.week:
            for z in range(0, 96):
                value = x.loc[z, y]
                (empty.loc[z, y]).append(value)
    return(empty)


# [average_week_cat(weeks_list, cat_dict)] returns a Pandas DataFrame of an 'average' week in which each time entry for each day is a list of the certain type of actions
#   that take place at the time, on that day through all the weeks given in [weeks_list].  [weeks_list] must be a list of Pandas DataFrames.  [cat_dict] must be a dictionary where
#   the keys are action categories, and the values are lists of actions in that category.


def average_week_cat(weeks_list, empty, cat_dict):
    for x in weeks_list:
        for y in extra.week:
            for z in range(0, 96):
                value = x.loc[z, y]
                for w in cat_dict:
                    if value in (cat_dict.get(w)):
                        value = w
                (empty.loc[z, y]).append(value)
    return(empty)

# I/O Function to do Level Two classification


def level_two_work(w_list):
    print("Level Two Classification \n For Work: 3610 for AEP 3610, 3330 for AEP 3330, 3110 for CS 3110, 3112 for GOVT 3112, 3281 for LAW 3281, pp for Purple Pill, 4200 for AEP 4200, pi for PIKE, gen for General")
    aep3610 = []
    aep3330 = []
    cs3110 = []
    govt3112 = []
    law3281 = []
    pp = []
    aep4200 = []
    pike = []
    general = []
    no_cat = []
    for x in w_list:
        print("Action to categorize: " + x)
        cat = input("Classification: ")
        if cat in ["3610", "3330", "3110", "3112", "3281", "pp", "4200", "pi", "gen"]:
            if cat == "3610":
                aep3610.append(x)
            if cat == "3330":
                aep3330.append(x)
            if cat == "3110":
                cs3110.append(x)
            if cat == "3112":
                govt3112.append(x)
            if cat == "3281":
                law3281.append(x)
            if cat == "pp":
                pp.append(x)
            if cat == "4200":
                aep4200.append(x)
            if cat == "pi":
                pike.append(x)
            if cat == "gen":
                general.append(x)
        else:
            no_cat.append(x)
    print(aep3610)
    print(aep3330)
    print(cs3110)
    print(govt3112)
    print(law3281)
    print(pp)
    print(aep4200)
    print(pike)
    print(general)
    print(no_cat)

# Level Two Classification for Life


def level_two_life(l_list):
    print("Level Two Classification \n When given an action, type category for it to be filed as.")
    act_cat = {}
    for x in l_list:
        print("Action to categorize: " + x)
        cat = input("Classification: ")
        if act_cat.get(cat) != None:
            count = act_cat.get(cat)
            count.append(x)
            act_cat.update({cat: count})
        else:
            actions_list = [x]
            act_cat[cat] = actions_list

    print(act_cat)
    return(act_cat)


def count_actions(list_list):
    for x in list_list:
        num = 0
        for y in x:
            n = actions.get(y)
            # actions.pop(y)
            if n == None:
                print(y)
            else:
                num = num + n
        print(num)


def type_data(list):
    data = []
    for x in list:
        dat = input("Give type of " + x + ": ")
        data.append(dat)
    print(data)

# [anno_pie(data, legend, title) produces a pie chart with a legend.  The pie chart percentages are based off of the numbers in [data].  [data]
#   is a list of the number of hours spent on an action.  [legend] is a list of strings mapping the action hours to an action.  [title] is the
#   title of the pie chart given as a string.]


def anno_pie(data, legend, title):

    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

    data = data
    legend = legend

    def func(pct, allvals):
        absolute = int(np.round(pct/100.*np.sum(allvals)))
        return "{:.1f}%\n({:d} hours)".format(pct, absolute)

    wedges, text, autotexts = ax.pie(
        data, autopct=lambda pct: func(pct, data), textprops=dict(color="w"))

    ax.legend(wedges, legend, title="Categories",
              loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    plt.setp(autotexts, size=8, weight="bold")
    ax.set_title(title)

    plt.show()


# [anno_donut_plot(data, anno, title) will create a donut pie chart using data for percentages, anno for the annotations, and title for the plot title]


def anno_donut_plot(data, anno, title):
    fig, ax = plt.subplots(figsize=(8, 3), subplot_kw=dict(aspect="equal"))

    wedges, texts = ax.pie(data, wedgeprops=dict(width=0.5), startangle=-40)

    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-"),
              bbox=bbox_props, zorder=0, va="center")

    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(anno[i], xy=(x, y), xytext=(
            1.35*np.sign(x), 1.4*y), horizontalalignment=horizontalalignment, **kw)

    ax.set_title(title, pad=40.0)
    plt.show()


# [bar_of_pie(pie_data, pie_anno, explode, pie_title, bar_data, bar_title, bar_legend)] returns a plot of a pie and bar chart.  [pie_data] is a list of numbers to create the
#   pie chart.  [pie_anno] is a list of string mapping each number in the previous list to a annotation.  [explode] is a list of int 0's, except for the location of the data
#   point that is going to be expanded with the bar chart.  [pie_title] is the title for the pie chart.  [bar_data] is a list of number to create the bar chart.  [bar_title]
#   is the title for the bar chart.  [bar_legend] is a tuple mapping the bar data list to the annotation for the legend.
def bar_of_pie(pie_data, pie_anno, explode, pie_title, bar_data, bar_title, bar_legend):

    # make figure anf assign axis objects
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 5))
    fig.subplots_adjust(wspace=0)

    # pie chart parameters
    tot = 0
    for x in pie_data:
        tot += x
    ratios = (np.array(pie_data) / tot).tolist()
    labels = pie_anno
    explode = explode
    # rotate so that first wedge is spliy by the x-axis
    count = 0
    num = 0
    max = 0
    for x in explode:
        if x > max:
            max = x
            num = count
        count += 1
    ang_ratio = 0
    for x in range(num):
        ang_ratio += ratios[x]
    angle = (ang_ratio * -360) + (-180 * ratios[num])
    ax1.pie(ratios, autopct='%1.1f%%', startangle=angle,
            labels=labels, explode=explode)
    ax1.set_title(pie_title)

    # bar chart parameters
    xpos = 0
    top = 1
    tot = 0
    for x in bar_data:
        tot += x
    ratios = (np.array(bar_data) / tot).tolist()
    width = 0.2
    colors = ['blue', 'lightcoral', 'limegreen', 'darkorchid',
              'palegoldenrod', 'dodgerblue', 'tomato', 'olivedrab', 'mediumpurple']

    for j in range(len(ratios)):
        length = len(ratios)
        height = ratios[j]
        ax2.bar(xpos, height, width, bottom=(top - height),
                color=colors[j])
        ypos = top - ax2.patches[j].get_height() / 2
        top -= height
        ax2.text(xpos, ypos, "%d%%" %
                 (ax2.patches[j].get_height() * 100), ha='center')

    ax2.set_title(bar_title)
    ax2.legend(bar_legend)
    ax2.axis('off')
    ax2.set_xlim(- 2.5 * width, 2.5 * width)

    # use ConnectionPatch to draw lines between the two plots
    # get the wedge data
    theta1, theta2 = ax1.patches[num].theta1, ax1.patches[num].theta2
    center, r = ax1.patches[num].center, ax1.patches[num].r
    bar_height = sum([item.get_height() for item in ax2.patches])

    # draw top connection line
    x = r * np.cos(np.pi / 180 * theta2) + center[0]
    y = r * np.sin(np.pi / 180 * theta2) + center[1]
    con = ConnectionPatch(xyA=(-width / 2, bar_height),
                          coordsA=ax2.transData, xyB=(x, y), coordsB=ax1.transData)
    con.set_color([0, 0, 0])
    con.set_linewidth(2)
    ax2.add_artist(con)

    # draw bottom connecting line
    x = r * np.cos(np.pi / 180 * theta1) + center[0]
    y = r * np.sin(np.pi / 180 * theta1) + center[1]
    con = ConnectionPatch(xyA=(-width / 2, 0),
                          coordsA=ax2.transData, xyB=(x, y), coordsB=ax1.transData)
    con.set_color([0, 0, 0])
    con.set_linewidth(2)
    ax2.add_artist(con)

    plt.show()
