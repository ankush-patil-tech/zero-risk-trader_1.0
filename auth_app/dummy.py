#!/usr/bin/env python3
# import pymysql
# import os
# import sys
#
# HOST = "zeroriskserver.mysql.database.azure.com"
# USER = os.environ.get("DB_USER", "ankush12345")
# PASSWORD = os.environ.get("DB_PASSWORD", "Patil@12345")
# DB = os.environ.get("DB_NAME", "user_platform_db")
# TIMEOUT = 7
#
# # candidate CA paths to test (order matters)
# CA_CANDIDATES = [
#     "/etc/ssl/certs/ca-certificates.crt",                                  # Debian aggregated bundle (recommended)
#     "/usr/local/share/ca-certificates/extra/BaltimoreCyberTrustRoot.crt",   # our added Baltimore cert
#     "/usr/local/share/ca-certificates/extra/DigiCertGlobalRootCA.crt.pem",  # alternate name
#     "certificate/DigiCertGlobalRootCA.crt.pem",                             # repo-local path
#     "certificate/BaltimoreCyberTrustRoot.crt",                              # repo-local alternate
# ]
#
# print("Running MySQL SSL diagnostic\n")
# print("Using DB host:", HOST)
# print("Using DB user:", USER)
# print("Using DB name:", DB)
# print("")
#
# for ca in CA_CANDIDATES:
#     print("=== Checking CA path:", ca)
#     exists = os.path.exists(ca)
#     print("Exists:", exists)
#     if not exists:
#         print(" -> file not found, skipping connection attempt\n")
#         continue
#
#     try:
#         print(" -> Attempting pymysql connect() with ssl ca:", ca)
#         conn = pymysql.connect(
#             host=HOST,
#             user=USER,
#             password=PASSWORD,
#             db=DB,
#             ssl={"ca": ca},
#             connect_timeout=TIMEOUT,
#         )
#         print(" -> SUCCESS: connected (conn.open == {})".format(conn.open))
#         conn.close()
#         print(" -> Closing connection and exiting with success.")
#         sys.exit(0)
#     except Exception as e:
#         print(" -> ERROR:", repr(e))
#         print(" -> continuing to next CA candidate\n")
#
# # Last resort: try system bundle with cert_reqs disabled (DEBUG ONLY)
# print("No CA candidate worked. Trying insecure connect (debug only).")
# try:
#     conn = pymysql.connect(
#         host=HOST,
#         user=USER,
#         password=PASSWORD,
#         db=DB,
#         ssl={"cert_reqs": False},
#         connect_timeout=TIMEOUT,
#     )
#     print(" -> INSECURE SUCCESS: connected (conn.open == {})".format(conn.open))
#     conn.close()
#     print(" -> Insecure connection succeeded. THIS CONFIRMS CA verification was the issue.")
#     sys.exit(2)
# except Exception as e:
#     print(" -> INSECURE ERROR:", repr(e))
#     print("\nSUMMARY: None of the CA paths worked and insecure connect also failed.")
#     print("Next steps: ensure the certificate file(s) are present inside the running container and")
#     print("that your Django 'OPTIONS': {'ssl': {'ca': '<path>'}} uses the same path.")
#     sys.exit(1)


import os

from django_extensions.settings import BASE_DIR

print("BASE_DIR =", BASE_DIR)
print(
    "SSL CA PATH =",
    os.path.join(BASE_DIR, 'certificate', 'DigiCertGlobalRootCA.crt.pem')
)
print(
    "CA file exists =",
    os.path.exists(os.path.join(BASE_DIR, 'certificate', 'DigiCertGlobalRootCA.crt.pem'))
)
