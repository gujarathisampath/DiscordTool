mytitle = "DiscordTool - Developed by Sampath"
from os import system
system("title "+mytitle)
import time
import os
import discord
import asyncio
from colorama import Fore, init, Style
from datetime import datetime
from time import sleep
import requests
import getpass

os.system('cls' if os.name == 'nt' else 'clear')

print(f'''{Fore.RED}
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║                     Discord Server Cloner v1.1.0                  ║
║                                                                   ║
║                     Developer: Sampath                            ║
║                     GitHub: @gujarathisampath                     ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}''')

print(f'{Fore.RED}[WARNING]{Style.RESET_ALL} This tool is against Discord Terms of Service.')
print(f'{Fore.RED}[WARNING]{Style.RESET_ALL} Using this tool may result in account termination.')
print(f'{Fore.RED}[WARNING]{Style.RESET_ALL} Excessive use of this tool will increase the risk of detection.')
print(f'{Fore.RED}[WARNING]{Style.RESET_ALL} Use this tool at your own risk.\n')

print(f'{Fore.YELLOW}[NOTE]{Style.RESET_ALL} Community features must be enabled to clone forum and announcement channels.')
print(f'{Fore.YELLOW}[NOTE]{Style.RESET_ALL} Some features might not work due to Discord API limitations.\n')

def print_add(message):
    print(f'{Fore.GREEN}[+]{Style.RESET_ALL} {message}')

def print_delete(message):
    print(f'{Fore.RED}[-]{Style.RESET_ALL} {message}')

def print_warning(message):
    print(f'{Fore.RED}[WARNING]{Style.RESET_ALL} {message}')


def print_error(message):
    print(f'{Fore.RED}[ERROR]{Style.RESET_ALL} {message}')


