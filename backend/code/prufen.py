import gesprach_kontroller, ki_kontroller, os

# gesprach_name = "juliet"

# gesprach : list[gesprach_kontroller.BaseMessage] = gesprach_kontroller.gesprach_laden(gesprach_name)
# print(gesprach)
# input()

# if not gesprach:

#     personlichkeit = "Du bist glücklich aber normal"

#     gesprach : list[gesprach_kontroller.BaseMessage] = gesprach_kontroller.gesprach_erstellen(gesprach_name, personlichkeit=personlichkeit)

# while True:
#     os.system("clear")
#     gesprach_kontroller.gesprach_zeigen(gesprach)

#     benutzer_nachricht = input("Deine nachricht: ")

#     gesprach = ki_kontroller.nachricht_an_gesprach_senden(benutzer_nachricht, gesprach)
#     gesprach_kontroller.gesprach_speichern(gesprach_name,gesprach)

print(gesprach_kontroller.alle_gesprache_erhalten())