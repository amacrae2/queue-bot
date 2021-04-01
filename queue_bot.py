from slackclient import SlackClient
import os, time
from slackqueue import SlackQueue
import random


_QUEUE = SlackQueue()

def run_bot_update_queue(sc, channel_name):
    """Check latest messages constantly and update queue."""

    # Set the channel to send messages to, based on name passed
    channel_info = sc.server.channels.find(channel_name)
    channel_id = channel_info.id

    # TODO: Add whitelist of users who are allowed to interact with queue bot
    # to make sure staff are the only ones who can manage the queue.

    # Read messages forever!
    names = set()
    while True:

        latest = sc.rtm_read()

        # Are there any new messages, and are they not the stock bot connection
        # message?
        if (latest != [] and latest != [{'text': u'hello'}]):
            latest = latest[0]

            # Make sure we're in the desired channel and the latest update
            # was actually a message, not a typing notification.
            if (latest.get("channel") == channel_id and
                latest.get("type") == "message"):

                text = latest["text"]
                print "Latest:", latest

                # _QUEUE.update(text)

                # Add a new student to the queue. Staff should still have to do
                # this manually.
                if "!add" in text.lower():

                    names.add(' '.join(text.split()[1:]))

                # # A user could be allowed to remove themselves.
                # elif "!remove" in text.lower():
                #     # user_to_remove = re.search(r"<@\w+>", text).group()
                #     names.remove(' '.join(text.split()[1:]))

                elif "!next" in text.lower():
                    # user_to_remove = re.search(r"<@\w+>", text).group()

                    names.remove(random.sample(names, 1)[0])
                    value = names.pop(' '.join(text.split()[1:]))
                    sc.rtm_send_message(
                        channel_id,
                        value
                    )

            # if _QUEUE.needs_message:
            #     sc.rtm_send_message(
            #         channel_id,
            #         _QUEUE.generate_display()
            #     )

                # _QUEUE.needs_message = False

        time.sleep(.5)


if __name__ == "__main__":

    # Get API token and instantiate a client for all our Slack
    # interactions.
    slack_token = os.environ.get("BOT_API_TOKEN")
    sc = SlackClient(slack_token)

    # Connect to slack
    if not sc.rtm_connect():
        raise Exception("Couldn't connect to slack.")

    # Try to connect to the real time messaging service
    if sc.rtm_connect():
        run_bot_update_queue(sc, "celebrity-fishbowl")
    else:
        print "Connection Failed"
