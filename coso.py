#!/usr/bin/env python
# -*- coding: utf-8 -*-

a="""
how much cooperate because communication
team spirit
afterc importance of your image
afterc importance maximum resources to everyone
afterc importance other members trust in you
afterc importance maximum resources to everyone not you
afterc How much trust do you have into other members
afterc how much do you like the other team members
afterc How good you understand solving problem max resources
afterc others understand solving problem great max resources
which strategy would you follow and why
""".strip()

lines = a.splitlines()

for l in lines:
    l = l.lower().split()
    l = "_".join(l)
    print "q2_{} = models.PositiveIntegerField(min=1, max=5, widget=widgets.SliderInput(show_value=False))".format(l)

print ""
lista = ["q2_"+"_".join(l.lower().split()) for l in lines]
import pprint;pprint.pprint(lista)
print map(len, lista)
