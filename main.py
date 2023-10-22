import sys
import os
import asyncio

from dotenv import load_dotenv
from loguru import logger  # Trying it out

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

import yt_dlp

logger.add(
    "logs/archivist.log",
    format="{time:DD-MM-YY HH:mm:ss} - {level} - {message}",
    level="INFO",
    rotation="1 month",
    compression="zip",
)

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
ARCHIVE_PATH = os.getenv("ARCHIVE_PATH")
AUDIOBOOK_PATH = os.getenv("AUDIOBOOK_PATH")
MUSIC_PATH = os.getenv("MUSIC_PATH")

bot = Bot(token=API_TOKEN)

# For example use simple MemoryStorage for Dispatcher.
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# States
class Form(StatesGroup):
    name = State()  # Will be represented in storage as 'Form:name'
    gender = State()  # Will be represented in storage as 'Form:gender'


@dp.message_handler(text_contains="http")
async def start_bots(msg, state: FSMContext):
    await bot.send_message(msg.from_user.id, "Ok, send me a file")
    await Form.name.set()
    logger.info(f"From user {msg.from_user.full_name} we got URL: {msg.text}")

    async with state.proxy() as data:
        data["URL"] = msg.text

    # Configure ReplyKeyboardMarkup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Music", "Archive")
    markup.add("Audiobook")
    await msg.reply("What is the type of content?", reply_markup=markup)


@dp.message_handler(commands="help")
async def cmd_start(message: types.Message):
    """
    Help's entry point
    """
    # Set state
    await message.reply(
        "Hi there! This is a simple bot just give me your youtube url or enter /cancel"
    )


# You can use state '*' if you need to handle all states
@dp.message_handler(state="*", commands="cancel")
@dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logger.info(f"From user {msg.from_user.full_name} we got a cancel request")
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply("Cancelled.", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=Form.name)
async def process_contenttype(msg: types.Message, state: FSMContext):
    """
    Process user name
    """
    async with state.proxy() as data:
        data["contenttype"] = msg.text
        logger.info(
            f"From user {msg.from_user.full_name} we got content type: {msg.text}"
        )

    # Remove keyboard
    markup = types.ReplyKeyboardRemove()

    # And send message
    await bot.send_message(
        msg.chat.id,
        md.text(
            md.text("Hi! I am currently downloading: ", md.bold(data["URL"])),
            md.text(
                "It will be available in the following section ,",
                md.bold(data["contenttype"]),
            ),
            sep="\n",
        ),
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN,
    )

    # Kick off download
    # XXX Here is the logic to determine what we need to do so really move it all out the fuck from here
    # While waiting for python 3.10 everywhere we pretend switch statements don't exist
    if data["contenttype"].lower() == "music":
        format = ydl_opts_music
    elif data["contenttype"].lower() == "audiobook":
        format = ydl_opts_audiobook
    else:
        format = ydl_opts_default

    outcome = await downloadAudioBook(data["URL"], format)
    if outcome == 0:
        await msg.reply(f"File downloaded successfully ")

    # Finish conversation
    await state.finish()


ydl_opts_default = {
    "format": "bestvideo+bestaudio/best",
    # See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
    "outtmpl": ARCHIVE_PATH + "/%(title)s.%(ext)s",
}


ydl_opts_audiobook = {
    "format": "m4a/bestaudio/best",
    # See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
    "postprocessors": [
        {  # Extract audio using ffmpeg
            "key": "FFmpegExtractAudio",
            "preferredcodec": "m4a",
        }
    ],
    "outtmpl": AUDIOBOOK_PATH + "/%(title)s.%(ext)s",
}

ydl_opts_music = {
    "format": "bestaudio/best",
    # See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
    "postprocessors": [
        {  # Extract audio using ffmpeg
            "key": "FFmpegExtractAudio",
            "preferredcodec": "flac",
        }
    ],
    "outtmpl": MUSIC_PATH + "/%(title)s.%(ext)s",
}


async def downloadAudioBook(url, format):
    """
    Return code
    0 = Everything is successful
    100 = yt-dlp must restart for update to complete
    101 = Download canceled by --max-downloads etc
    2 = Error in user-provided options
    1 = Any other error
    """

    URL = url
    try:
        with yt_dlp.YoutubeDL(format) as ydl:
            error_code = ydl.download(URL)
            logger.info(
                f"\nYT-DLP exit code : {error_code} while attempting to download : {URL}"
            )
    except Exception as e:
        error_code = -200
        logger.error(f"\n Exception: {e} occured while attempting to download: {URL}")
    return error_code


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
