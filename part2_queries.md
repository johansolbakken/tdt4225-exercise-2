TODO: vi må huske å fjerne de som hadde høyere altitude enn 777 meter!!!

# 1. How many users, activities and trackpoints are there in the dataset (after it is inserted into the database).

~~~sql
SELECT count(id) as num_users from users
~~~
~~~sql
SELECT count(id) as num_acts from activities
~~~
~~~sql
SELECT count(id) as num_tracks from trackpoints
~~~

Summer disse

# 2. Find the average, maximum and minimum number of trackpoints per user.
**Avg**
~~~sql
SELECT AVG(Trackpoints) as AvgTrackpoints
FROM (
  SELECT COUNT(trackpoint_id) as Trackpoints
  FROM user
  NATURAL JOIN activity
  NATURAL JOIN trackpoint
);
~~~

**Max**
~~~sql
SELECT COUNT(trackpoint_id) as Trackpoints
FROM user
NATURAL JOIN activity
NATURAL JOIN trackpoint
ORDER BY Trackpoints DESC;
~~~

**Min**
~~~sql
SELECT COUNT(trackpoint_id) as Trackpoints
FROM user
NATURAL JOIN activity
NATURAL JOIN trackpoint
ORDER BY COUNT(trackpoint_id) ASC;
~~~

# 3. Find the top 15 users with the highest number of activities.
~~~sql
SELECT user_id
FROM user
NATURAL JOIN activity
NATURAL JOIN trackpoint
GROUP BY user_id
ORDER BY COUNT(trackpoint_id) DESC
LIMIT 15;
~~~

# 4. Find all users who have taken a bus.
~~~sql
SELECT user_id 
FROM user WHERE has_labels = 1
NATURAL JOIN activity 
WHERE transportation_mode = "bus"
~~~

# 5. List the top 10 users by their amount of different transportation modes.
~~~sql
SELECT user_id 
FROM user WHERE has_labels = 1
NATURAL JOIN activity 
ORDER BY count(transportation_mode) DESC
LIMIT 10;
~~~

# 6. Find activities that are registered multiple times. You should find the query even if it gives zero result.
hmmmmmmmmm...
# 7. 
### a) Find the number of users that have started an activity in one day and ended the activity the next day.
### b) List the transportation mode, user id and duration for these activities.
# 8. Find the number of users which have been close to each other in time and space. Close is defined as the same space (50 meters) and for the same half minute (30 seconds)







# 9. Find the top 15 users who have gained the most altitude meters.
     7
 TDT4225 - Fall 2023
 ○ Output should be a table with (id, total meters gained per user).
○ Remember that some altitude-values are invalid
○ Tip:
∑(𝑡𝑝 𝑛. 𝑎𝑙𝑡𝑖𝑡𝑢𝑑𝑒 − 𝑡𝑝 𝑛−1. 𝑎𝑙𝑡𝑖𝑡𝑢𝑑𝑒), 𝑡𝑝 𝑛. 𝑎𝑙𝑡𝑖𝑡𝑢𝑑𝑒 > 𝑡𝑝 𝑛−1. 𝑎𝑙𝑡𝑖𝑡𝑢𝑑𝑒
10. Find the users that have traveled the longest total distance in one day for each transportation mode.
11. Find all users who have invalid activities, and the number of invalid activities per user
○ An invalid activity is defined as an activity with consecutive trackpoints where the timestamps deviate with at least 5 minutes.
12. Find all users who have registered transportation_mode and their most used transportation_mode.
○ The answer should be on format (user_id, most_used_transportation_mode) sorted on user_id.
○ Some users may have the same number of activities tagged with e.g. walk and car. In this case it is up to you to decide which transportation mode to include in your answer (choose one).
○ Do not count the rows where the mode is null.
