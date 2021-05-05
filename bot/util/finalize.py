from bot.util.UserUtil import *
from bot.util.TimeUtil import *

def finalize(ctx, command, send, errorcode, *args):
    time = current_time()
    if errorcode == 'OK':
        errormsg = 'Task completed successfully!'
    else:
        errormsg = errorcode
    base = f'[{time}, {ctx.message.guild.name}:#{ctx.message.channel.name}] {prefix}{command}:\n\
 - {errormsg}\n - User {username(ctx.message.author, testfor_alt(ctx.message.author.id))[0]} did "{prefix}{command}'
    if len(args) > 0:
        print(base + ' ' + args[0] + '\"')
    else:
        print(base + '"')
    if send != None:
        return send
