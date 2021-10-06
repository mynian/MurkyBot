# MurkyBot Docker
This is a Minimum Viable Product.  All complaints go to mynian's trash can.  
This is brought to you by hacky google engineering, so it is likely not the best way to do things.
You have been warned!

Requirements:
* Blizzard Api client and secret
* Discord server token
* World of Warcraft Realm ID

---

1. Copy the following files to a directory on your docker host Ex: /home/mynian/MurkyBot:
  * bot.py
  * requirements.txt  
  * dockerfile


2. Build the container
  * Make sure you are in the same directory as the files from the previous step.
  * > docker build -f dockerfile -t murkybot .

3. Set the require environment variables  
  * > export DISCORD_TOKEN="123abc"
  * > export CLIENT_ID="123abc"
  * > export CLIENT_SECRET="123abc"
  * > export REALM_ID="13"

4. Run the docker container in the foreground (so you can see all it's glory)
docker run -it --rm --name murkybot -v "$PWD":/usr/src/myapp \
  --env DISCORD_TOKEN=${DISCORD_TOKEN} \
  --env CLIENT_ID=${CLIENT_ID} \
  --env CLIENT_SECRET=${CLIENT_SECRET} \
  --env REALM_ID=${REALM_ID} \
  -w /usr/src/myapp murkybot

5. Run the docker container in the background
docker run -d --rm --name murkybot -v "$PWD":/usr/src/myapp \
  --env DISCORD_TOKEN=${DISCORD_TOKEN} \
  --env CLIENT_ID=${CLIENT_ID} \
  --env CLIENT_SECRET=${CLIENT_SECRET} \
  --env REALM_ID=${REALM_ID} \
  -w /usr/src/myapp murkybot  
