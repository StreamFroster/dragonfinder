import nextcord
import random, uuid, os, time, logging

# Machine Learning libraries
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from tensorflow.python.ops.numpy_ops import np_config
from pathlib import Path
from nextcord.ext import commands

np_config.enable_numpy_behavior()

# Logging configuration
logging.basicConfig(filename = 'discord-bot.log', filemode = 'a', format = '%(asctime)s %(levelname)s: %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', encoding='utf-8', level = logging.INFO)

try:
    logging.info('Trying to load Dragonfinder model from current directory...')
    model = tf.keras.models.load_model('dragonfinder-model.h5')
except:
    logging.error('No model found, are you sure you have downloaded the model from the repository?')
    exit()

logging.info('Model successfully loaded!')

IMAGE_HEIGHT = 100
IMAGE_WIDTH = 150

CLASS_NAMES = ['deer', 'dragon', 'lion']

def findDragon(image):

    # Load the raw data from the file as a string
    img = tf.io.read_file(image)
    
    # Convert the compressed string to a 3D uint8 tensor
    img = tf.image.decode_jpeg(img, channels = 3)
    
    # Use `convert_image_dtype` to convert to floats in the [0,1] range.
    img = tf.image.convert_image_dtype(img, tf.float32)
    
    # Resize the image to the desired size.
    img = tf.image.resize(img, [IMAGE_HEIGHT, IMAGE_WIDTH])
    
    # This is an override function to get rid of the errors
    # If you comment this line out, the bot won't work
    # I don't know why
    img = img.reshape(IMAGE_HEIGHT, IMAGE_WIDTH, 3)

    softmax = tf.keras.layers.Softmax()

    prediction_score = model.predict(np.expand_dims(img, 0))

    prediction_probability = softmax(prediction_score)
    
    prediction_class = np.argmax(prediction_probability, axis=1)

    print('The prediction class index is ' + str(prediction_class))

    print('The prediction probabilities are ' + str(prediction_probability))

    print(prediction_score)
    
    # Find the percentage of the highest class from above
    percentage = max(prediction_score[0])

    return 'I am ' + str(percentage) + '% sure that it is a ' + str(CLASS_NAMES[int(prediction_class)])


description = 'What truly counts as a dragon? $help'

# Specify what intents do we want from Discord
intents = nextcord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='$', description=description, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    logging.info(f'Bot {bot.user} successfully logged on with user ID {bot.user.id}')
    print('-------------------------')

@bot.command()
async def add(ctx, left: int, right: int):
    '''Adds two numbers together.'''
    await ctx.send(left + right)


# Download the image attachment from the user message, then send the image file back to the user.
@bot.command()
async def find(ctx):
    '''Find a dragon within an image, make sure the attachment is included with the command.'''
    if ctx.message.attachments:
        # Generate a unique UUID for the downloaded image
        imgFileName = uuid.UUID(int = random.getrandbits(128)) + '.png'
        
        # Combine the attachment file name with the folder it's supposed to be in
        imgName = str(os.path.join('attachments', imgFileName)) 

        await ctx.message.attachments[0].save(imgName)

        await ctx.send(findDragon(imgName))

        await ctx.send(file=nextcord.File(imgName))
        
    else:
        await ctx.send('I couldn\'t find an image in your message content, please try again.')


bot.run('BOT_TOKEN')
