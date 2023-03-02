# Strava Activities to ArcGIS Dashboard
Repository with some Python and Arcade code to extract activity data from Strava to produce an ArcGIS Dashboard.

The first step to extract data from Strava is to activate the Strava API and get the right permissions and refresh token to be able to get all the activity data of interest. I must give credit to <b><a href="https://towardsdatascience.com/using-the-strava-api-and-pandas-to-explore-your-activity-data-d94901d9bfde">Matt Ambrogi</a></b> and <b><a href="https://www.youtube.com/watch?v=sgscChKfGyg&t=258s">franchyze923</a></b>. They provide an easy step by step guide to achieve this.

I have created 2 different scripts, that can be combined once you have extracted all the activity streams (if you are interested on those) and automate for dayly/weekly/monthyl updates if you wish. They are splitted as the Strava API has some limitation on requests (100 request every 15 min, and 1000 request per day)

<h2>Extract_act.py : script to extract activities as csv file and create Feature Class with routes (lines)</h2>
In my case, I used the code from Fran in its gibhub Strava API repository <b><a href="https://github.com/franchyze923/Code_From_Tutorials/tree/master/Strava_Api">franchyze923</a></b> with some changes in the way the code iterates over the pages. I am using the Strava API to get the total number of activities to calculate the number of pages that I need to loop though.

After getting the activities, using Pandas and the Polyline libraries I obtained the coordinates from the <i>map.polylines</i> column than later I will use to create some points and lines using <b>arcpy</b>. I am using <b>arcpy 3.1</b>, with previous versions slightly changes are required.

<h2>Extract_streams.py : script to extract activity streams as csv file</h2>
The second script allows to extract the activity streams (streams in Strava are the data recorded during an activity, wich might include distance, time, heart rate, gradient, speed, cadence. As I mentioned before, the Strava API has some limitations on requests, so you will need to slice the <i>activities_ids</i> list to avoid exceeding those limits (you might want to use some Python timer to automate this process).

&nbsp

With the line Feature Class, activities.csv and streams.csv you can create the ArcGIS Dashboard.
