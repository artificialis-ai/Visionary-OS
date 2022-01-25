# Visionary-OS
Our Visionary open source discord bot. 

# How do I get started?
- First, head over to our [Get Started guide](https://github.com/artificialis-ai/start-here-guidelines#get-started)
- Afterwards, you can write your own bot, take a look at their [Documentation](https://discordpy.readthedocs.io/en/stable/)
- If you need inspiration, head over to open their [examples](https://github.com/Rapptz/discord.py/tree/master/examples)

# How do I start the bot?
In our [main.py](main.py) we have specified 
```py
bot.run(os.environ['BOT_TOKEN'])
```
This means the bot is searching for an existing environment variable with the name `BOT_TOKEN`. So, now you just have to create it in your environment and start the bot as you would any python program.
