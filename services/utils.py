import re
import uuid
from werkzeug.utils import secure_filename

def is_strong_password(password):
    return (
        len(password) >= 8 and
        re.search(r"[a-z]", password) and
        re.search(r"[A-Z]", password) and
        re.search(r"\d", password) and
        re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
    )
#jede Datei einen einzigartigen Namen bekommt, um Überschreibungen zu verhindern.
#zb ausweis.pdf" → "9d2a7e8f1b3449bc92854b230d7fddf2_ausweis.pdf
def generate_secure_filename(original_name):
    return f"{uuid.uuid4().hex}_{secure_filename(original_name)}"
# damit filnames nicht durch manipulierte Dateinnamen Schaden erstellt