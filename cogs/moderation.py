import discord
from discord.ext import commands, tasks
from discord.ext.commands import context

class Mod(commands.Cog, name='Moderation'):

    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self,ctx, amount: int):
        await ctx.channel.purge(limit=amount+1)

    @clear.error
    async def clear_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('"ARE YOU RETARD", Put some number of messages to delete.')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('"YOU ARE NOOB", You dont have permission.')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self,ctx, member: discord.Member , * , reason=None):
        try:
            await member.kick(reason=reason)
            await ctx.send(f'{member.name} has been kick for {reason}')
        except Exception as e:
            print(e)

    @kick.error
    async def kick_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('"CAN I KICK MYSELF", Mention the member to kick.')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('"CAN I KICK YOU?" You dont have permission.')
        if ctx.author.top_role < discord.Member.top_role:
            await ctx.send("I cant kick your Dad, He is also my Dad.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban(self,ctx, member: discord.Member , * , reason=None):
        try:
            await member.ban(reason=reason)
            await ctx.send(f'{member.name} has been banned for {reason}')
        except Exception as e:
            print(e)

    @ban.error
    async def ban_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('"CAN I BAN YOU?", Mention the member to ban.')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('"CAN I BAN YOU?" You dont have permission.')
        if ctx.author.top_role < discord.Member.top_role:
            await ctx.send("CAN I CAN YOU? He is your Dad. Respect them.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unban(self,ctx, *, member):
        banned_users = await ctx.guild.bans()
        
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.channel.send(f"{user.mention} has been unbanned.")

    @unban.error
    async def unban_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('"I CANT UNBAN MYSELF?", Mention the member to unban.')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('"CAN I BAN YOU?" You dont have permission.')


    @commands.command(description="Mutes the specified user.")
    @commands.has_permissions(administrator=True)
    async def mute(self,ctx, member: discord.Member, *, reason=None):
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="Muted")

        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")

            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)

        await member.add_roles(mutedRole, reason=reason)
        await ctx.send(f"Muted {member.mention} for reason {reason}")
        await member.send(f"You were muted in the server {guild.name} for {reason}")

    @mute.error
    async def mute_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('"Why are you muted?", Mention the member to mute.')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('"NOOB!" You dont have permission.') 


    @commands.command(description="Unmutes a specified user.")
    @commands.has_permissions(administrator=True)
    async def unmute(self,ctx, member: discord.Member):
        mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

        await member.remove_roles(mutedRole)
        await ctx.send(f"Unmuted {member.mention}")
        await member.send(f"You were unmuted in the server {ctx.guild.name}")

    @unmute.error
    async def unmute_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('"Noob!", Mention the member to unban.')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('"You are Noob!!" You dont have permission.')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def dm(self,ctx,user: discord.Member,*,args):
        if args != None:
            try:
                await user.send(args)
            except:
                await ctx.send('I think that User has closed his DMs!')

    @dm.error
    async def dm_error(self,ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('"U ARE NOOB, U DONT KNOW HOW TO SEND MSG!" You dont have permission.')
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('"WASTING MY TIME,I THINK YOU DONT HAVE MSG", Put some thing to send.')

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def send(self,ctx, channelid: int , * , args):
        channel = self.bot.get_channel(channelid)
        await channel.send(args)

    @send.error
    async def send_error(self,ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You dont have permission to use this command.')
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Usage: $send [channel_id] [message]')



def setup(bot):
    bot.add_cog(Mod(bot))
    print("Mod cog is loaded!")