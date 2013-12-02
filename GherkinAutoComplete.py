#-----------------------------------------------------------------------------------
# Gherkin Auto-Complete Sublime Text Plugin
# Copyright 2013, Andy Hitchman
# Author: Andy Hitchman
# Version: 0.1
# License: MIT
# Description: Show all existing gherkin phrases within features in folder hierarchy
# Based on the work of Elad Yarkoni. Thank you!
# See http://www.eladyarkoni.com/2012/09/sublime-text-auto-complete-plugin.html
#-----------------------------------------------------------------------------------
import sublime, sublime_plugin, os, re, threading
from os.path import basename


class Phrase:
	_phrase = ''
	_predicate = ''
	_feature_name = ''
	_file_name = ''

	def __init__(self, phrase, predicate, feature_name, file_name):
		self._phrase = phrase
		self._predicate = predicate
		self._feature_name = feature_name
		self._file_name = file_name

	def phrase(self):
		return self._phrase

	def predicate(self):
		return self._predicate

	def feature_name(self):
		return self._feature_name

	def file_name(self):
		return self._file_name


class GherkinPhrases:
	phrases = []

	def clearPhrases(self):
		self.phrases = []
	
	def clearPhrasesForFeatureFile(self, file_name):
		self.phrases = [phrase for phrase in self.phrases if phrase.file_name() != file_name]

	def addPhrase(self, predicate, phrase, feature_name, file_name):
		self.phrases.append(Phrase(phrase, predicate, feature_name, file_name))

	def get_match_on(self, activePredicate):
		continuations = '|and|but'
		return '(?P<given>given' + (continuations if activePredicate == 'given' else '') + ')|\
(?P<when>when' + (continuations if activePredicate == 'when' else '') + ')|\
(?P<then>then' + (continuations if activePredicate == 'then' else '') + ')'

	def get_autocomplete_list(self, word):
		autocomplete_list = []
		for phrase in self.phrases:
			if word in phrase.phrase():
				autocomplete_list.append( (phrase.phrase() + '\t' + phrase.predicate() + ' in ' + phrase.feature_name(), phrase.phrase()) ) 
		return autocomplete_list


	def is_feature_file(self, filename):
		return '.feature' in filename


class GherkinAutoComplete(GherkinPhrases, sublime_plugin.EventListener):
	all_indexed = False

	def on_activated_async(self, view):
		if not self.all_indexed:
			self.all_indexed = True
			self.index_all_features(view.window().folders())

	def on_post_save_async(self, view):
		if self.is_feature_file(view.file_name()):
			if self.all_indexed:
				self.clearPhrasesForFeatureFile(view.file_name())
				self.index_file(view.file_name())
			else:
				self.all_indexed = True
				self.index_all_features(view.window().folders())

	def index_all_features(self, open_folders):
		self.clearPhrases()

		for folder in open_folders:
			feature_files = self.get_feature_files(folder)
			for file_name in feature_files:
				self.index_file(file_name)

	def on_query_completions(self, view, prefix, locations):
		completions = []

		if self.is_feature_file(view.file_name()):
			return self.get_autocomplete_list(prefix)

		return (completions, sublime.INHIBIT_EXPLICIT_COMPLETIONS)

	def index_file(self, file_name):
		print('Indexing gherkin phrases in ' + file_name)
		sublime.status_message('Indexing gherkin phrases in ' + file_name)
		self.index_phrases(file_name, open(file_name, 'rU'))

	# Not used at present
	def index_view(self, view):
		print('Indexing gherkin phrases in ' + view.file_name())
		sublime.status_message('Indexing gherkin phrases in ' + view.file_name())
		all_lines = view.substr(sublime.Region(0, view.size()))
		print(all_lines)
		#self.index_phrases(view.file_name(), all_lines)

	def index_phrases(self, file_name, lines):
		feature_name = file_name
		activePredicate = None
		collecting_table_data = False
		phrase = None

		for line in lines:
			match = re.match(r'^\s*feature:\s*(.*)$', line, re.IGNORECASE)
			if match != None:
				feature_name = match.group(1)

			# Collect table data or emit phrase as soon as we have no match
			if activePredicate != None:
				if re.match(r'^\s*\|', line) != None:
					phrase += ('' if collecting_table_data else '\n') + line
					collecting_table_data = True
					continue
				elif phrase != None and phrase != '':
					collecting_table_data = False
					self.addPhrase(activePredicate, phrase, feature_name, file_name)

			match_on = self.get_match_on(activePredicate)
			match = re.match(r'^\s*(?:' + match_on + ')\s+(.*)$', line, re.IGNORECASE)
			if match != None:
				if match.group('given') != None:
					activePredicate = 'given'
				elif match.group('when') != None:
					activePredicate = 'when'
				elif match.group('then') != None:
					activePredicate = 'then'

				phrase = match.group(4)
			else:
				activePredicate = None

	def get_feature_files(self, dir_name, *args):
		fileList = []

		for file in os.listdir(dir_name):
			dirfile = os.path.join(dir_name, file)
			if os.path.isfile(dirfile):
				fileName, fileExtension = os.path.splitext(dirfile)
				if fileExtension == '.feature':
					fileList.append(dirfile)
			elif os.path.isdir(dirfile):
				fileList += self.get_feature_files(dirfile, *args)

		return fileList

