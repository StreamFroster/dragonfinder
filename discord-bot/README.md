# DragonFinder Discord Bot

- Warning: Dragonfinder is currently in rapid development, you may see some drastic changes in how we generate and use a trained model.

The bot itself looks for any message starting with the command `$find` to download and run predictions on the attachments for the message. The image to predict must be sent along with the command.

## Installing dependencies

You'll need to install all of the required dependencies listed in the `requirements.txt` file

```
pip install -r requirements.txt
```

## Downloading the trained model

The trained model is available for download [here](https://drive.google.com/drive/folders/1YTl06HgPwjzF6NKue7XAw9b55XP06zhs?usp=share_link). The bot will use the downloaded model to draw bounding boxes on new images.

> Note: Make sure to replace the [DISCORD_BOT_TOKEN] with your own token! If unsure how to get yours, refer to [the official Discord Developer docs](https://discord.com/developers/docs/topics/oauth2)

## Run the Python script

```
python ./main.py
```