class Clone:
    @staticmethod
    async def roles_delete(guild_to: discord.Guild):
            for role in guild_to.roles:
                try:
                    if role.name != "@everyone":
                        await role.delete()
                        print_delete(f"Deleted Role: {role.name}")
                except discord.Forbidden:
                    print_error(f"Error While Deleting Role: {role.name}")
                except discord.HTTPException:
                    print_error(f"Unable to Delete Role: {role.name}")

    @staticmethod
    async def roles_create(guild_to: discord.Guild, guild_from: discord.Guild):
        roles = []
        role: discord.Role
        for role in guild_from.roles:
            if role.name != "@everyone":
                roles.append(role)
        roles = roles[::-1]
        for role in roles:
            try:
                try:
                    icon = await role.icon.read()
                    await guild_to.create_role(
                        name=role.name,
                        permissions=role.permissions,
                        colour=role.colour,
                        hoist=role.hoist,
                        mentionable=role.mentionable,
                        icon=icon
                    )
                except:
                    await guild_to.create_role(
                        name=role.name,
                        permissions=role.permissions,
                        colour=role.colour,
                        hoist=role.hoist,
                        mentionable=role.mentionable
                    )
                print_add(f"Created Role {role.name}")
            except discord.Forbidden:
                print_error(f"Error While Creating Role: {role.name}")
            except discord.HTTPException:
                print_error(f"Unable to Create Role: {role.name}")

    @staticmethod
    async def channels_delete(guild_to: discord.Guild):
        for channel in guild_to.channels:
                try:
                    await channel.delete()
                    print_delete(f"Deleted Channel: {channel.name}")
                except discord.Forbidden:
                    print_error(f"Error While Deleting Channel: {channel.name}")
                except discord.HTTPException:
                    print_error(f"Unable To Delete Channel: {channel.name}")

    @staticmethod
    async def categories_create(guild_to: discord.Guild, guild_from: discord.Guild):
        channels = guild_from.categories
        channel: discord.CategoryChannel
        new_channel: discord.CategoryChannel
        for channel in channels:
            try:
                overwrites_to = {}
                for key, value in channel.overwrites.items():
                    role = discord.utils.get(guild_to.roles, name=key.name)
                    overwrites_to[role] = value
                new_channel = await guild_to.create_category(
                    name=channel.name,
                    overwrites=overwrites_to)
                await new_channel.edit(position=channel.position)
                print_add(f"Created Category: {channel.name}")
            except discord.Forbidden:
                print_error(f"Error While Deleting Category: {channel.name}")
            except discord.HTTPException:
                print_error(f"Unable To Delete Category: {channel.name}")
    
    @staticmethod
    async def channels_create(guild_to: discord.Guild, guild_from: discord.Guild, messages_count:int = None):
        channel_text: discord.TextChannel 
        channel_voice: discord.VoiceChannel
        channel_fourm: discord.ForumChannel
        category = None
        for channel_text in guild_from.text_channels:
            try:
                for category in guild_to.categories:
                    try:
                        if category.name == channel_text.category.name:
                            break
                    except AttributeError:
                        print_warning(f"Channel {channel_text.name} doesn't have any category!")
                        category = None
                        break

                overwrites_to = {}
                for key, value in channel_text.overwrites.items():
                    role = discord.utils.get(guild_to.roles, name=key.name)
                    overwrites_to[role] = value
                try:
                    
                    if channel_text.type == channel_fourm:
                        print('Bruh')
                    
                    new_channel = await guild_to.create_text_channel(
                        name=channel_text.name,
                        overwrites=overwrites_to,
                        position=channel_text.position,
                        topic=channel_text.topic,
                        slowmode_delay=channel_text.slowmode_delay,
                        nsfw=channel_text.nsfw)
                    
                except:
                    new_channel = await guild_to.create_text_channel(
                        name=channel_text.name,
                        overwrites=overwrites_to,
                        position=channel_text.position)
                if category is not None:
                    await new_channel.edit(category=category)
                print_add(f"Created Text Channel: {channel_text.name}")
                if messages_count is not None:
                    webhook = await new_channel.create_webhook(name="Test")
                    async for message in channel_text.history(limit=messages_count):
                        username = f"{message.author.name}"
                        avatar_url = str(message.author.avatar.url)
                        try:
                            await webhook.send(content=message.content, username=username, avatar_url=avatar_url, wait=True)
                        except:
                            continue
            except discord.Forbidden:
                print_error(f"Error While Creating Text Channel: {channel_text.name}")
            except discord.HTTPException:
                print_error(f"Unable To Creating Text Channel: {channel_text.name}")
        category = None
        for channel_fourm in guild_from.forum_channels:
            try:
                for category in guild_to.categories:
                    try:
                        if category.name == channel_fourm.category.name:
                            break
                    except AttributeError:
                        print_warning(f"Channel {channel_fourm.name} doesn't have any category!")
                        category = None
                        break

                overwrites_to = {}
                for key, value in channel_fourm.overwrites.items():
                    role = discord.utils.get(guild_to.roles, name=key.name)
                    overwrites_to[role] = value
                try:                    
                    new_channel = await guild_to.create_forum_channel(
                        name=channel_fourm.name,
                        overwrites=overwrites_to,
                        position=channel_fourm.position,
                        topic=channel_fourm.topic,
                        slowmode_delay=channel_fourm.slowmode_delay,
                        nsfw=channel_fourm.nsfw)
                    
                except:
                    new_channel = await guild_to.create_forum_channel(
                        name=channel_fourm.name,
                        overwrites=overwrites_to,
                        position=channel_fourm.position)
                if category is not None:
                    await new_channel.edit(category=category)
                print_add(f"Created Fourm Channel: {channel_fourm.name}")                    
            except discord.Forbidden:
                print_error(f"Error While Creating Fourm Channel: {channel_fourm.name}")
            except discord.HTTPException:
                print_error(f"Unable To Creating Fourm Channel: {channel_fourm.name}")
        category = None
        for channel_voice in guild_from.voice_channels:
            try:
                for category in guild_to.categories:
                    try:
                        if category.name == channel_voice.category.name:
                            break
                    except AttributeError:
                        print_warning(f"Channel {channel_voice.name} doesn't have any category!")
                        category = None
                        break

                overwrites_to = {}
                for key, value in channel_voice.overwrites.items():
                    role = discord.utils.get(guild_to.roles, name=key.name)
                    overwrites_to[role] = value
                try:
                    new_channel = await guild_to.create_voice_channel(
                        name=channel_voice.name,
                        overwrites=overwrites_to,
                        position=channel_voice.position,
                        bitrate=channel_voice.bitrate,
                        user_limit=channel_voice.user_limit,
                        )
                except:
                    new_channel = await guild_to.create_voice_channel(
                        name=channel_voice.name,
                        overwrites=overwrites_to,
                        position=channel_voice.position)
                if category is not None:
                    await new_channel.edit(category=category)
                print_add(f"Created Voice Channel: {channel_voice.name}")
            except discord.Forbidden:
                print_error(f"Error While Creating Voice Channel: {channel_voice.name}")
            except discord.HTTPException:
                print_error(f"Unable To Creating Voice Channel: {channel_voice.name}")


    @staticmethod
    async def emojis_delete(guild_to: discord.Guild):
        for emoji in guild_to.emojis:
            try:
                await emoji.delete()
                print_delete(f"Deleted Emoji: {emoji.name}")
            except discord.Forbidden:
                print_error(f"Error While Deleting Emoji{emoji.name}")
            except discord.HTTPException:
                print_error(f"Error While Deleting Emoji {emoji.name}")

    @staticmethod
    async def emojis_create(guild_to: discord.Guild, guild_from: discord.Guild):
        emoji: discord.Emoji
        for emoji in guild_from.emojis:
            try:
                emoji_image = await emoji.read()
                await guild_to.create_custom_emoji(
                    name=emoji.name,
                    image=emoji_image)
                print_add(f"Created Emoji {emoji.name}")
            except discord.Forbidden:
                print_error(f"Error While Creating Emoji {emoji.name} ")
            except discord.HTTPException:
                print_error(f"Error While Creating Emoji {emoji.name}")

    @staticmethod
    async def emojis_download(guild_from: discord.Guild):
        emoji: discord.Emoji
        for emoji in guild_from.emojis:
            try:
                emoji_image = await emoji.read()
                with open(f"emojis/{guild_from.id}/{emoji.name}.png", "wb") as f:
                    f.write(emoji_image)
                print_add(f"Created Emoji {emoji.name}")
                        
            except discord.Forbidden:
                print_error(f"Error While Creating Emoji {emoji.name} ")
            except discord.HTTPException:
                print_error(f"Error While Creating Emoji {emoji.name}")

    @staticmethod
    async def guild_edit(guild_to: discord.Guild, guild_from: discord.Guild):
        try:
            try:
                icon_image = await guild_from.icon.read()
            except discord.errors.DiscordException:
                print_error(f"Can't read icon image from {guild_from.name}")
                icon_image = None
            await guild_to.edit(name=f'{guild_from.name}')
            if icon_image is not None:
                try:
                    await guild_to.edit(icon=icon_image)
                    print_add(f"Guild Icon Changed: {guild_to.name}")
                except:
                    print_error(f"Error While Changing Guild Icon: {guild_to.name}")
        except discord.Forbidden:
            print_error(f"Error While Changing Guild Icon: {guild_to.name}")
            

