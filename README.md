# Visionary-OS
Our Visionary open source discord bot. Our goal is to create a discord bot, which is hosted by us, but every member of our community can contribute and add features.

# How do I get started?
- First, head over to our [Get Started guide](https://github.com/artificialis-ai/start-here-guidelines#get-started)
- Afterwards, as you continue with your Visionary feature, you can take a look at their [Documentation](https://discordpy.readthedocs.io/en/stable/)
- If you need inspiration, head over to open their [examples](https://github.com/Rapptz/discord.py/tree/master/examples)
- After your pull request got accepted, you can head over to [our discord](https://discord.gg/GRpkfnZcUj) and tell everyone about the new feature! And don't forget to write about your experience through [our publication](https://medium.com/artificialis)

# How do I start the bot?
In our [main.py](main.py) we have specified 
```py
bot.run(os.environ['BOT_TOKEN'])
```
This means the bot is searching for an existing environment variable with the name `BOT_TOKEN`. So, now you just have to create it in your environment and start the bot as you would any python program.
