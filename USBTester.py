import random
import shutil
import string
import colorama
import termcolor
import time
import hashlib
import os
import secrets
import traceback
import sys
from decimal import Decimal

# Whaaa des couleurs!
colorama.init()

SCRIPT_VERSION = "1.1"

TEST_FILENAME = "USBTESTFILE.rnd"
FILE_CHARNUMBER = 1000000000
STR_SEPARATOR = "====================="


def ret_md5(filename):
    """
    Voir https://stackoverflow.com/a/3431838
    """

    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def main():
    print(
        termcolor.colored("USB Tester", "cyan")
        + " -- Par "
        + termcolor.colored("Erwan", "cyan")
    )
    print("--> Version " + termcolor.colored(SCRIPT_VERSION, "cyan"))

    print(STR_SEPARATOR + "- DESTINATION -" + STR_SEPARATOR)
    USB_KEY_LOCATION = input("[INPUT] Destination de la clé USB (Style Windows) : ")

    # On va générer un fichier d'environ 1 Go
    # Contenant des charactères aléatoires

    # On construit le dictionnaire de génération
    test_file_write = open(TEST_FILENAME, "w")

    print(STR_SEPARATOR + "- GENERATION -" + STR_SEPARATOR)

    termcolor.cprint("[1/5] Génération de 1 Go...", "cyan")

    # On commence à générer avec 1 Gigaoctet
    # NOTE: 1 charactère = 1 octet

    for x in range((FILE_CHARNUMBER // 100000) // 2):
        test_file_write.write(secrets.token_hex(100000))

    test_file_write.close()

    # Calcul de la taille du fichier généré en MB (utilisé pour calculer la vitesse de transfert plus tard)
    FLOAT_TEST_FILESIZE_MB = round(
        Decimal(os.path.getsize(TEST_FILENAME) / 1024 / 1024), 3
    )

    termcolor.cprint("[2/5] génération de la somme de contrôle MD5 (entrée)...", "cyan")
    START_FILE_MD5_DIGEST = ret_md5(TEST_FILENAME)

    # Le fichier test est à présent généré! OUAIIIS!
    # On doit le déplacer vers la destination et mesurer le temps pris

    termcolor.cprint("[3/5] Déplacement du fichier (Source -> Destination)... ", "cyan")
    start_time_write = time.time()
    shutil.move(TEST_FILENAME, USB_KEY_LOCATION + "\\" + TEST_FILENAME)
    time_took_write = round(Decimal(time.time() - start_time_write), 2)

    termcolor.cprint("[4/5] Génération de la somme de contrôle MD5 (sortie)...", "cyan")
    END_FILE_MD5_DIGEST = ret_md5(USB_KEY_LOCATION + "\\" + TEST_FILENAME)

    # On mesure la vitesse de lecture
    # On déplace le fichier depuis la destination vers la source
    termcolor.cprint("[5/5] Déplacement du fichier (Destination -> Source)...", "cyan")
    start_time_read = time.time()
    shutil.move(USB_KEY_LOCATION + "\\" + TEST_FILENAME, TEST_FILENAME)
    time_took_read = round(Decimal(time.time() - start_time_read), 2)

    # Suppression du fichier de destination
    os.remove(TEST_FILENAME)

    print(STR_SEPARATOR + "- INTEGRITE -" + STR_SEPARATOR)

    termcolor.cprint("MD5 Entrée : " + str(START_FILE_MD5_DIGEST), "magenta")
    termcolor.cprint("MD5 Sortie : " + str(END_FILE_MD5_DIGEST), "magenta")

    if START_FILE_MD5_DIGEST == END_FILE_MD5_DIGEST:
        termcolor.cprint("Somme de contrôle OK!", "green")

    else:
        termcolor.cprint("Différence de somme de contrôle [Fichier corrompu]!", "red")

    average_write_speed_mbps = round(FLOAT_TEST_FILESIZE_MB / time_took_write, 3)
    average_read_speed_mbps = round(FLOAT_TEST_FILESIZE_MB / time_took_read, 3)

    print(STR_SEPARATOR + "- STATS -" + STR_SEPARATOR)
    # STATS ECRITURE (SOURCE --> DESTINATION)
    print("[Ecriture]")
    print(
        "Vitesse d'écriture moyenne (Source --> Destination) : "
        + termcolor.colored(str(average_write_speed_mbps) + " MB/s", "magenta")
    )

    print(
        "Temps d'écriture : "
        + termcolor.colored(str(time_took_write) + " secondes", "magenta")
    )
    # STATS LECTURE (DESTINATION --> SOURCE)
    print("[Lecture]")
    print(
        "Vitesse de lecture moyenne (Destination --> Source) : "
        + termcolor.colored(str(average_read_speed_mbps) + " MB/s", "magenta")
    )
    print(
        "Temps de lecture : "
        + termcolor.colored(str(time_took_read) + " secondes", "magenta")
    )
    print(STR_SEPARATOR * 2)
    input("Appuyez sur [ENTREE] pour quitter...")
    sys.exit()


try:
    main()

except Exception as script_crash:
    # Merde
    termcolor.cprint(STR_SEPARATOR + "- CRASH! -" + STR_SEPARATOR, "grey", "on_red")
    print("...Merde!")
    print("BASE EXCEPTION : " + str(script_crash))
    termcolor.cprint("==- TRACEBACK -==", "red")
    traceback.print_exc()
    input("Appuyez sur [Entrée] pour quitter...")
