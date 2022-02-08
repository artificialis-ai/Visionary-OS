# For Developers that want to contribute to the project

Hello! This page will supply information about how to contribute to the project.

## Creating new commands

To create a new command you have to add this code to `main.py` (before `bot.run`):

```py
@bot.command(name='command_name', description="Description for help command", usage="Usage for help command")
async def command(ctx, other_arguments_here):
    pass # Your code here
```

### Help command support

For best results in the help command specify a `usage` and `description` for the command. An example of a command with usage and description:

```py
@bot.command(name='get_pfp', description="Get the user's profile picture", usage="get_pfp [user]")
```

For the usage you specify required arguments in pointy brackets (example `<name>`) and optional arguments in curly brackets (example `[name]`).

### Argument parsing

#### Catch all

To catch all arguments after the command you use `*` after the command (works with other commands too, but the catch all should be the last argument):

```py
@bot.command()
async def example_command(ctx, age, *fullname):
    full_name = ' '.join(fullname)
    await ctx.send(f"Your name is {full_name} and you are {age} years old.")
```

**Note:** The catch all argument returns a tuple, so you need to prosess `join()` to convert it to a string.

#### Optional arguments

You can specify optional arguments with `arg=None`, so that the default value is `None` (you can pass any default arguments). You can check for that in the code.

```py
@bot.command()
async def example_command(ctx, user=None):
    if user:
        ctx.send(f"Hello {user}!")
    else:
        ctx.send()
```

## The local library

The local library `utils` (in the `utils` folder) contains a few useful functions.

### Embeds

The library has usefull classes for embeds.

#### SendEmbed

The `SendEmbed` class is used to send embeds. It has 6 arguments:
* `ctx`: The context of the command.
* `title`: The title of the embed.
* `description`: The description of the embed. It appears as text below the title.
* `color`: The color of the embed. You can pass hex values as colors. The default is `0x253439` *optional*
* `thumbnail`: The thumbnail of the embed. *optional*
* `image`: The image of the embed. *optional*

#### ErrorEmbed

The `ErrorEmbed` class is used to send error embeds. It has 2 arguments:
* `ctx`: The context of the command.
* `error`: The error message.

#### HelpEmbed

There are 2 embeds to help with the help command - `HelpEmbed` and `CommandHelpEmbed`.

The `HelpEmbed` class is used to send help embeds. It has 2 arguments:
* `ctx`: The context of the command.
* `commands`: A list of commands to display. You can get them with `bot.commands`.

The `CommandHelpEmbed` class is used to send command help embeds. It has 2 arguments:
* `ctx`: The context of the command.
* `command`: The command to display. You need to pass a `Command` object.