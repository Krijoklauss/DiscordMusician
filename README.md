# DiscordMusician
This is a simple MusicBot i wrote in Python, all features and upcomming updates explained below 

 - Intention
   -  This whole bot was basically an idea i had a while ago already.
      But the first time i used the Bot for my own Discord only and havent released it to the public.
      This time i will keep this bot updated for everyone and push updates whenever i find time to edit something.
      Keep in mind, im programming this bot all by myself and I have some more projects running in the background!
      So please just dont ask for next updates or something like that!
 

 - Functions
    - The MusicBot is able to play Music on multiple DiscordServers simultaniously
    - Commands
      -  prefix
      -  nick
      -  bind
      -  play
      -  pause
      -  stop
      -  resume
      -  queue
      -  seek
      -  clear
      -  cleaner
      -  help
      -  lang
      -  languages


-  Upcomming updates
   -  Working on the seek functions which is currently locked due to very slow performance

-  Latest updates
   -  Updated youtube playlist implementation
      -  It's way faster now and works without any bugs

   -  Fixed a bug where normal youtube links wont work anymore
      -  When specified a normal youtube link as argument on play function
         the bot would run into an error due to some library issues with python

   -  Implemented several new languages (~ 50 new language packages)
      -  If the Bot runs into an Error based on a languge error please let me know,
         it was an automated process to create the languages.json file
         If something goes wrong i need to fix that in my code or manually push an update

   -  Updated the way bot tokens were read in
      -  They are now read from a .json file instead of global variables on your system!
      -  You can change the path to your json in the 'main.py' file

   -  Updated *Config* tab in README.md

-  Config
      If you want to use this Bot on your Server you can either inivite it by using this link *COMING SOON*,
      or by making it your own Bot. You need to go to your Discord applications and then create a new application, add
      a new bot to the application, invite the bot to your server and put the token inside the main.py file.
      
      I stored my discord tokens in a .json file and im loading them in at lines 16-18.
      You can either create your own json file and load that in or delete
      line 17 and 18 and just set token to *YOUR_NEW_TOKEN*

      This is the link to the discord applications: 'https://discord.com/developers/applications'
      This Video may be a little old but you find something about creating bots and inviting them to your server here: 'https://www.youtube.com/watch?v=UVedJuBojF8'

      If this wont help you just send me a message to 'musician-bot@protonmail.com'!
      I'll try to answer all your questions there =)


-  Other things
   -  As i said in the beginning of this README im a single programmer working on this.
      I'll try my best to keep it updated and push new things every month.

   Last update ~ 27.04.2022
