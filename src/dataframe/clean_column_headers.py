import unicodedata
import string

valid_filename_chars = "_ %s%s" % (string.ascii_letters, string.digits)
char_limit = 255


def clean_column_header(column_header, whitelist, replace):
    # lower case and trim
    column_header = column_header.strip().lower()
    column_header = column_header.replace('æ', 'ae').replace('ø', 'o').replace('å', 'aa')

    # replace spaces
    for r in replace:
        column_header = column_header.replace(r,'_')

    # keep only valid ascii chars
    cleaned_column_header = unicodedata.normalize('NFKD', column_header).encode('ASCII', 'ignore').decode()

    # keep only whitelisted chars
    cleaned_column_header = ''.join(c for c in cleaned_column_header if c in whitelist)
    return cleaned_column_header[:char_limit]

def clean_column_headers(_df, whitelist=valid_filename_chars, replace=' -'):
    _df.columns = [clean_column_header(c, whitelist, replace) for c in _df.columns]
    return _df