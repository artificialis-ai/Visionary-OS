import discord

class SendEmbed(discord.Embed):
    def __init__(self, ctx, title, description, color=0x253439, thumbnail=None, image=None):
        super().__init__(title=title, description=description, color=color)
        self.set_footer(text="Requested by " + ctx.author.name, icon_url=ctx.author.avatar_url)
        if thumbnail:
            self.set_thumbnail(url=thumbnail)
        if image:
            self.set_image(url=image)

class ErrorEmbed(SendEmbed):
    def __init__(self, ctx, error):
        super().__init__(ctx, title="Error", description=error, color=discord.Color.red())

class HelpEmbed(SendEmbed):
    def __init__(self, ctx, commands):
        super().__init__(ctx, title="Help", description="Here's a list of commands you can use. Use `{}help [command]` to get more info on a command.".format(ctx.prefix))
        
        for command in commands:
            self.add_field(name=command.name, value=command.description)

class CommandHelpEmbed(SendEmbed):
    def __init__(self, ctx, command):
        super().__init__(ctx, title="Help", description=f"Here's some info on the command `{command}`.")    
        self.add_field(name="Usage", value=f"```{ctx.prefix + command.usage}```")    