bot = discord.Client()
def get_input(prompt):
    return input(f'{prompt}\n{Fore.MAGENTA}>{Fore.RESET}')

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    menu_options = [
        "Copy all channels",
        "Copy all roles", 
        "Copy all emojis",
        "Copy all channels (delete existing)",
        "Copy all roles (delete existing)", 
        "Copy all emojis (delete existing)",
        "Copy everything",
        "Download all emojis"
    ]
    
    print("Select an option:")
    for i, option in enumerate(menu_options, 1):
        print(f"[{Fore.RED}{i}{Style.RESET_ALL}] {option}")

# Get user inputs
token = get_input('Please enter your account token')
clear_screen()

guild_s = get_input('Please enter guild ID you want to copy from')
guild = get_input('Please enter guild ID you want to copy to')
clear_screen()

display_menu()
option = input(f'{Fore.MAGENTA}>{Fore.RESET}')
os.system('cls' if os.name == 'nt' else 'clear')
messages_count = input(f'Do you want to copy messages from the guild? (Type 0 for No, or enter a number for Yes):\n {Fore.MAGENTA}>{Fore.RESET}')
if messages_count == "0":
    messages_count = None
input_guild_id = guild_s
output_guild_id = guild
token = token

@bot.event
async def on_ready():
    system("title "+'Loading')
    print("Loading...")
    time.sleep(2)
    extrem_map = {} 
    print(f"{Fore.GREEN}[SUCCESS]{Fore.RESET} Logged In as : {Fore.BLUE}{bot.user}{Fore.RESET}")
    print(f"{Fore.GREEN}[SUCCESS]{Fore.RESET} Started Cloning")
    system("title "+'Started Cloning')
    guild_from = bot.get_guild(int(input_guild_id))
    guild_to = bot.get_guild(int(output_guild_id))
    if option == "1":
        await Clone.categories_create(guild_to, guild_from)
        await Clone.channels_create(guild_to, guild_from,messages_count)
    elif option == "2":
        await Clone.roles_create(guild_to, guild_from)
    elif option == "3":
        await Clone.emojis_create(guild_to,guild_from)
    elif option == "4":
        await Clone.channels_delete(guild_to)
        await Clone.categories_create(guild_to, guild_from)
        await Clone.channels_create(guild_to, guild_from,messages_count)
    elif option == "5":
        await Clone.roles_delete(guild_to)
        await Clone.roles_create(guild_to, guild_from)
    elif option == "6":
        await Clone.emojis_delete(guild_to)
        await Clone.emojis_create(guild_to,guild_from)
    elif option == "7":
        await Clone.guild_edit(guild_to, guild_from)
        await Clone.roles_delete(guild_to)
        await Clone.channels_delete(guild_to)
        await Clone.roles_create(guild_to, guild_from)
        await Clone.categories_create(guild_to, guild_from)
        await Clone.channels_create(guild_to, guild_from,messages_count)
        await Clone.emojis_delete(guild_to)
        await Clone.emojis_create(guild_to,guild_from)
    elif option == "8":
        await Clone.emojis_download(guild_from)
    print(f'''{Fore.GREEN}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                        CLONING COMPLETE                    
                                                          
    Source Server: {guild_from.name}
    Source ID: {guild_from.id}
    Target ID: {guild_to.id}
                                                          
    Thank you for using Discord Server Cloner!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{Style.RESET_ALL}''')
    await asyncio.sleep(5)
    
os.system('cls' if os.name == 'nt' else 'clear')
try:
    bot.run(token, bot=False)
except discord.errors.LoginFailure:
    print_error("Please enter a valid user token")