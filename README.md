# MurkyBot

This is a bot written for Discord in Python to do a few things.

1. Automatically request the status of the world server for a warcraft realm and post to a channel when a change happens.

2. Automatically request if a world server has a login queue and post to a channel when a change happens.

3. Allows users to manually request the current server status by typing +status.

4. Allows users to manually requests the current queue status by typing +queue.

5. Some other commands that I add randomly to either test or mess with my discord members.

6. Use status indicator LEDs that I have mounted to a custom printed part on my raspberry pi case to indicate what the current status is at a glance from a distance. 

7. The kill command that can be triggered via a bot command will stop the script from running. This has been added as a failsafe for some kind of error that may occur and cause the bot to constantly send messages to Discord.
