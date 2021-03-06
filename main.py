# coding: utf-8

"""
MIT License

Copyright (c) 2021-2022 Akkey

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Module import
from operator import ne
import re

from nextcord.errors import LoginFailure
from nextcord.ext.commands.errors import UserNotFound
from nextcord.permissions import PermissionOverwrite
print("[StartUp]ライブラリ「re」をインポートしました")
from json.decoder import JSONDecodeError
print("[StartUp]ライブラリ「json」のパッケージ「decoder」に含まれている「JsonDecodeError」をインポートしました")
import nest_asyncio
print("[StartUp]ライブラリ「nest_asyncio」をインポートしました")
import datetime
print("[StartUp]ライブラリ「datetime」をインポートしました")
import traceback
print("[StartUp]ライブラリ「traceback」をインポートしました")
import requests
print("[StartUp]ライブラリ「requests」をインポートしました")
import nextcord
print("[StartUp]ライブラリ「nextcord」をインポートしました")
import dateutil.parser
print("[StartUp]ライブラリ「dateutil」をインポートしました")
import asyncio
print("[StartUp]ライブラリ「asyncio」をインポートしました")
import json
print("[StartUp]ライブラリ「json」をインポートしました")
import yaml
print("[StartUp]ライブラリ「yaml」をインポートしました")
from dateutil.tz import *
from nextcord.ext import commands, tasks
print("[StartUp]ライブラリ「nextcord」のパッケージ「commands」をインポートしました")
from nextcord.ext.commands import CommandNotFound, CommandOnCooldown, NotOwner, MemberNotFound, RoleNotFound, MissingRequiredArgument, MissingPermissions
print("[StartUp]ライブラリ「nextcord」のパッケージ「CommandNotFound」をインポートしました")
print("[StartUp]ライブラリ「nextcord」のパッケージ「CommandOnCooldown」をインポートしました")
print("[StartUp]ライブラリ「nextcord」のパッケージ「NotOwner」をインポートしました")
print("[StartUp]ライブラリ「nextcord」のパッケージ「MemberNotFound」をインポートしました")
print("[StartUp]ライブラリ「nextcord」のパッケージ「RoleNotFound」をインポートしました")
print("[StartUp]ライブラリ「nextcord」のパッケージ「MissingRequiredArgument」をインポートしました")
print("[StartUP]ライブラリ「nextcord」のパッケージ「MissingPermissions」をインポートしました")
# Module import

# RuntimeError防止
nest_asyncio.apply()
print("[StartUp]nest_asyncioを適応しました")
# RuntimeError防止

# 関数
def get_mute_role(gid): # mute関連に使用
	with open("mute.json", "r") as f:
		mute_role_ids = json.load(f)
	return mute_role_ids[str(gid)]
print("[StartUp]関数「get_mute_role」をロードしました")

def mc_status(t, address, port): # minecraft関連のコマンドに使用
	if t == "normal":
		api_url = f"https://api.minetools.eu/ping/{address}/{port}"
		response = requests.get(api_url)
		return response.json()
	if t == "query":
		api_url = f"https://api.minetools.eu/query/{address}/{port}"
		response = requests.get(api_url)
		return response.json()
print("[StartUp]関数「mc_status」をロードしました")

def ip_lookup(ip): # lookupコマンドで使用
	response = requests.get(f"http://ip-api.com/json/{ip}?fields=status,continent,country,regionName,city,lat,lon,timezone,isp,org,reverse,mobile,proxy,hosting,query")
	return response.json()
print("[StartUp] 関数「ip_lookup」をロードしました")

def Start_up_message(): # on_ready()関数で使用
	version = ConfigLoad["version"]
	print("Bot has been launch")
	print(f"Bot version is {version}")
print("[StartUp]関数「Start_up_message」をロードしました")

def get_prefix_bot(bot, message): # commandsのBot関数で使用
	with open("prefix.json", "r") as f:
		prefixes = json.load(f)
	try:
		return prefixes[str(message.guild.id)]
	except:
		return "."
print("[StartUp]関数「get_prefix」をロードしました")

def get_prefix_id(gid):
	with open("prefix.json", "r") as f:
		prefixes = json.load(f)
	try:
		return prefixes[str(gid)]
	except:
		return "."

time_layout = {'s': 'seconds', 'm': 'minutes', 'h': 'hours', 'd': 'days', 'w': 'weeks'}
def convert_seconds(time): # 時間計算
    return int(datetime.timedelta(**{time_layout.get(m.group('unit').lower(), 'seconds'): int(m.group('val'))for m in re.finditer(r'(?P<val>\d+)(?P<unit>[smhdw]?)', time, flags=re.I)}).total_seconds())
print("[StartUp]関数「convert_seconds」をロードしました")
# Function

# Class
class mute_easy_reason(nextcord.ui.View):
	def __init__(self, *, timeout = 60):
		super().__init__(timeout=timeout)
		self.value = None
	@nextcord.ui.select(
		custom_id="reason",
		placeholder="理由選択",
		options= [
			nextcord.SelectOption(label="不審なアカウント", value="doubt_user", description="該当のユーザーが不審であるという理由に設定します。"),
			nextcord.SelectOption(label="スパム", value="spam_user", description="スパム行為という理由に設定します。"),
			nextcord.SelectOption(label="無駄なメンション", value="mention", description="無駄なメンションを行ったという理由に設定します。"),
			nextcord.SelectOption(label="その他(カスタム)", value="custom", description="任意に理由を設定します。"),
			nextcord.SelectOption(label="無し", value="null", description="理由無しに設定します。")
		]
	)
	async def easy_reason_menu(self, select: nextcord.ui.Select, interaction: nextcord.Interaction):
		self.value = select.values[0]

class ban_easy_reason(nextcord.ui.View):
	def __init__(self, *, timeout = 60):
		super().__init__(timeout=timeout)
		self.value = None
	@nextcord.ui.select(
		custom_id="reason",
		placeholder="理由選択",
		options= [
			nextcord.SelectOption(label="不審なアカウント", value="doubt_user", description="該当のユーザーが不審であるという理由に設定します。"),
			nextcord.SelectOption(label="荒らし", value="spam_user", description="荒らし行為という理由に設定します。"),
			nextcord.SelectOption(label="その他(カスタム)", value="custom", description="任意に理由を設定します。"),
			nextcord.SelectOption(label="無し", value="null", description="理由無しに設定します。")
		]
	)
	async def easy_reason_menu(self, select: nextcord.ui.Select, interaction: nextcord.Interaction):
		self.value = select.values[0]
# Class

# Config load
ConfigOpen = open("config.yml", "r", encoding="utf-8")
ConfigLoad = yaml.safe_load(ConfigOpen) 
print("[StartUp]Jsonファイル「config.yml」をロードしました")
# Config load

# Settings
prefix = ConfigLoad["prefix"]
owners = []

bot = commands.AutoShardedBot(
	command_prefix=(get_prefix_bot),
	help_command=None,
	owner_ids = set(owners),
	intents=nextcord.Intents.all(),
	shard_count=10
)

bot.remove_command("help")
print("[StartUp]設定をロードしました。")
# Settings

# Error処理
@bot.event
async def on_command_error(_error, error):
	if isinstance(error, CommandNotFound):
		print("[Defined error]想定済みのエラー(CommandNotFound)が発生しました。")
		await _error.reply("そのコマンドは存在しません。")
		return
	elif isinstance(error, CommandOnCooldown):
		print("[Defined error]想定済みのエラー(CommandOnCooldown)が発生しました。")
		await _error.reply("次のコマンドを実行するには数秒間待つ必要があります。")
		return
	elif isinstance(error, NotOwner):
		print("[Defined error]想定済みのエラー(NotOwner)が発生しました。")
		await _error.reply("そのコマンドは限られたユーザーのみが実行できます。")
		return
	elif isinstance(error, MemberNotFound):
		print("[Defined error]想定済みのエラー(MemberNotFound)が発生しました。")
		await _error.reply("ユーザーが見つかりませんでした。")
		return
	elif isinstance(error, RoleNotFound):
		print("[Defined error]想定済みのエラー(RoleNotFound)が発生しました。")
		await _error.reply("ロールが見つかりませんでした。")
		return
	elif isinstance(error, MissingRequiredArgument):
		print("[Defined error]想定済みのエラー(MissingRequiredArgument)が発生しました。")
		await _error.reply("コマンドの引数が足りていません。")
		return
	elif isinstance(error, MissingPermissions):
		print("[Defined error]想定済みのエラー(MissingPermissions)が発生しました。")
		await _error.reply("Bot自体の権限が足りません。")
		return
	elif isinstance(error, PermissionError):
		print("[Defined error]想定済みのエラー(PermissionError)が発生しました。")
		await _error.reply("Bot自体の権限が足りません。")
		return
	elif isinstance(error, NotOwner):
		print("[Defined error]想定済みのエラー(NotOwner)が発生しました。")
		await _error.reply("そのコマンドは特定のユーザーのみが実行できます。")
		return
	else:
		main_python_error = getattr(error, "original", error)
		error_message = "".join(traceback.TracebackException.from_exception(main_python_error).format())
		error_embed = nextcord.Embed(title="エラー", description="Botで予期せぬエラーが発生しました。")
		error_embed.add_field(name="エラーが起きた原因", value="予期せぬエラーは、開発者が想定していないエラーです。\n基本的に開発者に報告することをお勧めします。\nただし、対処法が1つだけあるため、それだけ確認してから報告することを推奨します。", inline=False)
		error_embed.add_field(name="解決法", value="**この方法で治る可能性は低いです**\nresetコマンドを実行して、リセットが完了するまで待ちます。\nリセットが完了したらエラーが解決しているか確かめてみてください。\nもし解決していなかったら報告する必要があります。", inline=False)
		error_embed.add_field(name="エラー文", value=f"```powershell\n{error_message}\n```")
		await _error.send(embed=error_embed)
		print(f"[Undefined error]想定外のエラーが発生しました。\n=== エラー スタート ===\n{error_message}\n=== エラー終了 ===")
		return

	raise error
# Error処理

@tasks.loop(seconds=15)
async def loop():
	await bot.change_presence(activity=nextcord.Game(name=f'{len(bot.guilds)}servers', type=1))

# Bot Events
@bot.event
async def on_ready():
	if ConfigLoad["start-notify"] == "true":
		Start_up_message()
		await bot.change_presence(activity=nextcord.Game(name=f'{len(bot.guilds)}servers', type=1))
		notify_channel_id = ConfigLoad["chid"]
		notify_channel = await bot.fetch_channel(int(notify_channel_id))
		version = ConfigLoad["version"]
		await notify_channel.send("Bot has been launch")
		await notify_channel.send(f"Bot version is {version}")
	else:
		Start_up_message()
		await bot.change_presence(activity=nextcord.Game(name=f'{len(bot.guilds)}servers', type=1))

@bot.event
async def on_guild_join(guild):
	print(f"サーバー「{guild.name}」へ参加しました")
	if guild.system_channel:
		try:
			await guild.system_channel.send(f'AkkeyBotの導入誠にありがとうございます。\n「{get_prefix_id(guild.id)}help cmd 1」で全てのコマンドを表示することができます。\nhelpコマンドの「1」の所を変えるとページを変えることができます。')
		except nextcord.errors.Forbidden:
			pass
	with open("mute.json", "r") as f:
		mute_role_ids = json.load(f)
	mute_role_ids[str(guild.id)] = "0"
	with open("mute.json", "w") as f:
		json.dump(mute_role_ids, f, indent=4)
	with open("prefix.json", "r") as f:
		guilds_prefix = json.load(f)
	guilds_prefix[str(guild.id)] = "."
	with open("prefix.json", "w") as f:
		json.dump(guilds_prefix, f, indent=4)
	with open("amm.json", "r") as f:
		amm_data = json.load(f)
	amm_data[str(guild.id)] = {}
	amm_data[str(guild.id)]["amm"] = "0"
	amm_data[str(guild.id)]["maxuser"] = "3"
	amm_data[str(guild.id)]["maxrole"] = "5"
	amm_data[str(guild.id)]["mute"] = "0"
	with open("amm.json", "w") as f:
		json.dump(amm_data, f, indent=4)

@bot.event
async def on_guild_remove(guild):
	print(f"サーバー「{guild.name}」から離脱しました")
	with open("mute.json", "r") as f:
		mute_role_ids = json.load(f)
	try:
		mute_role_ids.pop(str(guild.id))
		with open("mute.json", "w") as f:
			json.dump(mute_role_ids, f, indent=4)
	except KeyError:
		pass
	with open("prefix.json", "r") as f:
		prefixes = json.load(f)
	try:
		prefixes.pop(str(guild.id))
		with open("prefix.json", "w") as f:
			json.dump(prefixes, f, indent=4)
	except KeyError:
		pass
	with open("amm.json", "r") as f:
		amm_data = json.load(f)
	try:
		amm_data.pop(str(guild.id))
		with open("amm.json", "w") as f:
			json.dump(amm_data, f, indent=4)
	except KeyError:
		pass
# Bot Events

@bot.command()
async def help(help, t=None, page=None):
	if t == "cmd":
		if page == None:
			await help.send(f"コマンド「{get_prefix_id(help.guild.id)}help cmd 1」でコマンド一覧を表示できます。\n(ページ: 0/5)")
		elif page == "1":
			HelpPage1 = nextcord.Embed(title="コマンド一覧 - 1", description="説明の最初に「x」がついている場合は、特定の権限が必要です。")
			HelpPage1.add_field(name="reset", value="x | Botの設定をすべて再設定します。(初期化)", inline=False)
			HelpPage1.add_field(name="say [type(msg/ embed)] [message]", value="x | Botに言葉をしゃべらせることができます。", inline=False)
			HelpPage1.add_field(name="roleper [@MentionRole]", value="o | メンションしたロールの権限を見ることができます。", inline=False)
			HelpPage1.add_field(name="memberper [@Mention]", value="o | メンションしたユーザーの権限を見ることができます。", inline=False)
			HelpPage1.add_field(name="getmcsv [type(normal / query)*] [Minecraftサーバーのアドレス*] [Minecraftサーバーのポート*]", value="o | 指定したサーバーの参加人数やpingを取得します。", inline=False)
			await help.send(embed=HelpPage1)
		elif page == "2":
			HelpPage2 = nextcord.Embed(title="コマンド一覧 - 2", description="説明の最初に「x」がついている場合は、特定の権限が必要です。")
			HelpPage2.add_field(name="warn [type(warn / toggle / punish / limit)] [settings]", value="x | Warnの設定と実行を行います", inline=False)
			HelpPage2.add_field(name="user [@Mention / UserID]", value="o | IDのユーザーの情報を取得します。", inline=False)
			HelpPage2.add_field(name="banlist", value="x | サーバーからBanされているユーザーを一覧します。", inline=False)
			HelpPage2.add_field(name="kick [@Mentioin] [Reason]", value="x | ユーザーのKickを実行します。", inline=False)
			HelpPage2.add_field(name="tempban [@Mention / UserID] [Time(s:秒 / m:分 / h:時間 / w:週間)] [Reason]", value="x | 一時的なBanを行います。", inline=False)
			await help.send(embed=HelpPage2)
		elif page == "3":
			HelpPage3 = nextcord.Embed(title="コマンド一覧 - 3", description="説明の最初に「x」がついている場合は、特定の権限が必要です。")
			HelpPage3.add_field(name="ban [@Mention / UserID] [Reason]", value="x | プレイヤーをBanします", inline=False)
			HelpPage3.add_field(name="unban [UserID]", value="x | 指定のユーザーをUnBanします。", inline=False)
			HelpPage3.add_field(name="report [Content]", value="o | 不具合等の報告ができます。")
			HelpPage3.add_field(name="ping", value="o | Botのpingを測定します。", inline=False)
			HelpPage3.add_field(name="slowmode [delay(seconds / max: 6h)]", value="x | 簡単にそのチャンネルの低速モードを設定できます。", inline=False)
			await help.send(embed=HelpPage3)
		elif page == "4":
			HelpPage4 = nextcord.Embed(title="コマンド一覧 - 4", description="説明の最初に「x」がついている場合は、特定の権限が必要です。")
			HelpPage4.add_field(name="lookup [IP]", value="o | IPの情報をAPIで検索します。", inline=False)
			HelpPage4.add_field(name="mute [type(set / mute)] [id(user / role)]", value="x | ユーザーのミュートとアンミュートを行います", inline=False)
			HelpPage4.add_field(name="qi [@Mention]", value="o | 特定のBotの招待リンクを発行します。", inline=False)
			HelpPage4.add_field(name="amm [type(user / role / toggle / mute)] [settings]", value="x | AntiMassMentionsの設定を行います。", inline=False)
			HelpPage4.add_field(name="dupe [type(role / category)] [既存のCategory ID(or Role ID)] [New Category Name(or Role Name)]", value="x | カテゴリまたはロールを複製します。", inline=False)
			await help.send(embed=HelpPage4)
		else:
			await help.send("無効な引数です。")
	elif t == "features":
		Features = nextcord.Embed(title="機能", description="Botの特徴を見ることができます。")
		Features.add_field(name="簡単なbanとtempban", value="メンションでもIDでもユーザーを素早くBanすることができます。\nまた、サーバーに入っていないユーザーもBanすることができます。\nこれにより、素早くまたは事前にユーザーをBanできます。", inline=False)
		Features.add_field(name="カスタマイズ可能な設定", value="サーバーごとにPrefixやミュートロールを設定できます。\nそのため、Prefixで複数のBotが反応してしまうことがありません。\nそして、ロールを勝手に作ってほしくないサーバーにもおすすめです。\nミュートロールを完全にカスタマイズできます。", inline=False)
		Features.add_field(name="サーバーの作成を支援", value="slowmodeやdupeでサーバーの作成を簡単にします。\nカテゴリやロールを複製できるため、何回も権限を設定する必要はなくなります!", inline=False)
		await help.send(embed=Features)
	else:
		await help.send("無効な引数です。")

@bot.command()
@commands.cooldown(1, 60, commands.BucketType.guild)
async def ping(ping):
	print("[Run]コマンド「ping」が実行されました")
	ping_value = round(bot.latency, 1)
	ping_result = nextcord.Embed(title="Ping測定", description=f"Ping値: {ping_value}ms", color=0x7cfc00)
	await ping.edit(embed=ping_result)

@bot.command()
@commands.cooldown(1, 900, commands.BucketType.guild)
async def reset(reset):
	if not reset.author.guild_permissions.administrator:
		await reset.send("サーバーの管理者権限が必要です。")
		return
	guild = reset.guild
	wait_request_message = await reset.send("リセット中です...")
	with open("mute.json", "r") as f:
		mute_role_ids = json.load(f)
	mute_role_ids[str(guild.id)] = "0"
	with open("mute.json", "w") as f:
		json.dump(mute_role_ids, f, indent=4)
	with open("prefix.json", "r") as f:
		guilds_prefix = json.load(f)
	guilds_prefix[str(guild.id)] = "."
	with open("prefix.json", "w") as f:
		json.dump(guilds_prefix, f, indent=4)
	with open("amm.json", "r") as f:
		amm_data = json.load(f)
	amm_data[str(guild.id)] = {}
	amm_data[str(guild.id)]["amm"] = "0"
	amm_data[str(guild.id)]["maxuser"] = "3"
	amm_data[str(guild.id)]["maxrole"] = "5"
	amm_data[str(guild.id)]["mute"] = "0"
	with open("amm.json", "w") as f:
		json.dump(amm_data, f, indent=4)
	await wait_request_message.edit("リセットが完了しました。")
	
@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def warn(warn, set_content=None, member: nextcord.Member=None):
	print("[Run]コマンド「warn」が実行されました")
	if warn.author.guild_permissions.administrator:
		await warn.send("管理者権限が必要です。")
		return
	if set_content == "warn":
		with open("warn.json", "r") as file:
			warn_data = json.load(file)
		if warn_data[str(warn.guild.id)]["warn"] == "0":
			await warn.send("Warn機能が有効ではありません。")
		try:
			get_warns = warn_data[str(warn.guild.id)][str(member.id)]
		except KeyError:
			get_warns = "0"
		int_get_warns = int(get_warns)
		int_get_warns += 1
		warn_data[str(warn.guild.id)][str(member.id)] = str(int_get_warns)
		with open("warn.json", "w") as file:
			json.dump(warn_data, file, indent=4)
		muted_status = "No"
		if int(int_get_warns) > int(warn_data[str(warn.guild.id)]["limit"]):
			with open("mute.json", "r", encoding="utf-8") as file:
				mute_role_ids = json.load(file)
			guild = bot.get_guild(warn.guild.id)
			role = guild.get_role(int(mute_role_ids[str(warn.guild.id)]))
			member = guild.get_member(member.id)
			await member.add_roles(role)
			muted_status = "Muted"
		await warn.send("Warnをユーザーに与えました。\nミュートステータス: " + muted_status)
	elif set_content == "toggle":
		with open("warn.json", "r") as file:
			warn_data = json.load(file)
		if warn_data[str(warn.guild.id)]["warn"] == "0":
			warn_data[str(warn.guild.id)]["warn"] = "1"
		elif warn_data[str(warn.guild.id)]["warn"] == "1":
			warn_data[str(warn.guild.id)]["warn"] = "0"
		with open("warn.json", "w") as file:
			json.dump(warn_data, file, indent=4)
		await warn.send("設定しました。")
	elif set_content == "punish":
		with open("warn.json", "r") as file:
			warn_data = json.load(file)
		if warn_data[str(warn.guild.id)]["warn"] == "0":
			await warn.send("Warnが無効です。")
			return
		await warn.send("**Kick** / **Ban** / **Mute**\nどれかをメッセージで送信してください。(Default: Ban)")
		def check(m):
			return warn.author.id == m.author.id
		try:
			msg = await bot.wait_for("message", check=check, timeout=30)
		except asyncio.TimeoutError:
			await warn.send("タイムアウトです。")
			return
		if msg.content == "Kick":
			warn_data[str(warn.guild.id)]["punish"] = "Kick"
			await warn.send("Limitに達した時の処置をKickに設定しました。")
		elif msg.content == "Ban":
			warn_data[str(warn.guild.id)]["punish"] = "Ban"
			await warn.send("Limitに達した時の処置をBanに設定しました。")
		elif msg.content == "Mute":
			warn_data[str(warn.guild.id)]["punish"] = "Mute"
			await warn.send("Limitに達した時の処置をMuteに設定しました。")
		else:
			await warn.send("無効な選択です。")
			return
		with open("warn.json", "w") as file:
			json.dump(warn_data, file, indent=4)
	elif set_content == "limit":
		with open("warn.json", "r") as file:
			warn_data = json.load(file)
		if warn_data[str(warn.guild.id)]["warn"] == "0":
			await warn.send("Warnが無効です。")
			return
		await warn.send("最大何個のWarnを受けたら処置をするか、メッセージで送信してください。(Default: 3)")
		def check(m):
			return warn.author.id == m.author.id
		try:
			msg = await bot.wait_for("message", check=check, timeout=30)
		except asyncio.TimeoutError:
			await warn.send("タイムアウトです。")
			return
		try:
			int(msg.content)
		except TypeError:
			await warn.send("無効な数値です。")
			return
		warn_data[str(warn.guild.id)]["limit"] = msg.content
		await warn.send("設定しました。")
		with open("warn.json", "w") as file:
			json.dump(warn_data, file, indent=4)

@bot.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def amm(amm, settings_type=None, set_content=None):
	print("[Run]コマンド「amm」が実行されました")
	if not amm.author.guild_permissions.administrator:
		await amm.send("貴方はこのコマンドを使用する権限がありません")
		return
	with open("amm.json", "r", encoding="utf-8") as file:
		amm_data = json.load(file)
	if settings_type == "toggle":
		if set_content == "on":
			if amm_data[str(amm.guild.id)]["amm"] == "1":
				error_message = await amm.send("すでにAntiMassMentionsは有効化済みです。")
				await asyncio.sleep(5000)
				await error_message.delete()
				return
			amm_data[str(amm.guild.id)]["amm"] = "1"
			await amm.send("AntiMassMentionsを有効にしました。")
		elif set_content == "off":
			if amm_data[str(amm.guild.id)]["amm"] == "0":
				error_message = await amm.send("すでにAntiMassMentionsは無効化済みです。")
				await asyncio.sleep(5000)
				await error_message.delete()
				return
			amm_data[str(amm.guild.id)]["amm"] = "0"
			await amm.send("AntiMassMentionsを無効にしました。")
		else:
			error_message = await amm.send("無効なToggleタイプです。")
			await asyncio.sleep(5000)
			await error_message.delete()
			return
	elif settings_type == "user":
		if amm_data[str(amm.guild.id)]["amm"] == "0":
			error_message = await amm.send("AntiMassMentionsは無効です。")
			await asyncio.sleep(5000)
			await error_message.delete()
			return
		try:
			max_mentions = int(set_content)
		except TypeError:
			error_message = await amm.send("メンションの許容量が不正です。")
			await asyncio.sleep(5000)
			await error_message.delete()
			return
		if max_mentions < 3 or max_mentions > 50:
			error_message = await amm.send("許容量が3より少ないか、50より多いです。")
			await asyncio.sleep(5000)
			await error_message.delete()
			return
		amm_data[str(amm.guild.id)]["maxuser"] = str(set_content)
		await amm.send(f"ユーザーメンション許容量を{set_content}に設定しました。")
	elif settings_type == "role":
		if amm_data[str(amm.guild.id)]["amm"] == "0":
			error_message = await amm.send("AntiMassMentionsは無効です。")
			await asyncio.sleep(5000)
			await error_message.delete()
			return
		try:
			max_mentions = int(set_content)
		except TypeError:
			error_message = await amm.send("メンションの許容量が不正です。")
			await asyncio.sleep(5000)
			await error_message.delete()
			return
		if max_mentions < 2 or max_mentions > 25:
			error_message = await amm.send("許容量が2より少ないか、15より多いです。")
			await asyncio.sleep(5000)
			await error_message.delete()
			return
		amm_data[str(amm.guild.id)]["maxrole"] = str(set_content)
		await amm.send(f"ユーザーメンション許容量を{set_content}に設定しました。")
	elif settings_type == "mute":
		if set_content == "on":
			if amm_data[str(amm.guild.id)]["mute"] == "1":
				error_message = await amm.send("すでにAntiMassMentionsのMuteは有効化済みです。")
				await asyncio.sleep(5000)
				await error_message.delete()
				return
			amm_data[str(amm.guild.id)]["mute"] = "1"
			await amm.send("AntiMassMentionsのMuteを有効にしました。")
		elif set_content == "off":
			if amm_data[str(amm.guild.id)]["mute"] == "0":
				error_message = await amm.send("すでにAntiMassMentionsのMuteは無効化済みです。")
				await asyncio.sleep(5000)
				await error_message.delete()
				return
			amm_data[str(amm.guild.id)]["mute"] = "0"
			await amm.send("AntiMassMentionsのMuteを無効にしました。")
		else:
			error_message = await amm.send("無効なToggleMuteタイプです。")
			await asyncio.sleep(5000)
			await error_message.delete()
			return
	else:
		error_message = await amm.send("不正なAMMオプションです。")
		await asyncio.sleep(5000)
		await error_message.delete()
		return
	with open("amm.json", "w") as file:
		json.dump(amm_data, file, indent=4)

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def dupe(dupe, t, id, name):
	print("[Run]コマンド「dupe」が実行されました")
	if not dupe.author.guild_permissions.administrator:
		await dupe.send("このコマンドの実行には管理者権限が必要です。")
		return
	if t == "Category":
		guild = bot.get_guild(int(dupe.guild.id))
		for category in guild.categories:
			if category.id == int(id):
				await guild.create_category(name=name, overwrites=category.overwrites)
				category_dupe_complete = nextcord.Embed(title="完了", description="カテゴリを複製しました。", color=0x7cfc00)
				await dupe.send(embed=category_dupe_complete)
				return
		category_unknown_error = nextcord.Embed(title="カテゴリが見つかりませんでした", description="該当のカテゴリが見つかりませんでした。\nidを確認してください。")
		await dupe.send(embed=category_unknown_error)
	elif t == "Role":
		guild = bot.get_guild(int(dupe.guild.id))
		try:
			role = guild.get_role(int(id))
		except RoleNotFound:
			role_unknown_error = nextcord.Embed(title="ロールが見つかりませんでした", description="該当のロールが見つかりませんでした。\nidを確認してください。")
			await dupe.send(embed=role_unknown_error)
			return
		try:
			set_role_perms = role.permissions.value
		except AttributeError:
			role_dupe_attribute_error = nextcord.Embed(title="原因不明のエラーが発生しました", description="原因が不明のエラーが発生しました。")
			role_dupe_attribute_error.add_field(name="可能性の高い原因", value="- roleの設定が異常(通常ではできない設定)\n- 存在しないロール", inline=False)
			await dupe.send(embed=role_dupe_attribute_error)
		try:
			await guild.create_role(name=name, permissions=nextcord.Permissions(permissions=int(set_role_perms)), color=int(role.color))
		except MissingPermissions:
			permissions_none = nextcord.Embed(title="権限が足りません", description="Botに権限がなかったため、ロールの複製ができませんでした。\nロールの管理権限が必要です。")
			await dupe.send(embed=permissions_none)
			return
		role_dupe_complete = nextcord.Embed(title="完了", description="ロールを複製しました。")
		await dupe.send(embed=role_dupe_complete)
	else:
		dupe_type_invalid = nextcord.Embed(title="引数タイプ無効", description="引数にしているタイプが無効です。\n<Category>または<Role>を指定する必要があります。")
		await dupe.send(embed=dupe_type_invalid)

@bot.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def server(server):
	print("[Run]コマンド「server」が実行されました")
	guild = bot.get_guild(server.guild.id)
	guild_create_time = guild.created_at
	guild_name = guild.name
	guild_id = guild.id
	guild_icon = f"https://cdn.discordapp.com/icons/{guild_id}/{guild.icon}"
	guild_rules_channel = guild.rules_channel
	guild_member_count = guild.member_count
	guild_afk_channel = guild.afk_channel
	guild_afk_time = guild.afk_timeout
	guild_2fa = guild.mfa_level
	guild_verify = guild.verification_level
	guild_boost_count = guild.premium_subscription_count
	guild_roles = guild.roles
	roles = []
	for entry in guild_roles:
		if entry.name == "@everyone":
			continue
		roles.append(f"• {entry.name}")
	if guild_2fa == 0:
		guild_2fa = "不要"
	else:
		guild_2fa = "必要"
	if guild_verify == 0:
		guild_verify = "誰も活動可能"
	elif guild_verify == 1:
		guild_verify = "メール認証必須"
	elif guild_verify == 2:
		guild_verify = "Discordに登録してから5分"
	elif guild_verify == 3:
		guild_verify = "サーバーに参加してから10分"
	else:
		guild_verify = "電話認証必須"
	ServerStatus_1 = nextcord.Embed(title="サーバーステータス - 基本情報", description=f"サーバー名: {guild_name}\nサーバーID: {guild_id}\nサーバーアイコンURL: {guild_icon}\nメンバー数: {guild_member_count}")
	ServerStatus_2 = nextcord.Embed(title="サーバーステータス - 詳細情報", description=f"ルールチャンネル: {guild_rules_channel}\n AFKチャンネル: {guild_afk_channel}\nAFK時間: {guild_afk_time}\nサーバーブースト: {guild_boost_count}\n管理の二段階認証: {guild_2fa}\n認証レベル: {guild_verify}\n作成日: {guild_create_time}")
	ServerRoles = nextcord.Embed(title="ロール一覧", description=format("\n".join(roles)))
	await server.send(embed=ServerStatus_1)
	await server.send(embed=ServerStatus_2)
	try:
		await server.send(embed=ServerRoles)
	except:
		return

@bot.command()
async def qi(qi, b=None, permscode="8"):
	print("[Run]コマンド「qi」が実行されました")
	if b == None:
		bot_select_none = nextcord.Embed(title="Bot無し", description="Botが指定されていません。\nそのため、招待リンクを発行できませんでした。")
		await qi.send(embed=bot_select_none)
		return
	a = b.replace("<", "")
	b = a.replace("@", "")
	c = b.replace("!", "")
	d = c.replace(">", "")
	e = d.replace("&", "")
	bot_user = e
	try:
		permission_code = int(permscode)
	except:
		bot_perms_noint = nextcord.Embed(title="権限コードエラー", description="指定された権限コードは数字以外が使われています。\n権限コードを利用してください。")
		await qi.send(embed=bot_perms_noint)
		return
	bot_invite_created = nextcord.Embed(title="リンクを発行しました。", description=f"リンクを発行しました。[ここ](https://discord.com/api/oauth2/authorize?client_id={bot_user}&permissions={permission_code}&scope=bot)から招待できます。")
	await qi.send(embed=bot_invite_created)

@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def lookup(lookup, ip=None):
	print("[Run]コマンド「lookup」が実行されました")
	if ip == None:
		await lookup.send("IPアドレスを指定してください。")
		return
	response = ip_lookup(ip)
	status_get = response["status"]
	if status_get == "fail":
		await lookup.send("情報を取得できませんでした。")
		return
	IPAddress = response["query"] # IP
	Continent = response["continent"] # エリア
	Country = response["country"] # 国
	Region = response["regionName"] # 都道府県
	City = response["city"] # 市 / 区
	Lat = response["lat"] # 緯度
	Lon = response["lon"] # 経度
	Timezone = response["timezone"] # タイムゾーン
	ISP = response["isp"] # ISP名
	ORG = response["org"] # ORG名
	Reverse = response["reverse"] # 逆引き
	Hosting = response["hosting"]
	Mobile = response["mobile"] # モバイル回線
	Proxy = response["proxy"] # Proxyステータス
	if Mobile == "true":
		UsingMobile = "使用"
	else:
		UsingMobile = "不使用"

	if Proxy == "true":
		UsingProxy = "使用"
	else:
		UsingProxy = "不使用"
	if Hosting == "true":
		Special = "特殊回線"
	else:
		Special = "通常回線"
	await lookup.send(f"IPアドレスの情報\nIP: {IPAddress}\nエリア: {Continent}\n国: {Country}\n都道府県: {Region}\n市 / 区: {City}\n緯度: {Lat}\n経度: {Lon}\nタイムゾーン: {Timezone}\nISP: {ISP}\nORG: {ORG}\n逆引き: {Reverse}\nモバイル回線: {UsingMobile}\nProxy使用: {UsingProxy}\n回線タイプ: {Special}")

@bot.command()
@commands.cooldown(1, 120, commands.BucketType.user)
async def say(say, type="msg", *, content):
	print("[Run]コマンド「say」が実行されました")
	if say.author.guild_permissions.administrator:
		await say.send("管理者権限が必要です。")
		return
	try:
		ch = await bot.fetch_channel(say.channel.id)
		msg = await ch.fetch_message(say.id)
		await msg.delete()
	except MissingPermissions:
		pass
	if say.author.guild_permissions.administrator:
		if type == "msg":
			await say.send(f"{content}")
		elif type == "embed":
			Embed = nextcord.Embed(description=f"{content}")
			await say.send(embed=Embed)
		else:
			await say.send("引数が無効です。")
	else:
		await say.send("管理者以外は実行することができません。")

@bot.command()
@commands.cooldown(1, 120, commands.BucketType.user)
async def mute(mute, settype, id, reason=None):
	print("[Run]コマンド「mute」が実行されました")
	if mute.author.guild_permissions.administrator:
		guild = bot.get_guild(mute.guild.id)
		if settype == "set":
			with open("mute.json", "r") as f:
				mute_role_ids = json.load(f)
			mute_role_ids[str(mute.guild.id)] = str(id)
			with open("mute.json", "w") as f:
				json.dump(mute_role_ids, f, indent=4)
			await mute.send(f"ロールのIDを{id}設定しました。")
		elif settype == "mute":
			a = id.replace("<", "")
			b = a.replace("@", "")
			c = b.replace("!", "")
			d = c.replace(">", "")
			e = d.replace("&", "")
			id = e
			def interaction_check(interaction_info):
				return mute.author.id == interaction_info.user.id
			def new_reason_check(new_reason_info):
				return mute.author.id == new_reason_info.author.id
			if reason == None:
				view = mute_easy_reason()
				await mute.send("ミュートの理由を選択してください。", view=view)
				interaction = await bot.wait_for(event="interaction", check=interaction_check)
				if interaction.data["values"][0] == "doubt_user":
					reason = "不審なユーザー"
				elif interaction.data["values"][0] == "spam_user":
					reason = "スパム行為をした"
				elif interaction.data["values"][0] == "mention":
					reason = "無駄なメンション行為"
				elif interaction.data["values"][0] == "custom":
					await mute.send("理由を設定してください。")
					new_reason = await bot.wait_for("message", check=new_reason_check)
					reason = new_reason.content
				elif interaction.data["values"][0] == "null":
					pass
			with open("mute.json", "r") as f:
				mute_role_ids = json.load(f)
			mute_role = mute_role_ids[str(guild.id)]
			user = guild.get_member(int(id))
			role = guild.get_role(int(mute_role))
			try:
				await user.add_roles(role, reason=reason)
			except:
				ExceptionError = nextcord.Embed(title="エラー", description="ミュートが正常にできませんでした。")
				await mute.send(embed=ExceptionError)
				return
			await mute.send(f"{user}をミュートしました。")
		elif settype == "unmute":
			a = id.replace("<", "")
			b = a.replace("@", "")
			c = b.replace("!", "")
			d = c.replace(">", "")
			e = d.replace("&", "")
			id = e
			with open("mute.json", "r") as f:
				mute_role_ids = json.load(f)
			mute_role = mute_role_ids[str(guild.id)]
			user = guild.get_member(int(id))
			role = guild.get_role(int(mute_role))
			try:
				await user.remove_roles(role)
			except:
				ExceptionError = nextcord.Embed(title="エラー", description="ミュート解除が正常にできませんでした。")
				await mute.send(embed=ExceptionError)
			await mute.send(f"{user}さんのロールを解除しました。")
	else:
		await mute.send("権限が足りません。\nミュートを実行するには管理者権限保有者でなければ行けません。")

@bot.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def roleper(roleper, role: nextcord.Role):
	if role.permissions.administrator:
		administrator=':green_circle:'
	else:
		administrator='::red_circle:'
	if role.permissions.view_audit_log:
		view_audit_log=':green_circle:'
	else:
		view_audit_log=':red_circle:'
	if role.permissions.view_guild_insights:
		view_guild_insights=':green_circle:'
	else:
		view_guild_insights=':red_circle:'
	if role.permissions.manage_guild:
		manage_guild=':green_circle:'
	else:
		manage_guild=':red_circle:'
	if role.permissions.manage_roles:
		manage_roles=':green_circle:'
	else:
		manage_roles=':red_circle:'
	if role.permissions.manage_channels:
		manage_channels=':green_circle:'
	else:
		manage_channels=':red_circle:'
	if role.permissions.kick_members:
		kick_members=":green_circle:"
	else:
		kick_members=':red_circle:'
	if role.permissions.ban_members:
		ban_members=':green_circle:'
	else:
		ban_members=':red_circle:'
	if role.permissions.create_instant_invite:
		create_instant_invite=':green_circle:'
	else:
		create_instant_invite=':red_circle:'
	if role.permissions.change_nickname:
		change_nickname=':green_circle:'
	else:
		change_nickname=':red_circle:'
	if role.permissions.manage_nicknames:
		manage_nicknames=':green_circle:'
	else:
		manage_nicknames=':red_circle:'
	if role.permissions.manage_emojis:
		manage_emojis=':green_circle:'
	else:
		manage_emojis=':red_circle:'
	if role.permissions.manage_webhooks:
		manage_webhooks=':green_circle:'
	else:
		manage_webhooks=':red_circle:'
	if role.permissions.view_channel:
		view_channel=':green_circle:'
	else:
		view_channel=':red_circle:'
	if role.permissions.send_messages:
		send_messages=':green_circle:'
	else:
		send_messages=':red_circle:'
	if role.permissions.send_tts_messages:
		send_tts_messages=':green_circle:'
	else:
		send_tts_messages=':red_circle:'
	if role.permissions.manage_messages:
		manage_messages=':green_circle:'
	else:
		manage_messages=':red_circle:'
	if role.permissions.embed_links:
		embed_links=':green_circle:'
	else:
		embed_links=':red_circle:'
	if role.permissions.attach_files:
		attach_files=':green_circle:'
	else:
		attach_files=':red_circle:'
	if role.permissions.read_message_history:
		read_message_history=':green_circle:'
	else:
		read_message_history=':red_circle:'
	if role.permissions.mention_everyone:
		mention_everyone=':green_circle:'
	else:
		mention_everyone=':red_circle:'
	if role.permissions.use_external_emojis:
		use_external_emojis=':green_circle:'
	else:
		use_external_emojis=':red_circle:'
	if role.permissions.add_reactions:
		add_reactions=':green_circle:'
	else:
		add_reactions=':red_circle:'
	if role.permissions.use_slash_commands:
		use_slash_commands=':green_circle:'
	else:
		use_slash_commands=':red_circle:'
	if role.permissions.connect:
		connect=':green_circle:'
	else:
		connect=':red_circle:'
	if role.permissions.speak:
		speak=':green_circle:'
	else:
		speak=':red_circle:'
	if role.permissions.mute_members:
		mute_members = ':green_circle:'
	else:
		mute_members = ':red_circle:'
	if role.permissions.deafen_members:
		deafen_members = ':green_circle:'
	else:
		deafen_members = ':red_circle:'
	if role.permissions.move_members:
		move_members = ':green_circle:'
	else:
		move_members = ':red_circle:'
	if role.permissions.use_voice_activation:
		use_voice_activation = ':green_circle:'
	else:
		use_voice_activation = ':red_circle:'
	if role.permissions.priority_speaker:
		priority_speaker = ':green_circle:'
	else:
		priority_speaker = ':red_circle:'
	print("[Run]コマンド「roleper」が実行されました")
	RolePermsResult = nextcord.Embed(title=f'ロール名: {role.name}', description=f'ロールID: {role.id}\nロール作成日: {role.created_at}\nロールの色(16進数カラーコード): {role.color}\n権限コード: {role.permissions.value}',color=0x008000)
	RolePermsResult.add_field(name='権限一覧', value=f'管理者権限: {administrator}\n\n監視ログの表示: {view_audit_log}\n\nサーバーインサイトの表示: {view_guild_insights}\n\nサーバー管理: {manage_guild}\n\nロール管理: {manage_roles}\n\nチャンネルの管理: {manage_channels}\n\nメンバーのKick: {kick_members}\n\nメンバーのBan: {ban_members}\n\nインスタント招待の作成: {create_instant_invite}\n\nニックネームの変更: {change_nickname}\n\nニックネームの管理: {manage_nicknames}\n\n絵文字の管理: {manage_emojis}\n\nWebHook管理: {manage_webhooks}\n\nチャンネルを表示: {view_channel}\n\nメッセージを送信: {send_messages}\n\nTTSメッセージの送信: {send_tts_messages}\n\nメッセージの管理: {manage_messages}\n\n埋め込みリンク: {embed_links}\n\nファイルの添付: {attach_files}\n\nメッセージ履歴を標示: {read_message_history}\n\neveryoneメンション: {mention_everyone}\n\n外部の絵文字を使用: {use_external_emojis}\n\nリアクションを追加: {add_reactions}\n\nスラッシュコマンドの使用: {use_slash_commands}\n\nボイスチャンネルへの接続: {connect}\n\nボイスチャンネルでの発言: {speak}\n\nメンバーをミュート: {mute_members}\n\nメンバーをスピーカーミュート: {deafen_members}\n\nメンバーを移動: {move_members}\n\nボイスアクティビティ: {use_voice_activation}\n\n優先スピーカー: {priority_speaker}', inline=False)
	await roleper.send(embed=RolePermsResult)

@bot.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def memberper(memberper, member: nextcord.Member):
	if member.guild_permissions.administrator:
		administrator=':green_circle:'
	else:
		administrator='::red_circle:'
	if member.guild_permissions.view_audit_log:
		view_audit_log=':green_circle:'
	else:
		view_audit_log=':red_circle:'
	if member.guild_permissions.view_guild_insights:
		view_guild_insights=':green_circle:'
	else:
		view_guild_insights=':red_circle:'
	if member.guild_permissions.manage_guild:
		manage_guild=':green_circle:'
	else:
		manage_guild=':red_circle:'
	if member.guild_permissions.manage_roles:
		manage_roles=':green_circle:'
	else:
		manage_roles=':red_circle:'
	if member.guild_permissions.manage_channels:
		manage_channels=':green_circle:'
	else:
		manage_channels=':red_circle:'
	if member.guild_permissions.kick_members:
		kick_members=":green_circle:"
	else:
		kick_members=':red_circle:'
	if member.guild_permissions.ban_members:
		ban_members=':green_circle:'
	else:
		ban_members=':red_circle:'
	if member.guild_permissions.create_instant_invite:
		create_instant_invite=':green_circle:'
	else:
		create_instant_invite=':red_circle:'
	if member.guild_permissions.change_nickname:
		change_nickname=':green_circle:'
	else:
		change_nickname=':red_circle:'
	if member.guild_permissions.manage_nicknames:
		manage_nicknames=':green_circle:'
	else:
		manage_nicknames=':red_circle:'
	if member.guild_permissions.manage_emojis:
		manage_emojis=':green_circle:'
	else:
		manage_emojis=':red_circle:'
	if member.guild_permissions.manage_webhooks:
		manage_webhooks=':green_circle:'
	else:
		manage_webhooks=':red_circle:'
	if member.guild_permissions.view_channel:
		view_channel=':green_circle:'
	else:
		view_channel=':red_circle:'
	if member.guild_permissions.send_messages:
		send_messages=':green_circle:'
	else:
		send_messages=':red_circle:'
	if member.guild_permissions.send_tts_messages:
		send_tts_messages=':green_circle:'
	else:
		send_tts_messages=':red_circle:'
	if member.guild_permissions.manage_messages:
		manage_messages=':green_circle:'
	else:
		manage_messages=':red_circle:'
	if member.guild_permissions.embed_links:
		embed_links=':green_circle:'
	else:
		embed_links=':red_circle:'
	if member.guild_permissions.attach_files:
		attach_files=':green_circle:'
	else:
		attach_files=':red_circle:'
	if member.guild_permissions.read_message_history:
		read_message_history=':green_circle:'
	else:
		read_message_history=':red_circle:'
	if member.guild_permissions.mention_everyone:
		mention_everyone=':green_circle:'
	else:
		mention_everyone=':red_circle:'
	if member.guild_permissions.use_external_emojis:
		use_external_emojis=':green_circle:'
	else:
		use_external_emojis=':red_circle:'
	if member.guild_permissions.add_reactions:
		add_reactions=':green_circle:'
	else:
		add_reactions=':red_circle:'
	if member.guild_permissions.use_slash_commands:
		use_slash_commands=':green_circle:'
	else:
		use_slash_commands=':red_circle:'
	if member.guild_permissions.connect:
		connect=':green_circle:'
	else:
		connect=':red_circle:'
	if member.guild_permissions.speak:
		speak=':green_circle:'
	else:
		speak=':red_circle:'
	if member.guild_permissions.mute_members:
		mute_members = ':green_circle:'
	else:
		mute_members = ':red_circle:'
	if member.guild_permissions.deafen_members:
		deafen_members = ':green_circle:'
	else:
		deafen_members = ':red_circle:'
	if member.guild_permissions.move_members:
		move_members = ':green_circle:'
	else:
		move_members = ':red_circle:'
	if member.guild_permissions.use_voice_activation:
		use_voice_activation = ':green_circle:'
	else:
		use_voice_activation = ':red_circle:'
	if member.guild_permissions.priority_speaker:
		priority_speaker = ':green_circle:'
	else:
		priority_speaker = ':red_circle:'
	print("[Run]コマンド「memberper」が実行されました")
	MemberPermsResult = nextcord.Embed(title=f'ユーザー: {member}', description=f'ユーザーID: {member.id}\n権限コード: {member.guild_permissions.value}',color=0x008000)
	MemberPermsResult.add_field(name='権限一覧', value=f'管理者権限: {administrator}\n\n監視ログの表示: {view_audit_log}\n\nサーバーインサイトの表示: {view_guild_insights}\n\nサーバー管理: {manage_guild}\n\nロール管理: {manage_roles}\n\nチャンネルの管理: {manage_channels}\n\nメンバーのKick: {kick_members}\n\nメンバーのBan: {ban_members}\n\nインスタント招待の作成: {create_instant_invite}\n\nニックネームの変更: {change_nickname}\n\nニックネームの管理: {manage_nicknames}\n\n絵文字の管理: {manage_emojis}\n\nWebHook管理: {manage_webhooks}\n\nチャンネルを表示: {view_channel}\n\nメッセージを送信: {send_messages}\n\nTTSメッセージの送信: {send_tts_messages}\n\nメッセージの管理: {manage_messages}\n\n埋め込みリンク: {embed_links}\n\nファイルの添付: {attach_files}\n\nメッセージ履歴を標示: {read_message_history}\n\neveryoneメンション: {mention_everyone}\n\n外部の絵文字を使用: {use_external_emojis}\n\nリアクションを追加: {add_reactions}\n\nスラッシュコマンドの使用: {use_slash_commands}\n\nボイスチャンネルへの接続: {connect}\n\nボイスチャンネルでの発言: {speak}\n\nメンバーをミュート: {mute_members}\n\nメンバーをスピーカーミュート: {deafen_members}\n\nメンバーを移動: {move_members}\n\nボイスアクティビティ: {use_voice_activation}\n\n優先スピーカー: {priority_speaker}', inline=False)
	await memberper.send(embed=MemberPermsResult)

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def getmcsv(getmcsv, t="normal", address=None, port="25565"):
	print("[Run]コマンド「getmcsv」が実行されました")
	if address == None:
		await getmcsv.send("引数が無効です。")
		return
	await getmcsv.send("サーバーの情報を取得します。")
	if t == "normal":
		try:
			status = mc_status(t="normal", address=address, port=port)
			Ping = status["latency"]
			MaxPlayer = status["players"]["max"]
			JoinPlayer = status["players"]["online"]
			ResultOutput = nextcord.Embed(title=f"{address}", description=f"Ping: {Ping}ms\n最大プレイヤー: {MaxPlayer}\nオンライン: {JoinPlayer}")
			await getmcsv.send(embed=ResultOutput)
		except:
			ExceptionError = nextcord.Embed(title="エラー", description="サーバーの情報を正常に取得できませんでした。")
			await getmcsv.send(embed=ExceptionError)
			return
	if t == "query":
		try:
			status = mc_status(t="query", address=address, port=port)
			MaxPlayer = status["MaxPlayers"]
			JoinPlayer = status["Players"]
			Motd = status["Motd"]
			Software = status["Software"]
			Plugin = status["Plugins"]
			ResultOutput = nextcord.Embed(title=f"{address}", description=f"最大プレイヤー: {MaxPlayer}\nオンライン: {JoinPlayer}\nMOTD: {Motd}\nサーバータイプ: {Software}\nプラグイン: {Plugin}")
			await getmcsv.send(embed=ResultOutput)
		except:
			ExceptionError = nextcord.Embed(title="エラー", description="サーバーの情報を正常に取得できませんでした。")
			await getmcsv.send(embed=ExceptionError)
			return

@bot.command()
@commands.cooldown(1, 120, commands.BucketType.user)
async def clear(clear, amout="10"):
	print("[Run]コマンド「clear」が実行されました")
	if clear.author.guild_permissions.administrator:
		amout = int(amout) + 1
		await clear.channel.purge(limit=amout)
		amout = int(amout) - 1
		await clear.send(f"{amout}件のメッセージを消去しました。")
	else:
		await clear.send("権限がたりません。管理者である必要があります。")
	
@bot.command()
@commands.cooldown(1, 180, commands.BucketType.user)
async def user(serach, u=None):
	print("[Run]コマンド「serach」が実行されました")
	if u == None:
		await serach.send("引数が無効です。")
		return
	a = u.replace("<", "")
	b = a.replace("@", "")
	c = b.replace("!", "")
	d = c.replace(">", "")
	e = d.replace("&", "")
	if e == "me":
		e = serach.author.id
	async def fetch_user_check(check_user):
		user = await bot.fetch_user(int(check_user))
		name = user.name
		tag = user.discriminator
		username = f"{name}#{tag}"
		id = user.id
		create_time = user.created_at
		bot_check = user.bot
		if bot_check == True:
			bot_check_jp = "Bot"
		elif bot_check == False:
			bot_check_jp = "User"
		uinfo = nextcord.Embed(title=f"{username}", description=f"ユーザー名: {username}\nID: {id}\nアカウント作成日: {create_time}\nBotステータス: {bot_check_jp}")
		uinfo.set_thumbnail(url=f"{user.avatar.url}")
		await serach.send(embed=uinfo)
	def status_jp_gen(s):
		if "online" in s:
			status_jp = ":green_circle:"
		elif "idle" in s:
			status_jp = ":yellow_circle:"
		elif "dnd" in s:
			status_jp = ":red_circle:"
		elif "offline" in s:
			status_jp = ":black_circle:"
		return status_jp
	guild = bot.get_guild(serach.guild.id)
	user = guild.get_member(int(e))
	if user == None:
		await fetch_user_check(check_user=int(e))
		return
	name = user.name
	tag = user.discriminator
	username = f"{name}#{tag}"
	id = user.id
	status = user.status
	status_phone = user.mobile_status
	status_app = user.desktop_status
	status_web = user.web_status
	nickname = user.display_name
	create_time = user.created_at
	join_time = user.joined_at
	bot_check = user.bot
	if bot_check == True:
		bot_check_jp = "Bot"
	if bot_check == False:
		bot_check_jp = "User"
	status_jp = status_jp_gen(s=status)
	phone_status_jp = status_jp_gen(s=status_phone)
	desktop_status_jp = status_jp_gen(s=status_app)
	web_status_jp = status_jp_gen(s=status_web)
	if user.guild_permissions.administrator:
		administrator=':green_circle:'
	else:
		administrator='::red_circle:'
	if user.guild_permissions.view_audit_log:
		view_audit_log=':green_circle:'
	else:
		view_audit_log=':red_circle:'
	if user.guild_permissions.view_guild_insights:
		view_guild_insights=':green_circle:'
	else:
		view_guild_insights=':red_circle:'
	if user.guild_permissions.manage_guild:
		manage_guild=':green_circle:'
	else:
		manage_guild=':red_circle:'
	if user.guild_permissions.manage_roles:
		manage_roles=':green_circle:'
	else:
		manage_roles=':red_circle:'
	if user.guild_permissions.manage_channels:
		manage_channels=':green_circle:'
	else:
		manage_channels=':red_circle:'
	if user.guild_permissions.kick_members:
		kick_members=":green_circle:"
	else:
		kick_members=':red_circle:'
	if user.guild_permissions.ban_members:
		ban_members=':green_circle:'
	else:
		ban_members=':red_circle:'
	if user.guild_permissions.create_instant_invite:
		create_instant_invite=':green_circle:'
	else:
		create_instant_invite=':red_circle:'
	if user.guild_permissions.change_nickname:
		change_nickname=':green_circle:'
	else:
		change_nickname=':red_circle:'
	if user.guild_permissions.manage_nicknames:
		manage_nicknames=':green_circle:'
	else:
		manage_nicknames=':red_circle:'
	if user.guild_permissions.manage_emojis:
		manage_emojis=':green_circle:'
	else:
		manage_emojis=':red_circle:'
	if user.guild_permissions.manage_webhooks:
		manage_webhooks=':green_circle:'
	else:
		manage_webhooks=':red_circle:'
	if user.guild_permissions.view_channel:
		view_channel=':green_circle:'
	else:
		view_channel=':red_circle:'
	if user.guild_permissions.send_messages:
		send_messages=':green_circle:'
	else:
		send_messages=':red_circle:'
	if user.guild_permissions.send_tts_messages:
		send_tts_messages=':green_circle:'
	else:
		send_tts_messages=':red_circle:'
	if user.guild_permissions.manage_messages:
		manage_messages=':green_circle:'
	else:
		manage_messages=':red_circle:'
	if user.guild_permissions.embed_links:
		embed_links=':green_circle:'
	else:
		embed_links=':red_circle:'
	if user.guild_permissions.attach_files:
		attach_files=':green_circle:'
	else:
		attach_files=':red_circle:'
	if user.guild_permissions.read_message_history:
		read_message_history=':green_circle:'
	else:
		read_message_history=':red_circle:'
	if user.guild_permissions.mention_everyone:
		mention_everyone=':green_circle:'
	else:
		mention_everyone=':red_circle:'
	if user.guild_permissions.use_external_emojis:
		use_external_emojis=':green_circle:'
	else:
		use_external_emojis=':red_circle:'
	if user.guild_permissions.add_reactions:
		add_reactions=':green_circle:'
	else:
		add_reactions=':red_circle:'
	if user.guild_permissions.use_slash_commands:
		use_slash_commands=':green_circle:'
	else:
		use_slash_commands=':red_circle:'
	if user.guild_permissions.connect:
		connect=':green_circle:'
	else:
		connect=':red_circle:'
	if user.guild_permissions.speak:
		speak=':green_circle:'
	else:
		speak=':red_circle:'
	if user.guild_permissions.mute_members:
		mute_members = ':green_circle:'
	else:
		mute_members = ':red_circle:'
	if user.guild_permissions.deafen_members:
		deafen_members = ':green_circle:'
	else:
		deafen_members = ':red_circle:'
	if user.guild_permissions.move_members:
		move_members = ':green_circle:'
	else:
		move_members = ':red_circle:'
	if user.guild_permissions.use_voice_activation:
		use_voice_activation = ':green_circle:'
	else:
		use_voice_activation = ':red_circle:'
	if user.guild_permissions.priority_speaker:
		priority_speaker = ':green_circle:'
	else:
		priority_speaker = ':red_circle:'
	roles = []
	for role in user.roles:
		if role.name == "@everyone":
			continue
		roles.append("- " + role.name)
	uinfo = nextcord.Embed(title=f"{username}", description=f"ユーザー名: {username}\nID: {id}\nニックネーム: {nickname}\nアカウント作成日: {create_time}\nサーバー参加日: {join_time}\nステータス: {status_jp}\nWebステータス: {web_status_jp}\nデスクトップステータス: {desktop_status_jp}\nスマホステータス: {phone_status_jp}\nBotステータス: {bot_check_jp}")
	uper = nextcord.Embed(title=f'権限', description=f'管理者権限: {administrator}\n\n監視ログの表示: {view_audit_log}\n\nサーバーインサイトの表示: {view_guild_insights}\n\nサーバー管理: {manage_guild}\n\nロール管理: {manage_roles}\n\nチャンネルの管理: {manage_channels}\n\nメンバーのKick: {kick_members}\n\nメンバーのBan: {ban_members}\n\nインスタント招待の作成: {create_instant_invite}\n\nニックネームの変更: {change_nickname}\n\nニックネームの管理: {manage_nicknames}\n\n絵文字の管理: {manage_emojis}\n\nWebHook管理: {manage_webhooks}\n\nチャンネルを表示: {view_channel}\n\nメッセージを送信: {send_messages}\n\nTTSメッセージの送信: {send_tts_messages}\n\nメッセージの管理: {manage_messages}\n\n埋め込みリンク: {embed_links}\n\nファイルの添付: {attach_files}\n\nメッセージ履歴を標示: {read_message_history}\n\neveryoneメンション: {mention_everyone}\n\n外部の絵文字を使用: {use_external_emojis}\n\nリアクションを追加: {add_reactions}\n\nスラッシュコマンドの使用: {use_slash_commands}\n\nボイスチャンネルへの接続: {connect}\n\nボイスチャンネルでの発言: {speak}\n\nメンバーをミュート: {mute_members}\n\nメンバーをスピーカーミュート: {deafen_members}\n\nメンバーを移動: {move_members}\n\nボイスアクティビティ: {use_voice_activation}\n\n優先スピーカー: {priority_speaker}')
	uroles = nextcord.Embed(title="ロール", description="{0}".format("\n".join(roles)))
	uinfo.set_thumbnail(url=f"{user.avatar.url}")
	await serach.send(embed=uinfo)
	await serach.send(embed=uper)
	await serach.send(embed=uroles)

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def kick(kick, member: nextcord.member, reason=None):
	print("[Run]コマンド「kick」が実行されました")
	if kick.author.guild_permissions.kick_members:
		await member.kick(reason=reason)
		KickNotify = nextcord.Embed(title="Kick", description=f"ユーザーのKickを実行しました。", color=0x008000)
		KickNotify.add_field(name="実行者の情報", value=f"名前: {kick.author}\nID: {kick.author.id}", inline=False)
		KickNotify.add_field(name="Kickされたユーザーの情報", value=f"名前: {member}\nID: {member.id}", inline=False)
		await kick.send(embed=KickNotify)
	else:
		PermissionError = nextcord.Embed(title="権限エラー", description="権限が足りません。\n少なくともKick権限が必要です。", color=0xFF0000)
		await kick.send(embed=PermissionError)
	
@bot.command()
@commands.cooldown(1, 180, commands.BucketType.user)
async def tempban(tempban, request_ban_user, time, reason=None):
	print("[Run]コマンド「tempban」が実行されました")
	if tempban.author.guild_permissions.ban_members:
		a = request_ban_user.replace("<", "")
		b = a.replace("@", "")
		c = b.replace("!", "")
		d = c.replace(">", "")
		e = d.replace("&", "")
		ban_user = e
		def interaction_check(interaction_info):
			return tempban.author.id == interaction_info.user.id
		def new_reason_check(new_reason_info):
			return tempban.author.id == new_reason_info.author.id
		if reason == None:
			view = ban_easy_reason()
			await tempban.send("一時Banの理由を選択してください。", view=view)
			interaction = await bot.wait_for(event="interaction", check=interaction_check)
			if interaction.data["values"][0] == "doubt_user":
				reason = "不審なユーザー"
			elif interaction.data["values"][0] == "spam_user":
				reason = "荒らし行為をした"
			elif interaction.data["values"][0] == "custom":
				await tempban.send("理由を設定してください。")
				new_reason = await bot.wait_for("message", check=new_reason_check)
				reason = new_reason.content
			elif interaction.data["values"][0] == "null":
				pass
		user = await bot.fetch_user(int(ban_user))
		await tempban.guild.ban(user, reason=reason)
		response = convert_seconds(time)
		BanNotify = nextcord.Embed(title="Ban", description=f"ユーザーのBanを実行しました。", color=0x008000)
		BanNotify.add_field(name="実行者の情報", value=f"名前: {tempban.author}\nID: {tempban.author.id}", inline=False)
		BanNotify.add_field(name="TempBan者の情報", value=f"名前: {user}\nID: {user.id}\n解除日: <t:{datetime.datetime.now().timestamp() + response}>", inline=False)
		await tempban.send(embed=BanNotify)
		await asyncio.sleep(int(response))
		await tempban.guild.unban(user)
	else:
		PermissionError = nextcord.Embed(title="権限エラー", description="権限が足りません。\n少なくともBan権限が必要です。", color=0xFF0000)
		await tempban.send(embed=PermissionError)

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def ban(ban, request_ban_user, reason=None):
	print("[Run]コマンド「ban」が実行されました")
	if ban.author.guild_permissions.ban_members:
		a = request_ban_user.replace("<", "")
		b = a.replace("@", "")
		c = b.replace("!", "")
		d = c.replace(">", "")
		e = d.replace("&", "")
		ban_user = e
		def interaction_check(interaction_info):
			return ban.author.id == interaction_info.user.id
		def new_reason_check(new_reason_info):
			return ban.author.id == new_reason_info.author.id
		if reason == None:
			view = ban_easy_reason()
			await ban.send("Banの理由を選択してください。", view=view)
			interaction = await bot.wait_for(event="interaction", check=interaction_check)
			if interaction.data["values"][0] == "doubt_user":
				reason = "不審なユーザー"
			elif interaction.data["values"][0] == "spam_user":
				reason = "荒らし行為をした"
			elif interaction.data["values"][0] == "custom":
				await ban.send("理由を設定してください。")
				new_reason = await bot.wait_for("message", check=new_reason_check)
				reason = new_reason.content
			elif interaction.data["values"][0] == "null":
				pass
		user = await bot.fetch_user(int(ban_user))
		await ban.guild.ban(user, reason=reason)
		BanNotify = nextcord.Embed(title="Ban", description=f"ユーザーのBanを実行しました。", color=0x008000)
		BanNotify.add_field(name="実行者の情報", value=f"名前: {ban.author}\nID: {ban.author.id}", inline=False)
		BanNotify.add_field(name="Ban者の情報", value=f"名前: {user}\nID: {user.id}", inline=False)
		await ban.send(embed=BanNotify)
	else:
		PermissionError = nextcord.Embed(title="権限エラー", description="権限が足りません。\n少なくともBan権限が必要です。", color=0xFF0000)
		await ban.send(embed=PermissionError)

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def unban(unban, id:int):
	print("[Run]コマンド「unban」が実行されました")
	if unban.author.guild_permissions.administrator:
		try:
			user = await bot.fetch_user(id)
		except UserNotFound:
			await unban.send("ユーザーが見つかりませんでした。")
			return
		await unban.guild.unban(user)
		UNBanNotify = nextcord.Embed(title="UnBan", description=f"ユーザーのUnBanを実行しました。", color=0x008000)
		UNBanNotify.add_field(name="実行者の情報", value=f"名前: {unban.author}\nID: {unban.author.id}", inline=False)
		UNBanNotify.add_field(name="UnBan者の情報", value=f"名前: {user}\nID: {user.id}", inline=False)
		await unban.send(embed=UNBanNotify)
	else:
		PError = nextcord.Embed(title="権限エラー", description="権限が足りません。\n少なくとも管理者である必要があります。", color=0xFF0000)
		await unban.send(embed=PError)

@bot.command()
@commands.cooldown(1, 180, commands.BucketType.user)
async def banlist(banlist):
	print("[Run]コマンド「banlist」が実行されました")
	bans = await banlist.guild.bans()
	data = ["• {0.name}#{0.discriminator}({0.id})".format(entry.user) for entry in bans]
	bl = nextcord.Embed(title="Ban users", description=format("\n".join(data)))
	await banlist.send(embed=bl)

@bot.command()
@commands.cooldown(1, 120, commands.BucketType.user)
async def slowmode(slowmode, delay):
	print("[Run]コマンド「slowmode」が実行されました")
	if slowmode.author.guild_permissions.manage_channels:
		response = convert_seconds(delay)
		await slowmode.channel.edit(slowmode_delay=int(response))
		await slowmode.send(f"低速モードの時間を{response}秒にしました。")
	else:
		await slowmode.send("権限が足りません。\n少なくともチャンネルの編集権限を持っている必要があります。")

@bot.command()
@commands.cooldown(1, 90, commands.BucketType.guild)
async def report(report, *, content):
	print("[Run]コマンド「report」が実行されました")
	await report.send("レポートを送信します。")
	get_user = await bot.fetch_user()
	await get_user.send(f"レポートが届きました。\n送信元: {report.author}\n内容: {content}")
	await report.send("レポートが送信されました。")

@bot.command()
@commands.cooldown(1, 300, commands.BucketType.user)
async def setpre(setpre, prefix="."):
	print("[Run]コマンド「setpre」が実行されました")
	if setpre.author.guild_permissions.administrator:
		with open('prefix.json', 'r') as f:
			prefixes = json.load(f)
		try:
			prefixes[str(setpre.guild.id)] = str(prefix)
		except KeyError:
			await setpre.send("エラーが発生しました。\nBotの再参加が必要な可能性があります。")
		with open('prefix.json', 'w') as f:
			json.dump(prefixes, f, indent=4)
		await setpre.send(f'サーバーのPrefixを「 {prefix} 」へ設定変更しました')
	else:
		await setpre.send('管理者権限のみがPrefixを設定できます')

loop.start()

try:
	bot.run(ConfigLoad["token"])
except LoginFailure:
	print("Login Failed")
	exit()

# Copyright © 2021 Akkey57492
