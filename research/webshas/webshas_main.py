# -*- coding: utf-8 -*-
# import sys
import sys
import os
import django
import json

from sources.local_settings import *

import numpy as np

from bert_serving.client import BertClient
bc = BertClient()


sys.path.insert(0, SEFARIA_PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = "sefaria.settings"

django.setup()

from sefaria.model import *







# Write a test set
# Clean up the texts (bold tags, punctuation, stop words, etc...)
# Try only using the words inbetween bold tags
# Deal with having to combine texts from parent dicts in the webShas file with text is too small



with open("../../../webshas2.json", "r") as read_file:
    data = json.load(read_file)


overall_dict = {}


def iterate_through_dict(the_dict):
    if 'refs' in the_dict:
        if len(the_dict['refs']) > 0:
            overall_dict[the_dict['text']] = []
            overall_dict[the_dict['text']].append(the_dict['refs'])
            print
            print
            print the_dict['refs']
            webshas_text = the_dict['text']
            webshas_text_encoded = bc.encode([webshas_text])[0]
            # for seg_ref in Ref('Nedarim 35b-36a').all_segment_refs():
            #     print seg_ref.normal(), TextChunk(seg_ref).text


            for each_seg_ref in the_dict['refs']:
                print each_seg_ref
                segment_refs = Ref(each_seg_ref).all_segment_refs()
                segment_refs_text = {seg_ref.normal(): TextChunk(seg_ref).text for seg_ref in segment_refs}

                sefaria_text = list(segment_refs_text.values())
                sefaria_text_encoded = bc.encode(sefaria_text)


                sefaria_ref = ""
                # compute normalized dot product as score
                score = np.sum(webshas_text_encoded * sefaria_text_encoded, axis=1) / np.linalg.norm(sefaria_text_encoded, axis=1)
                topk_idx = np.argsort(score)[::-1][0]

                for ref, text in segment_refs_text.iteritems():  # for name, age in dictionary.iteritems():  (for Python 2.x)
                    if text == sefaria_text[topk_idx]:
                        sefaria_ref = ref

                print "\tWebshas Text:"
                print "\t\t", webshas_text
                print "\tOur Guess:"
                print "\t\t", sefaria_ref
                print "\t\t", sefaria_text[topk_idx]

                print
                print



    if 'subtopics' in the_dict:
        for sub_topic in the_dict['subtopics']:
            iterate_through_dict(sub_topic)


iterate_through_dict(data[0])
print len(overall_dict)


