from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from binascii import unhexlify as uhx
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from os.path import exists
from random import randint
from zlib import compress
from re import search, match
from json import load


def doEncrypt(key, buf):
    return AES.new(key, AES.MODE_ECB).encrypt(
        buf + (b"\x00" * (0x10 - (len(buf) % 0x10)))
    )


def encrypt(
    in_bytes, public_key, vm_file=None, *, drmkey="c9674744cfce53f3a3ee187a15869795"
):

    pubKey = RSA.importKey(open(public_key).read())
    aesKey = randint(0, 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF).to_bytes(0x10, "big")
    buf = None
    inp = b""

    if vm_file:
        with open(vm_file, "rb") as f:
            tmp = f.read()
            inp += b"\x13\x37\xB0\x0B"
            inp += len(tmp).to_bytes(4, "little")
            inp += tmp

    if vm_file:
        inp += doEncrypt(uhx(drmkey[0:32]), in_bytes)
    else:
        inp += in_bytes

    compressed = compress(inp, 9)

    return (
        b"TINFOIL\xFE"
        + PKCS1_OAEP.new(pubKey, hashAlgo=SHA256, label=b"").encrypt(aesKey)
        + len(compressed).to_bytes(8, "little")
        + doEncrypt(aesKey, compressed)
    )

def generate_shop(minidb):
    shop_files = []
    for i in minidb:
        if "mirrors" in i:
            for j in i["mirrors"].values():  # unlisted
                for k in j:
                    shop_files.append(
                        {
                            "url": "gdrive:/{}#{}".format(k["id"], k["filename"]),
                            "size": int(k["size"]),
                        }
                    )
    return shop_files


def get_creds(credentials, token, scopes=["https://www.googleapis.com/auth/drive"]):
    creds = None
    if exists(token):
        with open(token, "r") as t:
            creds = Credentials(**load(t))
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds = InstalledAppFlow.from_client_secrets_file(
                credentials, scopes
            ).run_local_server(port=0)
        with open(token, "w") as t:
            json_creds = creds.to_json()
            # https://github.com/googleapis/google-auth-library-python/issues/666
            # Avoids issues when loading the token again. 
            del json_creds["expiry"]
            t.write(json_creds)
    return creds


def generate_entry(item):
    return {"id": item["id"], "filename": item["name"], "size": int(item["size"])}


def find_title_id(name):
    tid = search(r"0100[0-9A-Fa-f]{12}", name)
    if tid is not None:
        return tid.group(0).upper()
    return


def valid_file_id(file_id):
    return match(r"[-\w]{25,}$",file_id)


def lsf(service, parent):
    files = []
    resp = {"nextPageToken": None}
    while "nextPageToken" in resp:
        resp = (
            service.files()
            .list(
                q='trashed = false and "{}" in parents and not mimeType = "application/vnd.google-apps.folder"'.format(
                    parent
                ),
                fields="files(id,name,size,fileExtension),nextPageToken",
                pageSize=1000,
                supportsAllDrives=True,
                includeItemsFromAllDrives=True,
                pageToken=resp["nextPageToken"],
            )
            .execute()
        )
        files += resp["files"]
    return files
