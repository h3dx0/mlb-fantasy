from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import datetime
import logging
from config import LEAGUE_ID
from league import League
from team import Team

updater = Updater(token='1998454464:AAFDiMUoQTEPuer4P-gjvlNH4oHOeJcDhbc')
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def matchups_info(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /matchups is issued."""
    league = League(LEAGUE_ID)
    scoreboard = league.get_scoreboard
    matchups = scoreboard['matchups']
    total_matchups = scoreboard['total_matchups']
    messages = league.get_matchups_as_str_message(matchups=matchups, total_matchups=total_matchups)

    update.message.reply_text(messages)


def get_team_info(update: Update, context: CallbackContext):
    team = Team(team_id='404.l.79962.t.3')
    message = f'Team for today : {datetime.datetime.today().date()}\n {team.get_roster_as_str_message()}'
    update.message.reply_text(message)


start_handler = CommandHandler('start', start)
matchup_handler = CommandHandler('matchups', matchups_info)
team_handler = CommandHandler('my_team', get_team_info)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(matchup_handler)
dispatcher.add_handler(team_handler)

updater.start_polling()