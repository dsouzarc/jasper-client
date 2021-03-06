#!/usr/bin/env python2
# -*- coding: utf-8-*-

import os
import sys
import shutil

# Change CWD to $JASPER_HOME/jasper/client
jasper_home = os.getenv("JASPER_HOME")
if not jasper_home or not os.path.exists(jasper_home):
    print("Error: $JASPER_HOME is not set.")
    sys.exit(0)

os.chdir(os.path.join(jasper_home, "jasper", "client"))

old_client = os.path.abspath(os.path.join(os.pardir, "old_client"))
if os.path.exists(old_client):
    shutil.rmtree(old_client)

import yaml
import sys
import speaker
import stt
from conversation import Conversation


def isLocal():
    return len(sys.argv) > 1 and sys.argv[1] == "--local"

if isLocal():
    from local_mic import Mic
else:
    from mic import Mic

if __name__ == "__main__":

    print "==========================================================="
    print " JASPER The Talking Computer                               "
    print " Copyright 2013 Shubhro Saha & Charlie Marsh               "
    print "==========================================================="

    profile = yaml.safe_load(open("profile.yml", "r"))

    try:
        api_key = profile['keys']['GOOGLE_SPEECH']
    except KeyError:
        api_key = None

    try:
        stt_engine_type = profile['stt_engine']
    except KeyError:
        print "stt_engine not specified in profile, defaulting to PocketSphinx"
        stt_engine_type = "sphinx"

    mic = Mic(speaker.newSpeaker(), stt.PocketSphinxSTT(),
              stt.newSTTEngine(stt_engine_type, api_key=api_key))

    addendum = ""
    if 'first_name' in profile:
        addendum = ", %s" % profile["first_name"]
    mic.say("How can I be of service%s?" % addendum)

    conversation = Conversation("JASPER", mic, profile)

    conversation.handleForever()
