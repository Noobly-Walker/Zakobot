

class zakoctx:
    def __init__(self, source=None, user=None, message=None):
        self.source = source
        self.user = user
        self.message = message

class zakouser:
    def __init__(self, name=None, id=None, profileImg=None):
        self.name = name
        self.id = id
        self.profileImg = profileImg

class zakomessage:
    def __init__(self, content=None, attachments=None, author=None):
        self.content = content
        self.attachments = attachments
        self.author = author

class messageInterpreter:
    def fromDiscord(self, ctx):
        translatedContext = zakoctx(
            source = ["discord", ctx.guild.id, ctx.channel.id]
            user = zakouser(
                name = ctx.author.name
                id = ctx.author.id
                profileImg = ctx.author.avatar_url
                )
            message = zakomessage(
                content = ctx.message.content
                attachments = [i.url for i in ctx.message.attachments]
                author = zakouser(
                    name = ctx.author.name
                    id = ctx.author.id
                    profileImg = ctx.author.avatar_url
                    )
                )
            )
        
        
