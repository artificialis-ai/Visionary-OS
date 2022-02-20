import discord

# Embed class - an easyier way to create embeds
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
            if command.description:
                desc = command.description 
            else: 
                desc = "No description available"
            
            self.add_field(name=command.name, value=desc)

class CommandHelpEmbed(SendEmbed):
    def __init__(self, ctx, command):
        if command.description:
            desc = command.description 
        else: 
            desc = "No description available"
        
        super().__init__(ctx, title=f"Help on `{command}`", description=desc)    
        
        if command.usage:
            self.add_field(name="Usage", value=f"```{ctx.prefix + command.usage}```")    