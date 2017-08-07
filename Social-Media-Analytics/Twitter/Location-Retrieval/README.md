# Twitter Location Retrieval

This script retrieves the location for a specified user.  Due to the fact that about 90% of tweets we were retrieving did not have any geodata enabled, we used the location of the user as a proxy.  To determine the location of the user, the user's followers were iterated through, and the location of the user was appended to a list.  The location that occurs msot commonly in the list was determined to be the user's location.

<br>

