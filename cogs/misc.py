import datetime
import asyncio
import strawpy
import random
import re
from PythonGists import PythonGists
from appuselfbot import bot_prefix
from discord.ext import commands
from discord import utils
from cogs.utils.checks import *

'''Module for miscellaneous commands'''

class Misc:

    def __init__(self, bot):
        self.bot = bot
        self.regionals = {'a': '\N{REGIONAL INDICATOR SYMBOL LETTER A}', 'b': '\N{REGIONAL INDICATOR SYMBOL LETTER B}', 'c': '\N{REGIONAL INDICATOR SYMBOL LETTER C}',
                          'd': '\N{REGIONAL INDICATOR SYMBOL LETTER D}', 'e': '\N{REGIONAL INDICATOR SYMBOL LETTER E}', 'f': '\N{REGIONAL INDICATOR SYMBOL LETTER F}',
                          'g': '\N{REGIONAL INDICATOR SYMBOL LETTER G}', 'h': '\N{REGIONAL INDICATOR SYMBOL LETTER H}', 'i': '\N{REGIONAL INDICATOR SYMBOL LETTER I}',
                          'j': '\N{REGIONAL INDICATOR SYMBOL LETTER J}', 'k': '\N{REGIONAL INDICATOR SYMBOL LETTER K}', 'l': '\N{REGIONAL INDICATOR SYMBOL LETTER L}',
                          'm': '\N{REGIONAL INDICATOR SYMBOL LETTER M}', 'n': '\N{REGIONAL INDICATOR SYMBOL LETTER N}', 'o': '\N{REGIONAL INDICATOR SYMBOL LETTER O}',
                          'p': '\N{REGIONAL INDICATOR SYMBOL LETTER P}', 'q': '\N{REGIONAL INDICATOR SYMBOL LETTER Q}', 'r': '\N{REGIONAL INDICATOR SYMBOL LETTER R}',
                          's': '\N{REGIONAL INDICATOR SYMBOL LETTER S}', 't': '\N{REGIONAL INDICATOR SYMBOL LETTER T}', 'u': '\N{REGIONAL INDICATOR SYMBOL LETTER U}',
                          'v': '\N{REGIONAL INDICATOR SYMBOL LETTER V}', 'w': '\N{REGIONAL INDICATOR SYMBOL LETTER W}', 'x': '\N{REGIONAL INDICATOR SYMBOL LETTER X}',
                          'y': '\N{REGIONAL INDICATOR SYMBOL LETTER Y}', 'z': '\N{REGIONAL INDICATOR SYMBOL LETTER Z}', '0': '0⃣', '1': '1⃣', '2': '2⃣', '3': '3⃣',
                          '4': '4⃣', '5': '5⃣', '6': '6⃣', '7': '7⃣', '8': '8⃣', '9': '9⃣'}
        self.emoji_reg = re.compile(r'<:.+?:([0-9]{15,21})>')
        self.ball = ['It is certain', 'It is decidedly so', 'Without a doubt', 'Yes definitely', 'You may rely on it', 'As I see it, yes', 'Most likely', 'Outlook good', 'Yes', 'Signs point to yes', 'Reply hazy try again',
                     'Ask again later', 'Better not tell you now', 'Cannot predict now', 'Concentrate and ask again', 'Don\'t count on it', 'My reply is no', 'My sources say no', 'Outlook not so good', 'Very doubtful']
    emojiDict = { #these arrays are in order of "most desirable". Put emojis that most convincingly correspond to their letter near the front of each array.
                  'a' : ['🇦','🅰','🍙','🔼','4⃣'],
                  'b' : ['🇧','🅱','8⃣'],
                  'c' : ['🇨','©','🗜'],
                  'd' : ['🇩','↩'],
                  'e' : ['🇪','3⃣','📧','💶'],       
                  'f' : ['🇫','🎏'],
                  'g' : ['🇬','🗜','6⃣','9⃣','⛽'],
                  'h' : ['🇭','♓'],
                  'i' : ['🇮','ℹ','🚹','1⃣'],
                  'j' : ['🇯','🗾'],
                  'k' : ['🇰','🎋'],
                  'l' : ['🇱','1⃣','🇮','👢','💷'],
                  'm' : ['🇲','Ⓜ','📉'],
                  'n' : ['🇳','♑','🎵'],
                  'o' : ['🇴','🅾','0⃣','⭕','🔘','⏺','⚪','⚫','🔵','🔴','💫'],
                  'p' : ['🇵','🅿'],
                  'q' : ['🇶','♌'],
                  'r' : ['🇷','®'],
                  's' : ['🇸','💲','5⃣','⚡','💰','💵'],
                  't' : ['🇹', '✝','➕','🎚','🌴','7⃣'],
                  'u' : ['🇺','⛎','🐉'],
                  'v' : ['🇻','♈','☑'],
                  'w' : ['🇼','〰','📈'],
                  'x' : ['🇽','❎','✖','❌','⚒'],
                  'y' : ['🇾','✌','💴'],
                  'z' : ['🇿','2⃣'],
                  '0' : ['0⃣','🅾','0⃣','⭕','🔘','⏺','⚪','⚫','🔵','🔴','💫'],
                  '1' : ['1⃣','🇮'],
                  '2' : ['2⃣','🇿'],
                  '3' : ['3⃣'],
                  '4' : ['4⃣'],
                  '5' : ['5⃣','🇸','💲','⚡'],
                  '6' : ['6⃣'],
                  '7' : ['7⃣'],
                  '8' : ['8⃣','🎱','🇧','🅱'],
                  '9' : ['9⃣'],
                  '?' : ['❓'],
                  '!' : ['❗','❕','⚠','❣'],
                  
                  #emojis that contain more than one letter can also help us react
                  #letters that we are trying to replace go in front, emoji to use second
                  #
                  #if there is any overlap between characters that could be replaced,
                  #e.g. 💯 vs 🔟, both could replace "10",
                  #the longest ones & most desirable ones should go at the top
                  #else you'll have "100" -> "🔟0" instead of "100" -> "💯".
                  'combination' : [['cool','🆒'],
                                   ['back','🔙'],
                                   ['soon','🔜'],
                                   ['free','🆓'],
                                   ['end','🔚'],
                                   ['top','🔝'],
                                   ['abc','🔤'],
                                   ['atm','🏧'],
                                   ['new','🆕'],
                                   ['sos','🆘'],
                                   ['100','💯'],
                                   ['loo','💯'],
                                   ['zzz','💤'],
                                   ['...','💬'],
                                   ['ng','🆖'],
                                   ['id','🆔'],
                                   ['vs','🆚'],
                                   ['wc','🚾'],
                                   ['ab','🆎'],
                                   ['cl','🆑'],
                                   ['ok','🆗'],
                                   ['up','🆙'],
                                   ['10','🔟'],
                                   ['11','⏸'],
                                   ['ll','⏸'],
                                   ['ii','⏸'],
                                   ['tm','™'],
                                   ['on','🔛'],
                                   ['oo','🈁'],
                                   ['!?','⁉'],
                                   ['!!','‼'],
                                   ['21','📅'],
                                ]
                 }

    #used in >react, checks if it's possible to react with the duper string or not
    def hasDupe(duper):
        colectomyDuper = list(filter(lambda x : x != '<' and x != '⃣', duper)) #remove < because those are used to denote a written out emoji, and there might be more than one of those requested that are not necessarily the same one.  ⃣ appears twice in the number unicode thing, so that must be stripped too...
        return len(set(colectomyDuper)) != len(colectomyDuper)
    
    #used in >react, replaces e.g. 'ng' with '🆖'
    def replaceCombos(reactMe):
        for combo in Misc.emojiDict['combination']:
            if combo[0] in reactMe:
                reactMe = reactMe.replace(combo[0],combo[1],1)
        return reactMe
        
    #used in >react, replaces e.g. 'aaaa' with '🇦🅰🍙🔼'
    def replaceLetters(reactMe):
        for char in "abcdefghijklmnopqrstuvwxyz0123456789!?":
            charCount = reactMe.count(char)
            if charCount > 1: #there's a duplicate of this letter:
                if len(Misc.emojiDict[char]) >= charCount: #if we have enough different ways to say the letter to complete the emoji chain
                    i = 0
                    while i < charCount: #moving goal post necessitates while loop instead of for
                        if Misc.emojiDict[char][i] not in reactMe:
                            reactMe = reactMe.replace(char, Misc.emojiDict[char][i],1)
                        else:
                            charCount+=1 #skip this one because it's already been used by another replacement (e.g. circle emoji used to replace O already, then want to replace 0)
                        i+=1
            else:
                if charCount == 1:
                    reactMe = reactMe.replace(char, Misc.emojiDict[char][0])
        return reactMe
    
    @commands.command(pass_context=True)
    async def about(self, ctx):
        """Links to the bot's github page."""
        if embed_perms(ctx.message) and ctx.message.content[7:] != 'short':
            em = discord.Embed(color=0xad2929, title='\ud83e\udd16 Appu\'s Discord Selfbot', description='**Features:**\n- Custom commands/reactions\n- Save last x images in a channel to your computer\n- Keyword notifier\n'
                                                                                                         '- Set/cycle your game status and your avatar\n- Google web and image search\n- MyAnimeList search\n- Spoiler tagging\n'
                                                                                                         '- Server info commands\n- Quoting, calculator, creating polls, and much more')
            em.add_field(name='\ud83d\udd17 Link to download', value='[Github link](https://github.com/appu1232/Discord-Selfbot/tree/master)')
            em.add_field(name='\ud83c\udfa5Quick examples:', value='[Simple commands](http://i.imgur.com/3H9zpop.gif)')
            em.set_footer(text='Made by appu1232#2569', icon_url='https://i.imgur.com/RHagTDg.png')
            await self.bot.send_message(ctx.message.channel, content=None, embed=em)
        else:
            await self.bot.send_message(ctx.message.channel, 'https://github.com/appu1232/Selfbot-for-Discord')
        await self.bot.delete_message(ctx.message)

    @commands.group(aliases=['status'], pass_context=True)
    async def stats(self, ctx):
        """Bot stats."""
        uptime = (datetime.datetime.now() - self.bot.uptime)
        hours, rem = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(rem, 60)
        days, hours = divmod(hours, 24)
        if days:
            time = '%s days, %s hours, %s minutes, and %s seconds' % (days, hours, minutes, seconds)
        else:
            time = '%s hours, %s minutes, and %s seconds' % (hours, minutes, seconds)
        try:
            game = self.bot.game
        except:
            game = 'None'
        if embed_perms(ctx.message):
            em = discord.Embed(title='Bot Stats', color=0x32441c)
            em.add_field(name=u'\U0001F553 Uptime', value=time, inline=False)
            em.add_field(name=u'\U0001F4E4 Messages sent', value=str(self.bot.icount))
            em.add_field(name=u'\U0001F4E5 Messages recieved', value=str(self.bot.message_count))
            em.add_field(name=u'\u2757 Mentions', value=str(self.bot.mention_count))
            em.add_field(name=u'\u2694 Servers', value=str(len(self.bot.servers)))
            em.add_field(name=u'\u270F Keywords logged', value=str(self.bot.keyword_log))
            em.add_field(name=u'\U0001F3AE Game', value=game)
            mem_usage = '{:.2f} MiB'.format(__import__('psutil').Process().memory_full_info().uss / 1024**2)
            em.add_field(name=u'\U0001F4BE Memory usage:', value=mem_usage)
            try:
                g = git.cmd.Git(working_dir=os.getcwd())
                g.execute(["git", "fetch", "origin", "master"])
                version = g.execute(["git", "rev-list", "--right-only", "--count", "master...origin/master"])
                commits = g.execute(["git", "rev-list", "--max-count=%s" % version, "origin/master"])
                if version == '0':
                    status = 'Up to date.'
                else:
                    latest = g.execute(["git", "log", "--pretty=oneline", "--abbrev-commit", "--stat", "--pretty", "-%s" % version, "origin/master"])
                    gist_latest = PythonGists.Gist(description='Latest changes for the selfbot.', content=latest, name='latest.txt')
                    if version == '1':
                        status = 'Behind by 1 release. [Latest update.](%s)' % gist_latest
                    else:
                        status = '%s releases behind. [Latest updates.](%s)' % (version, gist_latest)
                em.add_field(name=u'\U0001f4bb Update status:', value=status)
            except:
                raise
            await self.bot.send_message(ctx.message.channel, content=None, embed=em)
        else:
            msg = '**Bot Stats:** ```Uptime: %s\nMessages Sent: %s\nMessages Recieved: %s\nMentions: %s\nServers: %s\nKeywords logged: %s\nGame: %s```' % (time, str(self.bot.icount), str(self.bot.message_count), str(self.bot.mention_count), str(len(self.bot.servers)), str(self.bot.keyword_log), game)
            await self.bot.send_message(ctx.message.channel, bot_prefix + msg)
        await self.bot.delete_message(ctx.message)

    # 8ball
    @commands.command(pass_context=True, aliases=['8ball'])
    async def ball8(self, ctx, *, msg: str):
        """Let the 8ball decide your fate. Ex: >8ball Will I get good?"""
        answer = random.randint(0, 19)
        if embed_perms(ctx.message):
            if answer < 10:
                color = 0x008000
            elif 10 <= answer < 15:
                color = 0xFFD700
            else:
                color = 0xFF0000
            em = discord.Embed(color=color)
            em.add_field(name='\u2753 Question', value=msg)
            em.add_field(name='\ud83c\udfb1 8ball', value=self.ball[answer], inline=False)
            await self.bot.send_message(ctx.message.channel, content=None, embed=em)
            await self.bot.delete_message(ctx.message)
        else:
            await self.bot.send_message(ctx.message.channel, '\ud83c\udfb1 ``{}``'.format(random.choice(self.ball)))

    # Embeds the message
    @commands.command(pass_context=True)
    async def embed(self, ctx, *, msg: str = None):
        """Embed given text. Ex: Do >embed for more help"""
        if msg:
            if embed_perms(ctx.message):
                ptext = title = description = image = thumbnail = color = footer = author = None
                embed_values = msg.split('|')
                for i in embed_values:
                    if i.strip().lower().startswith('ptext='):
                        ptext = i.strip()[6:].strip()
                    elif i.strip().lower().startswith('title='):
                        title = i.strip()[6:].strip()
                    elif i.strip().lower().startswith('description='):
                        description = i.strip()[12:].strip()
                    elif i.strip().lower().startswith('desc='):
                        description = i.strip()[5:].strip()
                    elif i.strip().lower().startswith('image='):
                        image = i.strip()[6:].strip()
                    elif i.strip().lower().startswith('thumbnail='):
                        thumbnail = i.strip()[10:].strip()
                    elif i.strip().lower().startswith('colour='):
                        color = i.strip()[7:].strip()
                    elif i.strip().lower().startswith('color='):
                        color = i.strip()[6:].strip()
                    elif i.strip().lower().startswith('footer='):
                        footer = i.strip()[7:].strip()
                    elif i.strip().lower().startswith('author='):
                        author = i.strip()[7:].strip()
                if color:
                    if not color.startswith('0x'):
                        color = '0x' + color
                if color:
                    em = discord.Embed(title=title, description=description, color=int(color, 16))
                else:
                    em = discord.Embed(title=title, description=description)
                for i in embed_values:
                    if i.strip().lower().startswith('field='):
                        field_inline = True
                        field = i.strip().lstrip('field=')
                        field_name, field_value = field.split('value=')
                        if 'inline=' in field_value:
                            field_value, field_inline = field_value.split('inline=')
                            if 'false' in field_inline.lower() or 'no' in field_inline.lower():
                                field_inline = False
                        field_name = field_name.strip().lstrip('name=')
                        em.add_field(name=field_name, value=field_value.strip(), inline=field_inline)
                if author:
                    if 'icon=' in author:
                        text, icon = author.split('icon=')
                        em.set_author(name=text.strip()[5:], icon_url=icon)
                    else:
                        em.set_author(name=author)

                if image:
                    em.set_image(url=image)
                if thumbnail:
                    em.set_thumbnail(url=thumbnail)
                if footer:
                    if 'icon=' in footer:
                        text, icon = footer.split('icon=')
                        em.set_footer(text=text.strip()[5:], icon_url=icon)
                    else:
                        em.set_footer(text=footer)
                await self.bot.send_message(ctx.message.channel, content=ptext, embed=em)
            else:
                await self.bot.send_message(ctx.message.channel, bot_prefix + 'No embed permissions in this channel.')
        else:
            msg = '**How to use the >embed command:**\n**Example:** >embed title=test this | description=some words | color=3AB35E | field=name=test value=test\n\n**You do NOT need to specify every property, only the ones you want.**' \
                  '\n**All properties and the syntax:**\ntitle=words\ndescription=words\ncolor=hexvalue\nimage=url_to_image (must be https)\nthumbnail=url_to_image\nauthor=words **OR** author=name=words icon=url_to_image\nfooter=words ' \
                  '**OR** footer=name=words icon=url_to_image\nfield=name=words value=words (you can add as many fields as you want)\nptext=words\n\n**NOTE:** After the command is sent, the bot will delete your message and replace it with ' \
                  'the embed. Make sure you have it saved or else you\'ll have to type it all again if the embed isn\'t how you want it.'
            await self.bot.send_message(ctx.message.channel, bot_prefix + msg)
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def game(self, ctx, *, game: str = None):
        """Set playing status. Ex: >game napping >help game for more info

        Your game status will not show for yourself, only other people can see it. This is a limitation of how the client works and how the api interacts with the client.

        To set a rotating game status, do >game game1 | game2 | game3 | etc.
        It will then prompt you with an interval in seconds to wait before changing the game and after that the order in which to change (in order or random)
        Ex: >game with matches | sleeping | watching anime"""
        if game:

            # Cycle games if more than one game is given.
            if ' | ' in game:
                await self.bot.send_message(ctx.message.channel, bot_prefix + 'Input interval in seconds to wait before changing to the next game (``n`` to cancel):')

                def check(msg):
                    return msg.content.isdigit() or msg.content.lower().strip() == 'n'

                def check2(msg):
                    return msg.content == 'random' or msg.content.lower().strip() == 'r' or msg.content.lower().strip() == 'order' or msg.content.lower().strip() == 'o'

                reply = await self.bot.wait_for_message(author=ctx.message.author, check=check, timeout=60)
                if not reply:
                    return
                if reply.content.lower().strip() == 'n':
                    return await self.bot.send_message(ctx.message.channel, bot_prefix + 'Cancelled')
                elif reply.content.strip().isdigit():
                    interval = int(reply.content.strip())
                    if interval >= 10:
                        self.bot.game_interval = interval
                        games = game.split(' | ')
                        if len(games) != 2:
                            await self.bot.send_message(ctx.message.channel, bot_prefix + 'Change game in order or randomly? Input ``o`` for order or ``r`` for random:')
                            s = await self.bot.wait_for_message(author=ctx.message.author, check=check2, timeout=60)
                            if not s:
                                return
                            if s.content.strip() == 'r' or s.content.strip() == 'random':
                                await self.bot.send_message(ctx.message.channel,
                                                            bot_prefix + 'Game set. Game will randomly change every ``%s`` seconds' % reply.content.strip())
                                loop_type = 'random'
                            else:
                                loop_type = 'ordered'
                        else:
                            loop_type = 'ordered'

                        if loop_type == 'ordered':
                            await self.bot.send_message(ctx.message.channel,
                                                        bot_prefix + 'Game set. Game will change every ``%s`` seconds' % reply.content.strip())

                        games = {'games': game.split(' | '), 'interval': interval, 'type': loop_type}
                        with open('settings/games.json', 'w') as g:
                            json.dump(games, g, indent=4)

                        self.bot.game = game.split(' | ')[0]

                    else:
                        return await self.bot.send_message(ctx.message.channel, bot_prefix + 'Cancelled. Interval is too short. Must be at least 10 seconds.')

            # Set game if only one game is given.
            else:
                self.bot.game_interval = None
                self.bot.game = game
                games = {'games': str(self.bot.game), 'interval': '0', 'type': 'none'}
                with open('settings/games.json', 'w') as g:
                    json.dump(games, g, indent=4)
                await self.bot.change_presence(game=discord.Game(name=game))
                await self.bot.send_message(ctx.message.channel, bot_prefix + 'Game set as: ``Playing %s``' % game)

        # Remove game status.
        else:
            self.bot.game_interval = None
            self.bot.game = None
            await self.bot.change_presence(game=None)
            await self.bot.send_message(ctx.message.channel, bot_prefix + 'Set playing status off')
            if os.path.isfile('settings/games.json'):
                os.remove('settings/games.json')

    @commands.group(aliases=['avatars'], pass_context=True)
    async def avatar(self, ctx):
        """Rotate avatars. See README for more info."""

        if ctx.invoked_subcommand is None:
            with open('settings/avatars.json', 'r+') as a:
                avi_config = json.load(a)
            if avi_config['password'] == '':
                return await self.bot.send_message(ctx.message.channel, bot_prefix + 'Cycling avatars requires you to input your password. Your password will not be sent anywhere and no one will have access to it. '
                                                                                     'Enter your password with``>avatar password <password>`` Make sure you are in a private channel where no one can see!')
            if avi_config['interval'] != '0':
                self.bot.avatar = None
                self.bot.avatar_interval = None
                avi_config['interval'] = '0'
                with open('settings/avatars.json', 'w') as avi:
                    json.dump(avi_config, avi, indent=4)
                await self.bot.send_message(ctx.message.channel, bot_prefix + 'Disabled cycling of avatars.')
            else:
                if os.listdir('avatars'):
                    await self.bot.send_message(ctx.message.channel, bot_prefix + 'Enabled cycling of avatars. Input interval in seconds to wait before changing avatars (``n`` to cancel):')

                    def check(msg):
                        return msg.content.isdigit() or msg.content.lower().strip() == 'n'

                    def check2(msg):
                        return msg.content == 'random' or msg.content.lower().strip() == 'r' or msg.content.lower().strip() == 'order' or msg.content.lower().strip() == 'o'
                    interval = await self.bot.wait_for_message(author=ctx.message.author, check=check, timeout=60)
                    if not interval:
                        return
                    if interval.content.lower().strip() == 'n':
                        return await self.bot.send_message(ctx.message.channel, bot_prefix + 'Cancelled.')
                    elif int(interval.content) < 1800:
                        return await self.bot.send_message(ctx.message.channel, bot_prefix + 'Cancelled. Interval is too short. Must be at least 1800 seconds (30 minutes).')
                    else:
                        avi_config['interval'] = int(interval.content)
                    if len(os.listdir('avatars')) != 2:
                        await self.bot.send_message(ctx.message.channel, bot_prefix + 'Change avatars in order or randomly? Input ``o`` for order or ``r`` for random:')
                        cycle_type = await self.bot.wait_for_message(author=ctx.message.author, check=check2, timeout=60)
                        if not cycle_type:
                            return
                        if cycle_type.content.strip() == 'r' or cycle_type.content.strip() == 'random':
                            await self.bot.send_message(ctx.message.channel,
                                                        bot_prefix + 'Avatar cycling enabled. Avatar will randomly change every ``%s`` seconds' % interval.content.strip())
                            loop_type = 'random'
                        else:
                            loop_type = 'ordered'
                    else:
                        loop_type = 'ordered'
                    avi_config['type'] = loop_type
                    if loop_type == 'ordered':
                        await self.bot.send_message(ctx.message.channel,
                                                    bot_prefix + 'Avatar cycling enabled. Avatar will change every ``%s`` seconds' % interval.content.strip())
                    with open('settings/avatars.json', 'r+') as avi:
                        avi.seek(0)
                        avi.truncate()
                        json.dump(avi_config, avi, indent=4)
                    self.bot.avatar_interval = interval.content
                    self.bot.avatar = random.choice(os.listdir('avatars'))

                else:
                    await self.bot.send_message(ctx.message.channel, bot_prefix + 'No images found under ``avatars``. Please add images (.jpg .jpeg and .png types only) to that folder and try again.')

    @avatar.command(aliases=['pass', 'pw'], pass_context=True)
    async def password(self, ctx, *, msg):
        """Set your discord acc password to rotate avatars. See README for more info."""
        with open('settings/avatars.json', 'r+') as a:
            avi_config = json.load(a)
            avi_config['password'] = msg.strip().strip('"').lstrip('<').rstrip('>')
            a.seek(0)
            a.truncate()
            json.dump(avi_config, a, indent=4)
        await self.bot.delete_message(ctx.message)
        return await self.bot.send_message(ctx.message.channel, bot_prefix + 'Password set. Do ``>avatar`` to toggle cycling avatars.')

    @commands.command(pass_context=True, aliases=['pick'])
    async def choose(self, ctx, *, choices: str):
        """Choose randomly from the options you give. >choose this | that"""
        await self.bot.send_message(ctx.message.channel, bot_prefix + 'I choose: ``{}``'.format(random.choice(choices.split("|"))))

    @commands.command(pass_context=True, aliases=['emote'])
    async def emoji(self, ctx, *, msg):
        """Embed a custom emoji (from any server). Ex: >emoji :smug:"""
        msg = msg.strip(':')
        url = None
        exact_match = False
        for server in self.bot.servers:
            for emoji in server.emojis:
                if msg.strip().lower() in str(emoji):
                    url = emoji.url
                if msg.strip() == str(emoji).split(':')[1]:
                    url = emoji.url
                    exact_match = True
                    break
            if exact_match:
                break
        if embed_perms(ctx.message) and url:
            em = discord.Embed()
            em.set_image(url=url)
            await self.bot.send_message(ctx.message.channel, content=None, embed=em)
        elif not embed_perms(ctx.message) and url:
            await self.bot.send_message(ctx.message.channel, url)
        else:
            await self.bot.send_message(ctx.message.channel, bot_prefix + 'Could not find emoji.')

        return await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        """Get response time."""
        msgtime = ctx.message.timestamp.now()
        await self.bot.send_message(ctx.message.channel, bot_prefix + ' pong')
        now = datetime.datetime.now()
        ping = now - msgtime
        if embed_perms(ctx.message):
            pong = discord.Embed(title='Response Time:', description=str(ping), color=0x7A0000)
            pong.set_thumbnail(url='http://odysseedupixel.fr/wp-content/gallery/pong/pong.jpg')
            await self.bot.send_message(ctx.message.channel, content=None, embed=pong)
        else:
            await self.bot.send_message(ctx.message.channel, bot_prefix + '``Response Time: %s``' % str(ping))

    @commands.command(pass_context=True)
    async def quote(self, ctx, *, msg: str = None):
        """Quote a message. >help quote for more info.

        >quote - quotes the last message sent in the channel.
        >quote <words> - tries to search for a message in the server that contains the given words and quotes it.
        >quote <message_id> - quotes the message with the given message id. Ex: >quote 302355374524644290(Enable developer mode to copy message ids)."""
        result = channel = None
        await self.bot.delete_message(ctx.message)
        if msg:
            length = len(self.bot.all_log[ctx.message.channel.id + ' ' + ctx.message.server.id])
            if length < 201:
                size = length
            else:
                size = 200
            for channel in ctx.message.server.channels:
                if str(channel.type) == 'text':
                    if channel.id + ' ' + ctx.message.server.id in self.bot.all_log:
                        for i in range(length - 2, length - size, -1):
                            try:
                                search = self.bot.all_log[channel.id + ' ' + ctx.message.server.id][i]
                            except:
                                continue
                            if (ctx.message.clean_content[6:].lower().strip() in search[0].clean_content.lower() and (search[0].author != ctx.message.author or search[0].content[:7] != '>quote ')) or (ctx.message.clean_content[6:].strip() == search[0].id):
                                result = search[0]
                                break
                        if result:
                            break
            if not result:
                for channel in ctx.message.server.channels:
                    async for sent_message in self.bot.logs_from(channel, limit=500):
                        if (msg.lower().strip() in sent_message.clean_content and (sent_message.author != ctx.message.author or sent_message.clean_content[:7] != '>quote ')) or (msg.strip() == sent_message.id):
                            result = sent_message
                            break
                    if result:
                        break
        else:
            channel = ctx.message.channel
            search = self.bot.all_log[ctx.message.channel.id + ' ' + ctx.message.server.id][-2]
            result = search[0]
        if result:
            if embed_perms(ctx.message) and result.content:
                em = discord.Embed(description=result.content, timestamp=result.timestamp, color=0xbc0b0b)
                em.set_author(name=result.author.name, icon_url=result.author.avatar_url)
                if channel != ctx.message.channel:
                    em.set_footer(text='Sent in: {}'.format(channel.name))
                await self.bot.send_message(ctx.message.channel, embed=em)
            else:
                await self.bot.send_message(ctx.message.channel, '%s - %s```%s```' % (result.author.name, result.timestamp, result.content))
        else:
            await self.bot.send_message(ctx.message.channel, bot_prefix + 'No quote found.')

    @commands.command(pass_context=True)
    async def poll(self, ctx, *, msg):
        """Create a strawpoll. Ex: >poll Favorite color = Blue | Red | Green"""
        try:
            options = [op.strip() for op in msg.split('|')]
            if '=' in options[0]:
                title, options[0] = options[0].split('=')
                options[0] = options[0].strip()
            else:
                title = 'Poll by %s' % ctx.message.author.name
        except:
            return await self.bot.send_message(ctx.message.channel, bot_prefix + 'Invalid Syntax. Example use: ``>poll Favorite color = Blue | Red | Green | Purple``')

        poll = strawpy.create_poll(title.strip(), options)
        await self.bot.send_message(ctx.message.channel, bot_prefix + poll.url)

    @commands.command(pass_context=True)
    async def calc(self, ctx, *, msg):
        """Simple calculator. Ex: >calc 2+2"""
        equation = msg.strip().replace('^', '**')
        if '=' in equation:
            left = eval(equation.split('=')[0])
            right = eval(equation.split('=')[1])
            answer = str(left == right)
        else:
            answer = str(eval(equation))
        if embed_perms(ctx.message):
            em = discord.Embed(color=0xD3D3D3, title='Calculator')
            em.add_field(name='Input:', value=msg.replace('**', '^'), inline=False)
            em.add_field(name='Output:', value=answer, inline=False)
            await self.bot.send_message(ctx.message.channel, content=None, embed=em)
            await self.bot.delete_message(ctx.message)
        else:
            await self.bot.send_message(ctx.message.channel, bot_prefix + answer)

    @commands.command(pass_context=True)
    async def l2g(self, ctx, *, msg: str):
        """Creates a googleitfor.me link. Ex: >l2g how do i become cool."""
        lmgtfy = 'http://googleitfor.me/?q='
        words = msg.lower().strip().split(' ')
        for word in words:
            lmgtfy += word + '+'
        await self.bot.send_message(ctx.message.channel, bot_prefix + lmgtfy[:-1])
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def d(self, ctx, *, txt: str = None):
        """Deletes the last message sent or n messages sent. Ex: >d 5"""

        # If number of seconds/messages are specified
        if txt:
            if txt[0] == '!':
                killmsg = self.bot.self_log[ctx.message.channel.id][len(self.bot.self_log[ctx.message.channel.id]) - 2]
                timer = int(txt[1:].strip())

                # Animated countdown because screw rate limit amirite
                destroy = await self.bot.edit_message(ctx.message, bot_prefix + 'The above message will self-destruct in:')
                msg = await self.bot.send_message(ctx.message.channel, '``%s  |``' % timer)
                for i in range(0, timer, 4):
                    if timer - 1 - i == 0:
                        await self.bot.delete_message(destroy)
                        msg = await self.bot.edit_message(msg, '``0``')
                        break
                    else:
                        msg = await self.bot.edit_message(msg, '``%s  |``' % int(timer - 1 - i))
                        await asyncio.sleep(1)
                    if timer - 1 - i != 0:
                        if timer - 2 - i == 0:
                            await self.bot.delete_message(destroy)
                            msg = await self.bot.edit_message(msg, '``0``')
                            break
                        else:
                            msg = await self.bot.edit_message(msg, '``%s  /``' % int(timer - 2 - i))
                            await asyncio.sleep(1)
                    if timer - 2 - i != 0:
                        if timer - 3 - i == 0:
                            await self.bot.delete_message(destroy)
                            msg = await self.bot.edit_message(msg, '``0``')
                            break
                        else:
                            msg = await self.bot.edit_message(msg, '``%s  -``' % int(timer - 3 - i))
                            await asyncio.sleep(1)
                    if timer - 3 - i != 0:
                        if timer - 4 - i == 0:
                            await self.bot.delete_message(destroy)
                            msg = await self.bot.edit_message(msg, '``0``')
                            break
                        else:
                            msg = await self.bot.edit_message(msg, '``%s  \ ``' % int(timer - 4 - i))
                            await asyncio.sleep(1)
                await self.bot.edit_message(msg, ':bomb:')
                await asyncio.sleep(.5)
                await self.bot.edit_message(msg, ':fire:')
                await self.bot.edit_message(killmsg, ':fire:')
                await asyncio.sleep(.5)
                await self.bot.delete_message(msg)
                await self.bot.delete_message(killmsg)
            else:
                await self.bot.delete_message(self.bot.self_log[ctx.message.channel.id].pop())
                deleted = 0
                async for sent_message in self.bot.logs_from(ctx.message.channel, limit=200):
                    if sent_message.author == ctx.message.author:
                        try:
                            await self.bot.delete_message(self.bot.self_log[ctx.message.channel.id].pop())
                            deleted += 1
                        except:
                            pass
                        if deleted == int(txt):
                            break

        # If no number specified, delete message immediately
        else:
            await self.bot.delete_message(self.bot.self_log[ctx.message.channel.id].pop())
            await self.bot.delete_message(self.bot.self_log[ctx.message.channel.id].pop())

    @commands.command(pass_context=True)
    async def spoiler(self, ctx, *, msg: str):
        """Spoiler tag. Ex: >spoiler Some book | They get married."""
        try:
            if " | " in msg:
                spoiled_work, spoiler = msg.lower().split(" | ", 1)
            else:
                spoiled_work, _, spoiler = msg.lower().partition(" ")
            await self.bot.edit_message(ctx.message, bot_prefix + 'Spoiler for `' + spoiled_work + '`: \n`'
            + ''.join(map(lambda c: chr(ord('a') + (((ord(c) - ord('a')) + 13) % 26)) if c >= 'a' and c <= 'z' else c, spoiler))
            + '`\n' + bot_prefix + 'Use http://rot13.com to decode')
        except:
            await self.bot.send_message(ctx.message.channel, bot_prefix + 'Could not encrypt spoiler.')

    @commands.group(pass_context=True)
    async def gist(self, ctx):
        """Posts to gist"""
        if ctx.invoked_subcommand is None:
            url = PythonGists.Gist(description='Created in channel: {} in server: {}'.format(ctx.message.channel, ctx.message.server), content=ctx.message.content[6:], name='Output')
            await self.bot.send_message(ctx.message.channel, bot_prefix + 'Gist output: ' + url)
            await self.bot.delete_message(ctx.message)

    @gist.command(pass_context=True)
    async def file(self, ctx, *, msg):
        """Create gist of file"""
        try:
            with open(msg) as fp:
                output = fp.read()
                url = PythonGists.Gist(description='Created in channel: {} in server: {}'.format(ctx.message.channel, ctx.message.server), content=output, name=msg.replace('/', '.'))
                await self.bot.send_message(ctx.message.channel, bot_prefix + 'Gist output: ' + url)
        except:
            await self.bot.send_message(ctx.message.channel, bot_prefix + 'File not found.')
        finally:
            await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def regional(self, ctx, *, msg):
        """Replace letters with regional indicator emojis"""
        await self.bot.delete_message(ctx.message)
        msg = list(msg)
        regional_list = [self.regionals[x.lower()] if x.isalnum() else x for x in msg]
        regional_output = '  '.join(regional_list)
        await self.bot.send_message(ctx.message.channel, regional_output)

    @commands.command(pass_context=True)
    async def space(self, ctx, *, msg):
        """Add n spaces between each letter. Ex: >space 2 thicc"""
        await self.bot.delete_message(ctx.message)
        if msg.split(' ', 1)[0].isdigit():
            spaces = int(msg.split(' ', 1)[0]) * ' '
            msg = msg.split(' ', 1)[1].strip()
        else:
            spaces = ' '
        spaced_message = '{}'.format(spaces).join(list(msg))
        await self.bot.send_message(ctx.message.channel, spaced_message)

    #print unicode converted :emoji: to the console.
    @commands.command(pass_context=True)
    async def uni(self, ctx):
        print(self.bot.self_log[ctx.message.channel.id].pop().content)

    #given String reactMe, return a list of emojis that can construct the string with no duplicates (for the purpose of reacting)
    #TODO make it consider reactions already applied to the message
    @commands.command(pass_context=True, aliases=['r'])
    async def react(self, ctx, msg: str, msg_id = "last", preferCombine: bool = False):
        """Add letter(s) as reaction to previous message. Ex: >react hot"""
        await self.bot.delete_message(ctx.message)
        msg = msg.lower()
        
        if msg_id == "last" or msg_id == "0" or msg_id == "1":
            msg_id = None
        else:
            msg_id = int(msg_id)
        
        if msg_id:
            limit = 25
        else:
            limit = 1

        reactions = []
        nonUnicodeEmojiList = []
        reactMe = "" #this is the string that will hold all our unicode converted characters from msg

        #replace all custom server emoji <:emoji:123456789> with "<" and add emoji ids to nonUnicodeEmojiList
        charIndex = 0
        while charIndex < len(msg):
            reactMe += msg[charIndex]
            if msg[charIndex]=='<':
                if (charIndex != len(msg) - 1) and msg[charIndex+1] == ":":
                    nameEndColon = msg[charIndex+2:].index(':')+charIndex
                    idEnd = msg[nameEndColon+2:].index('>')+nameEndColon
                    nonUnicodeEmojiList.append(msg[nameEndColon+3:idEnd+2]) #we add the custom emoji to the list to replace '<' later
                    charIndex = idEnd+2 #jump ahead in reactMe parse
                else:
                    raise Exception("Can't react with '<'")
            charIndex += 1
        if Misc.hasDupe(nonUnicodeEmojiList):
            raise Exception("You requested that I react with at least two of the exact same specific emoji. I'll try to find alternatives for alphanumeric text, but if you specify a specific emoji must be used, I can't help.")

        reactMeOriginal = reactMe #we'll go back to this version of reactMe if preferCombine is false but we can't make the reaction happen unless we combine anyway.

        if Misc.hasDupe(reactMe): #there's a duplicate letter somewhere, so let's go ahead try to fix it.
            if preferCombine: #we want a smaller reaction string, so we'll try to combine anything we can right away
                reactMe = Misc.replaceCombos(reactMe)
            reactMe = Misc.replaceLetters(reactMe)

            if Misc.hasDupe(reactMe): #check if we were able to solve the dupe
                if not preferCombine: #we wanted the most legible reaction string possible, even if it was longer, but unfortunately that's not possible, so we're going to combine first anyway
                    reactMe = reactMeOriginal
                    reactMe = Misc.replaceCombos(reactMe)
                    reactMe = Misc.replaceLetters(reactMe)
                    if Misc.hasDupe(reactMe): #this failed too, so there's really nothing we can do anymore.
                        raise Exception("Tried a lot to get rid of the dupe, but couldn't. reactMe: "+reactMe)
                else:
                    raise Exception("Tried a lot to get rid of the dupe, but couldn't. reactMe: "+reactMe)

            ltCount=0
            for char in reactMe:
                if char != "<":
                    if char not in "0123456789": #these unicode characters are weird and actually more than one character.
                        if char != '⃣': #</3
                            reactions.append(char)
                    else:
                        reactions.append(self.emojiDict[char][0])
                else:
                    reactions.append(discord.utils.get(self.bot.get_all_emojis(), id=nonUnicodeEmojiList[ltCount]))
                    ltCount+=1
        else: #probably doesn't matter, but by treating the case without dupes seperately, we can save some time
            ltCount=0
            for char in reactMe:
                if char != "<":
                    if char in "abcdefghijklmnopqrstuvwxyz0123456789!?":
                        reactions.append(self.emojiDict[char][0])
                    else:
                        reactions.append(char)
                else:
                    reactions.append(discord.utils.get(self.bot.get_all_emojis(), id=nonUnicodeEmojiList[ltCount]))
                    ltCount+=1

        async for message in self.bot.logs_from(ctx.message.channel, limit=limit):
            if (not msg_id and message.id != ctx.message.id) or (str(msg_id) == message.id):
                for i in reactions:
                    await self.bot.add_reaction(message, i)

def setup(bot):
    bot.add_cog(Misc(bot))
