import sublime
import sublime_plugin

try:
	# Python 3
	from .commit import RandomCommitment
	from html.parser import HTMLParser

except (ValueError):
	# Python 2
	from commit import RandomCommitment
	from HTMLParser import HTMLParser

try:
    from hashlib import md5
except ImportError:
    from md5 import md5

#
# A few helpers
#

whatthecommit = 'http://whatthecommit.com/'
commitMessages = 'commit_messages.txt'
messages = {}
message_hashes = []
htmlParser = HTMLParser()

st_version = 2
if sublime.version() == '' or int(sublime.version()) > 3000:
    st_version = 3

#
# Build `messages` and `message_hashes`
# to be able to init an instance of `RandomCommitment`
#

# Sublime Text 2

if st_version == 2:

    from os import path

    messages_file = open(path.join(path.dirname(__file__), commitMessages))

    for line in messages_file.readlines():
        messages[md5(line).hexdigest()] = line

    randomMessages = RandomCommitment(messages)

# Sublime Text 3

def plugin_loaded():

        from zipfile import ZipFile

        # Is there an easier way to access files inside a .sublime-package file in Sublime Text 3?

        messages_file = ZipFile(sublime.installed_packages_path() + '/Commitment.sublime-package').open(commitMessages)

        for line in messages_file.readlines():
            messages[md5(line).hexdigest()] = line.decode('utf-8')

        CommitmentCommand.randomMessages = RandomCommitment(messages)


#
# The actual `WindowCommand`
#

class CommitmentCommand(sublime_plugin.WindowCommand):

    def run(self):

        try:

            # Sublime Text 3
            commit = self.randomMessages.get()

        except AttributeError:

            # Sublime Text 2
            commit = randomMessages.get()

        message = htmlParser.unescape(commit.get('message', '').replace('\n','').replace('<br/>', '\n'))

        message_hash = commit.get('message_hash', '')

        if message:

            print('Commitment: ' + '\n' + message + '\n' + 'Permalink: ' + whatthecommit + message_hash)

            sublime.set_clipboard(message)
            sublime.status_message(message)