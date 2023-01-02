# Weekly Schedule Analysis

This project is currently under construction.

## Why Under Construction ?

In short, I would like to keep using this project throughout my years. To do so, the project needs to grow, both is scale and complexity. As with most projects, the first working product is usable but scrapy, this edition was used to analysis the Fall 2021 semester. Improvements where made with regards to the functionality and usability of the project. This reduced the time the user needed to spend analyzing the actions. However, more scaling with data management and a better user interface with an API will result from this next refactoring.

## Database

Currently, all the analyzed data is stored in a JSON file. I have built some functions to help read and write from JSON file, but these read-write functions are not all encompassing. Moreover, the organization of the JSON files have not been full thought out, so data is stored in a somewhat non-optimal way. To help with these problems, a database will be used.

As this project is small, a smaller functioning database will be used. A few options are:

- SQLite
- Pocketbase

I am already using Pocketbase for my personal website, so I think I will double down on the technology and use Pocketbase.

### Database Structure

Here is the current structure of my JSON files:

```json
{
	"metadata": {
		"title": "Some title",
		"date_start": "Start date",
		"date_end": "End date"
	},
	"classifications": {
		"level_one": {
			"sleep": [
				"actions"
			],
			"work": [
				"actions"
			],
			"life": [
				"actions"
			],
			"food": [
				"actions"
			],
			"unknown": [
				"actions"
			]
		},
		"level_two": {
			...
		}
	},
	"analysis": {
		"actions": {
			"action1": 5,
			"action2": 15
		},
		"total_actions": 9000,
		"day": {
			"text": [
				"2882 of sleep"
			],
			"data": [
				2882
			],
			"time": [
				"7 hours, 25 minutes of sleep"
			]
		}
	},
	"talk": [
		"people I have talked to"
	]
}
```

The three top-level blocks are metadata, classification, and analysis. Metabase can be used to create a table that keeps track of the week CSV files and organizes them into semesters or other spans of time.

The real decision is how I am going to store 15-minute block and actions data. I believe two separate tables are needed. The goal is to house already-processed data in the database so easy, more specific analysis can take place easily. If I just stored the CSV files without any connection to the already-processed actions data, extract processing would be necessary. However, we need to keep in mind that a single-source-of-truth is necessary to avoid inconsistencies in the database.

#### Day Data

| Date      | Era        | 00:00 | 00:15 |
|-----------|------------|-------|-------|
| 2021-8-23 | Semester 5 | Sleep | Sleep |


A table like this might be used to deep the actual weekly data organized. Instead of having the string representation of the actions in the time block, a foreign key could be used.

#### Action Data

| Action | Total Count | Level One | Level Two | Level Three | 
|--------|-------------|-----------|-----------|-------------|
| Sleep  | 147         | Sleep     | Null      | Null        |

## Frontend

The frontend need two functionalities: user input to classify actions, and a dashboard to visualize the data.

### User Input

Whenever new actions are added to the database, I need to be able to:

- Edit the action's string if a typo is present
- Categorize the action for Level One
	- Either pick from an already used list, or
	- Create a new category
- Do the same for Level Two and Level Three

### Dashboard

As the dashboard needs to display pie charts or other graphs, the database will need to have tables that hold the processed data so chart generation and not data processing is done when the user requests a chart.

## Backend

A backend is needed to connect to the Notion API to collect the week data, process the week data, store the data in the database, and serve the user input and dashboard data to the frontend.