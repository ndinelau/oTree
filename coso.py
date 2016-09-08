#!/usr/bin/env python
# -*- coding: utf-8 -*-

a="""
how much cooperate because communication
team spirit
after communication importance of your image
after communication importance maximum resources to everyone
after communication importance other members trust in you
after communication importance maximum resources to everyone not you
after communication How much trust do you have into other members
after communication how much do you like the other team members
after communication How good you understand solving problem great maximum resources
after communication How good others understand solving problem great maximum resources
which strategy would you follow and why
""".strip()

lines = a.splitlines()

for l in lines:
    l = l.lower().split()
    l = "_".join(l)
    print "q2_{} = models.PositiveIntegerField(min=1, max=5, widget=widgets.SliderInput(show_value=False))".format(l)

print ""
import pprint;pprint.pprint(["q2_"+"_".join(l.lower().split()) for l in lines])
