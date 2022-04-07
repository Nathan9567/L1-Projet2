import fltk

fltk.cree_fenetre(800, 600)
while True:
    ev = fltk.donne_ev()
    if fltk.type_ev(ev) == 'Quitte':
        break
    if fltk.type_ev(ev) == 'Touche':
        print(fltk.touche(ev))
    fltk.mise_a_jour()