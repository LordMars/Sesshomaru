This is the python script for the seshhomaru discord bot
Its only current purpose is to create a minecraft event scheduled at 5:30PM pst each monday.

The script itself does not schedule when it is run.
That is to be done on the host machine, for example by way of TaskScheduler and batch files on windows machines.

In order for the script to run correctly a few things are required.
- a botConfig.json file
    This contains
    - token - the token of your discord bot
    - guildId - the id for the server the server the bot is in
    - eventList - a list of data for events to attempt to create
        Each of these events needs the following
        - name
        - description
        - startTime - the time to schedule this event for
            - hour(24 hour time)
            - minute
- a python installation with the discord, json, and pytz modules installed

Currently the bot always schedules events on Monday and in the Eastern timezone