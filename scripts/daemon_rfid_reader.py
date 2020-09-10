#!/usr/bin/env python3

import logging
import os
import subprocess
import time

from Reader import Reader

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

reader = Reader()

# get absolute path of this script
dir_path = os.path.dirname(os.path.realpath(__file__))
logger.info('Dir_PATH: {dir_path}'.format(dir_path=dir_path))

# vars for ensuring delay between same-card-swipes
same_id_delay = 0
previous_id = ""
previous_time = time.time()

continuous_play_timeout = 2


while True:
    cardid = reader.reader.readCard()
    try:
        if cardid is not None:
            if cardid == previous_id and (time.time() - previous_time) <= continuous_play_timeout:
                previous_time = time.time()
            elif cardid == 'x' and previous_id != 'x':
                previous_id = cardid
                subprocess.call([dir_path + '/playout_controls.sh -c=playerstop'], shell=True)
            elif cardid != previous_id: # or (time.time() - previous_time) >= same_id_delay:
                logger.info('Trigger Play Cardid={cardid}'.format(cardid=cardid))
                subprocess.call([dir_path + '/rfid_trigger_play.sh --cardid=' + cardid], shell=True)
                previous_id = cardid
                previous_time = time.time()

    except OSError as e:
        logger.error('Execution failed: {e}'.format(e=e))
