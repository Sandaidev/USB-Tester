import random
import shutil
import string
import colorama
import termcolor
import time
import hashlib
import os
import secrets
from decimal import Decimal

# Whaaa des couleurs!
colorama.init()

TEST_FILENAME = "USBTESTFILE.rnd"
FILE_CHARNUMBER = 1000000000
STR_SEPARATOR = "====================="


def sanitizedInput(input_type, printed_str):
    """
    Vérifie que l'entrée soit du bon type
    """

    while True:
        try:
            # On essaye de convertir l'entrée au bon type
            user_input = input_type(input(printed_str))
            break

        except:
            # L'entrée n'est pas du bon type, du coup, on recommence
            termcolor.cprint(
                "Cette entrée n'est pas du type " + str(input_type) + "!", "yellow"
            )

    return user_input


def ret_md5(filename):
    """
    Voir https://stackoverflow.com/a/3431838
    """

    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


termcolor.cprint("USB Tester", "cyan")
termcolor.cprint("Par Erwan", "green")
USB_KEY_LOCATION = input("Destination de la clé USB (Style Windows) : ")

# On va générer un fichier d'environ 1 Go
# Contenant des charactères aléatoires

# On construit le dictionnaire de génération
str_charset = string.ascii_letters + string.digits + string.punctuation
test_file_write = open(TEST_FILENAME, "w")

print(STR_SEPARATOR + "- GENERATION -" + STR_SEPARATOR)

termcolor.cprint("[1/4] Génération de 1 Go...", "cyan")

# On commence à générer avec 1 Gigaoctet
# NOTE: 1 charactère = 1 octet

for x in range((FILE_CHARNUMBER // 100000) // 2):
    test_file_write.write(secrets.token_hex(100000))

test_file_write.close()

# Calcul de la taille du fichier généré en MB (utilisé pour calculer la vitesse de transfert plus tard)
FLOAT_TEST_FILESIZE_MB = round(Decimal(os.path.getsize(TEST_FILENAME) / 1024 / 1024), 3)


termcolor.cprint("[2/4] Préparation de la comparaison des deux fichiers...", "cyan")
START_FILE_MD5_DIGEST = ret_md5(TEST_FILENAME)

# Le fichier test est à présent généré! OUAIIIS!
# On doit le déplacer vers la destination et mesurer le temps pris

termcolor.cprint("[3/4] Déplacement du fichier source...", "cyan")
start_time = time.time()
shutil.move(TEST_FILENAME, USB_KEY_LOCATION + "\\" + TEST_FILENAME)
time_took = round(Decimal(time.time() - start_time), 2)

termcolor.cprint("[4/4] Comparaison des deux fichiers...", "cyan")
END_FILE_MD5_DIGEST = ret_md5(USB_KEY_LOCATION + "\\" + TEST_FILENAME)

# Suppression du fichier de destination
os.remove(USB_KEY_LOCATION + "\\" + TEST_FILENAME)

print(STR_SEPARATOR + "- INTEGRITE -" + STR_SEPARATOR)

termcolor.cprint("MD5 Entrée : " + str(START_FILE_MD5_DIGEST), "magenta")
termcolor.cprint("MD5 Sortie : " + str(END_FILE_MD5_DIGEST), "magenta")

if START_FILE_MD5_DIGEST == END_FILE_MD5_DIGEST:
    termcolor.cprint("Intégrité du fichier garantie!", "green")

else:
    termcolor.cprint("Inégrité du fichier non gerantie!", "red")


average_transfer_speed_mbps = round(FLOAT_TEST_FILESIZE_MB / time_took, 3)

print(STR_SEPARATOR + "- STATS -" + STR_SEPARATOR)
print(
    "Vitesse de transfert moyenne (Taille div. par temps): "
    + termcolor.colored(str(average_transfer_speed_mbps) + " MB/s", "magenta")
)

print("Temps pris : " + termcolor.colored(str(time_took) + " secondes", "magenta"))
print(STR_SEPARATOR * 2)
input("Appuyez sur [ENTREE] pour quitter...")
