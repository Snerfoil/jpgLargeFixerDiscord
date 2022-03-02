# jpgLargeFixerDiscord
renaming files for ppl that dono about that. or solving problems that apparently phones have with twitter. like what the hecc?

anyway

# how to make use of this.
merp

so we heav thing nao. ngl figuring out how to properly make this work was kind a bitch.

targetChannelHere []: bot targets attachments in this channel
targetChannel [channelID]: bot targets attachments in this channel
setCommandPrefix [prefix]: change the command prefix trigger
setWhitelistedRoles [roleID0,roleID1,...,roleIDn]: set which roles can use this command (any role with admin perms will always be able to use this.)


for dev ppl:

so... this bot is designed to be run on heroku. if you wana build it yourself here is what ya need to know.

first goto https://discord.com/developers/applications and login. mind you discor'd website my try to redirect you to the web app when you login so you MAY have to use this link twice once your browser authenticates.

make a new app, and give it a name.
select the 'bot' tab on the left side and then press AddBot.
see where it says token just under the username field? copy the token there. you will need this later.

goto https://heroku.com/ and make an account there, the service is free.

in your dashboard make a new app and call it something.
goto its settings and add the following ENVIRON variable of:
BOT_TOKEN
with the value being your discord bot's login token.

you will also need to install the heroku Postgres db addon. it free and is how the bot stores its persistant config info. this also adds another ENVIRON variable called DATABASE_URL which the bot uses to talk to the DB.

you will also need to check the overview tab and set your dyno to use the launch param
`worker python3 discordBot.py`
this tells it to run that python script as the main entry code.

now... this is the fun part.

so on the heroku page on the 'Deploy' tab is instructions on how to push code to the heroku app using the heroku CLI. you will also need the git command line tool.
(for those of you that dono, this is a command line program that is used to push and configure heroku code.)

download git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git (or you can use another place doesnt rily matter)
download heroku CLI: https://devcenter.heroku.com/articles/heroku-command-line
(CAUTION: the install prosedue might have changed sense I wrote this so expect stuff to be different.)

once those are both installed like the page says you can run the following commands
first 'cd' to someplace you wana store your development folders (or directories, ie: c:\gitRepos)
do: heroku git:clone -a %APP_NAME%
this will add a new folder with git initalized into it and this si where you can put my source code. everything in that folder with the .py scripts.
'cd' inside of it.

run the following git command to add all the files, commit them, and then push to heroku
git add .
git commit -am "first push"
git push heroku master

once that is all done the heroku app should start operating (assuming you turned on the dyno)

thats all. mind you this instruction isnt exactly the best thing in the world so you are welcome to ask me SNERFOIL#9999 on discord for help. though you would be better off improving this or porting it to another language.

{rough overview of what all of the files are for}
__pycache__: a folder with precompiled python code for optimization thingys, tbh I dono its significance
.gitignore: this file contains a list of filenames and patters of files that DONT commit with the project.
discordbot.py: main code that excecutes on runtime
note.txt: this file dummy
Procfile: this is a file that contains the dyno command that tells heroku how to run the app.
requirements.txt: this tells heroku what python modules are needed
runtime.txt: the version of python (or whatever language you want) to use
tokenStore.py: this is a handler to store pickle'd python objects on the Postgre db. (tbh I hate the fact I even have to do this.)