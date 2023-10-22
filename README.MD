![I prompted it all by myself](Logo.jpg)
5F
# Install

## BOT API

1- Open telegram, enter @Botfather in the search tab and choose this bot.  
2- type /newbot  
3- Pick a name, then pick a username it needs to be globally unique and ends with "_bot"  
4- Get the token and save it , or if you are re-using an old bot call "/token"  

## Traditional  
  
```sh  
# Install ffmpeg using whatever OS package manager you use  
git clone $URL
cp .env.example .env 
emacs .env 
# Export the folders you use to store the data, for example your NAS, or /dev/null 
# You need to use your own and the path need to be writable
# The examples here make no sense
export ARCHIVE_FOLDER=/trinity/dump/
export AUDIOBOOK_FOLDER=/trinity/music/audiobooks
export MUSIC_FOLDER=/trinity/music/staging

virtualenv venv
source ./venv/bin/activate   # Or whatever your OS/Shell combo you use
pip install -r requirements.txt
python main.py
``` 

## Docker
```sh
# Build the image
docker build --tag=public/archivist:latest .

# Create an .env file, if you are using docker for some reason , leave the defaults just add the api key 
cp .env.example .env 
nano .env # only add API key 

# Export the folders you use to store the data, for example your NAS, or /dev/null 
# You need to use your own and the path need to be writable
# The examples here make no sense
export ARCHIVE_FOLDER=/trinity/dump/
export AUDIOBOOK_FOLDER=/trinity/music/audiobooks
export MUSIC_FOLDER=/trinity/music/staging

docker run -d -v $ARCHIVE_FOLDER:/tmp/data/archive -v $MUSIC_FOLDER:/tmp/data/music -v $AUDIOBOOK_FOLDER:/tmp/data/audiobook  -v "$(pwd)"/.env:/app/.env:ro --name archivistbot public/archivist:latest
```

# Logo

Probably the laziest logo yet .  
Model: Vintedois (22h) Diffusion model trained by Predogl and piEsposito with open weights, configs and prompts (as it should be) from [hugging face](https://huggingface.co/22h/vintedois-diffusion-v0-2?text=old+librarian+%2C+trending+on+artstation+%2C+old+school)  

```note
Prompt: "old librarian , trending on artstation , old school "
```


# TODO

Clean up the FSM code and move on. 

## Bugs
- [ ] The code is bad and I should feel bad 
- [X] Fix archiving to actually download highest quality 
    - [ ] block the three reply due to different format

## Major
- [ ] add git / fossil / other repo cloning/archiving
- [ ] Add full page(URL) cloning + screenshot 
- [ ] Add link sync, something along the line of a centralized links database and this would feed into it 

## Mid 
- [X] Use requirements.txt and/or start to be hip-with the kids and use poetry 
- [X] Use ReplyKeyboardMarkup and detrmine where the file ends up based on this and what YT-dlp option to give it 
- [ ] Fix environment var passing in general 
- [X] Is ffmpeg really really REALLY needed ?  (It is needed)
    - [X] Install ffmpeg in the container image, 
    - [A] Maybe use [some random](https://johnvansickle.com/ffmpeg/) internet link for a version of ffmpeg that is static
    - [?] Fix parameter to be more generic for the container 
    - [ ] Document the container crap (I do not care enough)
- [ ] Maybe one day build "highest" possible combo of audio and video , via split download (DASH+high quality audion+ffmepg glue them together)

## Minor
- [X] better logo the logo is perfect 
