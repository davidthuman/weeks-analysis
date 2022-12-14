# Weekly Schedule Analysis

## Introduction

When double majoring in Engineering Physics and Computer Science, while obtaining a minor in Public Policy, TAing an upperclassman math course, and being the Vice President of a fraternity, attention to detail, time management, and organization are the only way to stay afloat.

Most people at least flirt with the idea of creating a planner, schedule, or to-do list. When you become more involved in college, whether that be on the academic, professional, or club level, the amount of tasks that become spreadout among many areas of your life become too much to simply keep track of in your head. This is where a planner becomes essential to the productivity of a person's life.

My first prototype to keep myself organized was a simple to-do list during finals week.

![My Planning Prototype was a simple whiteboard with my classes weekly homework due days, my prelim schedule, and a section for tracking my workouts.](/prototype.png "Planning Prototype")

During my junior year at Cornell University, I created an optimized system.

## Data Collection

I created my planner through an application called Notion. "Notion is a note-taking software platform designed to help members of companies or organizations manage their knowledge for greater efficiency and productivity" (Wikipedia, 2022). However, Notion is not only a note-taking app. It is loaded with a multitude of features and data structures that can be combined in an infinite number of ways. For me, it was used to organize my life, down to level of every 15-minutes.

As was natural to my work process, I decided to look at my life a week at a time. To do this, I created a Week template page that can be created every Monday with a single click. There are three main components to my Week page:

* Global Assignment database
* Daily To-Do list
* Weekly Schedule

The Global Assignment database houses all assignments that need to be completed throughout the semester. Each assignment has an associated name, class, due date, type, weekday, and status. Assignments are sorted by due date and status to push assignments that have upcoming due dates that have not yet been completed. This table-view of the database is present in all Week pages.

![The Global Assignment database houses all assignments that need to be completed throughout the semester. Each assignment has an associated name, class, due date, type, weekday, and status. Assignments are sorted by due date and status to push assignments that have upcoming due dates that have not yet been completed. This table-view of the database is present in all Week pages.](/Notion_Assignments.png "Global Assignment Database")

The Daily To-Do list allows me to specify which assignments or task I will complete each day throughout the week. It is also a change to remind me to keep good habits, like working out or study for classes.

![The Daily To-Do list allows me to specify which assignments or task I will complete each day throughout the week. It is also a change to remind me to keep good habits, like working out or study for classes.](/Notion_ToDo.png "Daily To-Do list")

My Weekly Schedule is a table that breaks each day of the week into 15-minute blocks. As I created my Week pages from a template, all my classes and repeat meetings are already placed into the table. The rest of the blocks can be filled out by myself as they happen or in an attempt to schedule for the future. Most of the time, the schedule was used to track my actions rather than to guide me throughout the day.

![My Weekly Schedule is a table that breaks each day of the week into 15-minute blocks. As I created my Week pages from a template, all my classes and repeat meetings are already placed into the table. The rest of the blocks can be filled out by myself as they happen or in an attempt to schedule for the future.](/Notion_Schedule.png "Time Schedule")

Luckily for me, Notion has a lot of export options for all of their data structures and pages. So at the end of the semester, I am able to export my Weekly Schedule into a CSV file for processing.

## Source Code

`class Weeks` housed all the functions that are used to process the data.

`populate(folder)` will create a list of Pandas DataFrame to hold all the CSV tables data that is exported from Notion.

`create_actions()` will create an `analysis` dictionary that holds an `actions` dictionary, where the keys are actions that have been done in a 15-minute block and the values are the number of times that action has been done over the semester. `analysis` will also hold to total number of actions, for a sanity check on the data processing. The function will also write this dictionary into a JSON file that will hold all the processed data for a semester.

`level_one()` is an I/O function to do "Level One" categorization (Action Categorization will be discussed in the next section). It will loop through all the actions and ask what type of category this action is a part of. This information will be saved to the semester's JSON file.

`level_two()` is an I/O function to do "Level Two" categorization. This information will be saved to the semester's JSON file.

`level_three()` is an I/O function to do "Level Three" categorization. This information will be saved to the semester's JSON file.

`analysis_one()` will use the categorization data and the action counts to calculate time totals for each "Level One" categorization. This information will be saved to the semester's JSON file.

`analysis_two()` will use the categorization data and the action counts to calculate time totals for each "Level Two" categorization. This information will be saved to the semester's JSON file.

`analysis_three()` will use the categorization data and the action counts to calculate time totals for each "Level Three" categorization. This information will be saved to the semester's JSON file.

`anno_pie(data, legend, title)` produces a pie chart with a legend.  The pie chart percentages are based off of the numbers in `data`.  `data` is a list of the number of hours spent on an action.  `legend ` is a list of strings mapping the action hours to an action.  `title` is the title of the pie chart given as a string.

`anno_donut_plot(data, anno, title)`  will create a donut pie chart using data for percentages, anno for the annotations, and title for the plot title.

`bake_basic_pie()` will call `anno_donut_plot` for all the data that was analyzed using the array of analysis functions.

## Categorization

Having a list of all actions scheduled in a 15-minute block is useful data. You can see how many times that action was done or the total time in minutes or hours. However, to get a deeper look into how I played my life, these actions should be categorized.

### Level One

What are the fundamental actions in life? How does one classify this? To be honest, there was no scientific research or deep philisophical thougtht that went into creating the Level One categorizes. I allowed the data to guide my decisions. The categorizes are:

- Sleep
  - Sleep is defined as anyime that I am not awake. This can be regular sleep or naps.
- Work
  - Work is defined loosely as actions that need to be done because of an organization that I am apart of, whether that organization be my college, fraternity, or job.
- Life
  - Life is defined as actions that are not work. These actions are done in my free time. Talking with friends, social life, or doing nothing are examples of Life actions.
- Food
  - Food is defined as anytime I am eating.
- Unknown
  - Unknown is defined as time that was not filled out in my Weekly Schedule. Gaps do occur because of computer access or forgetfulness.

### Level Two

Level Two categories attempt to bin Level One actions into actual discrete things. For Work, this can be the class that the work is associated with (AEP 3610, CS 3110, LAW 3281, etc.) or the organization the work is done for (Pike or Purple Pill). For Life, this can be talking to people, social events with my fraternity, general fun events, or traveling.

### Level Three

Level Three is only associated with Level Two categories in Work. This level splits my classes into Lecture, Studying, and Assignment times.

## Results

Two semesters were analyzed, Fall 2021 and Spring 2022, both occuring in my junior year of collge. Data for the Fall semester runs from August 30th to November 21st of 2021 with the Spring semester running from January 31st to May 8th of 2022. This means the Fall semester has Weeks 2 through 13 of the semester (11 weeks) and the Spring semester has Weeks 2 through 15 (14 weeks).

### Fall 2021

![](/FA21_DAY.png "")

![](/FA21_WORK.png "")

![](/FA21_LIFE.png "")

![](/FA21_longest_day.png "")

![](/FA21_Level3.png "")

### Spring 2022

![](/SP22_DAY.png "Spring 2022 Average Day by Level One")

![](/SP22_WORK.png "Spring 2022 Total Time of Work")

![](/SP22_LIFE.png "Spring 2022 Total Time of Life")


## Life without My Schedule

