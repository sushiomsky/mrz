import sys
import random
from datetime import datetime
from mrz.checker.td1 import TD1CodeChecker
from mrz.checker.td2 import TD2CodeChecker
from mrz.checker.td3 import TD3CodeChecker
from mrz.generator.td1 import TD1CodeGenerator
from mrz.generator.td2 import TD2CodeGenerator
from mrz.generator.td3 import TD3CodeGenerator

def check_mrz_code(mrz_code):
    document_type = mrz_code.split("\n")[0][:2]

    try:
        if document_type == "ID":  # Personalausweis
            checker = TD1CodeChecker(mrz_code)
        elif document_type == "I<" or document_type == "IV":  # Vorläufiger Personalausweis
            checker = TD2CodeChecker(mrz_code)
        elif document_type == "P<":  # Reisepass
            checker = TD3CodeChecker(mrz_code)
        else:
            print("Unbekannter Dokumenttyp")
            return False

        if not checker.check():
            return False

        expiry_date_str = checker.expiry_date
        expiry_date = datetime.strptime(expiry_date_str, "%y%m%d").date()
        today = datetime.now().date()

        if expiry_date < today:
            print("Der Ausweis ist abgelaufen.")
            return False
        else:
            return True

    except Exception as e:
        print("Fehler bei der Überprüfung des MRZ-Codes:", e)
        return False
def generate_random_mrz(document_type):
    country = "D<<"
    name = "MUSTERMANN<<MAX<<<<<<<<<<<<<<<<<"
    document_number = "".join([random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(9)])
    nationality = "D<<"
    birth_date = "900101"
    sex = "M"
    expiry_date = "990101"

    if document_type == "ID":
        generator = TD1CodeGenerator("ID", country, name, document_number, nationality, birth_date, sex, expiry_date)
    elif document_type == "I<" or document_type == "IV":
        generator = TD2CodeGenerator("I<", country, name, document_number, nationality, birth_date, sex, expiry_date)
    elif document_type == "P<":
        generator = TD3CodeGenerator("P<", country, name, document_number, nationality, birth_date, sex, expiry_date)
    else:
        raise ValueError("Ungültiger Dokumenttyp")

    return str(generator)

if __name__ == "__main__":
    option = sys.argv[1] if len(sys.argv) > 1 else ""
    if not option:
        print("Bitte geben Sie eine Option ein: --check oder --generate.")
        sys.exit(1)

    if option == "--check":
        mrz_code = sys.argv[2] if len(sys.argv) > 2 else ""
        if not mrz_code:
            print("Bitte geben Sie den MRZ-Code ein.")
            sys.exit(1)
        is_valid = check_mrz_code(mrz_code)
        print("Gültiger MRZ-Code" if is_valid else "Ungültiger MRZ-Code")
    elif option == "--generate":
        document_type = sys.argv[2] if len(sys.argv) > 2 else ""
        if not document_type:
            print("Bitte geben Sie den Dokumenttyp ein: ID, I<, IV oder P<.")
            sys.exit(1)
        random_mrz = generate_random_mrz(document_type)
        print("Zufälliger gültiger MRZ-String:\n" + random_mrz)
    else:
        print("Ungültige Option. Verwenden Sie --check oder --generate.")

