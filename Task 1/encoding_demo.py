"""
encoding_demo.py
Task 1: Encoding Formats & Secure Protocols
Foundation of Computer Science | ST4015CMD
Data Systems and Security Assignment

Demonstrates the four encoding schemes discussed in the report:
  - ASCII / UTF-8 character encoding
  - Base64  (HTTP Basic Auth, MIME email attachments, OAuth JWT tokens)
  - URL / Percent encoding (REST APIs, OAuth redirect URIs, XSS prevention)
  - Hexadecimal (SHA-256 hash, HMAC-SHA256 signature)

Also simulates the full TLS email transmission flow described in
Section 1.8 of the report (Figure 5).

No external libraries required — uses Python standard library only.
Compatible with Python 3.8+.
"""

import base64
import urllib.parse
import hashlib
import hmac
import binascii

DIVIDER  = "=" * 65
DIVIDER2 = "-" * 65


def section(number: str, title: str) -> None:
    print(f"\n{DIVIDER}")
    print(f"  {number}. {title}")
    print(DIVIDER)


def subsection(title: str) -> None:
    print(f"\n  {DIVIDER2}")
    print(f"  {title}")
    print(f"  {DIVIDER2}")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1 — ASCII / UTF-8 ENCODING
# Report reference: Section 1.1 (Overview of Common Encoding Formats)
# "ASCII is an outdated encoding system that uses 7-bit binary numbers..."
# ─────────────────────────────────────────────────────────────────────────────
section("1", "ASCII / UTF-8 CHARACTER ENCODING")

text = "Hello, World!"
ascii_bytes   = text.encode("ascii")
utf8_bytes    = text.encode("utf-8")
binary_repr   = " ".join(format(b, "08b") for b in ascii_bytes[:5])

print(f"\n  Input text     : {text}")
print(f"  ASCII bytes    : {list(ascii_bytes[:6])} ...")
print(f"  UTF-8 bytes    : {list(utf8_bytes[:6])} ...")
print(f"  Binary (first 5 chars): {binary_repr} ...")
print(f"\n  Note: ASCII uses 7-bit encoding (128 characters).")
print(f"  UTF-8 is backward-compatible and handles all Unicode characters.")

# Non-ASCII character — shows ASCII limitation
subsection("ASCII Limitation with non-English characters")
emoji = "Héllo"
try:
    emoji.encode("ascii")
except UnicodeEncodeError as e:
    print(f"  Input          : {emoji!r}")
    print(f"  ASCII encode   : FAILED → {e}")
    print(f"  UTF-8 encode   : {list(emoji.encode('utf-8'))}")
    print(f"  → This is why Base64 is needed for binary/non-ASCII data.")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2 — BASE64 ENCODING / DECODING
# Report reference: Sections 1.1, 1.2, 1.4
# "Base64 encoding is a method used to encode binary data into human-readable
#  ASCII characters that can be transmitted through text-based protocols..."
# ─────────────────────────────────────────────────────────────────────────────
section("2", "BASE64 ENCODING")

# 2a. HTTP Basic Authentication
subsection("2a. HTTP Basic Auth  (used in web logins)")
credentials   = "alice:SecurePass123"
encoded_auth  = base64.b64encode(credentials.encode()).decode()
decoded_back  = base64.b64decode(encoded_auth).decode()

print(f"  Original       : {credentials}")
print(f"  Base64 encoded : {encoded_auth}")
print(f"  HTTP Header    : Authorization: Basic {encoded_auth}")
print(f"  Decoded back   : {decoded_back}")
print(f"  Size increase  : {len(credentials)} chars → {len(encoded_auth)} chars "
      f"(+{round((len(encoded_auth)/len(credentials)-1)*100)}%)")
print(f"\n  ⚠  Note: Base64 is NOT encryption — it is easily reversible.")
print(f"     Always transmit over TLS/HTTPS, never plain HTTP.")

# 2b. MIME Email Attachment
subsection("2b. MIME Email Attachment  (used in SMTP)")
file_content  = b"Report.pdf binary content sample \x89\x50\x4e\x47"
mime_encoded  = base64.b64encode(file_content).decode()
mime_decoded  = base64.b64decode(mime_encoded)

print(f"  Raw binary     : {file_content[:20]} ...")
print(f"  Base64 encoded : {mime_encoded}")
print(f"  MIME header    : Content-Transfer-Encoding: base64")
print(f"  Decoded match  : {mime_decoded == file_content}")
print(f"\n  → SMTP is text-based. Base64 converts binary files (PDFs,")
print(f"    images) into ASCII so they survive text-only transmission.")

# 2c. OAuth / JWT Token (Base64URL)
subsection("2c. OAuth JWT Token  (Base64URL variant)")
jwt_header    = '{"alg":"HS256","typ":"JWT"}'
jwt_payload   = '{"sub":"1234567890","name":"Alice","iat":1516239022}'
b64_header    = base64.urlsafe_b64encode(jwt_header.encode()).decode().rstrip("=")
b64_payload   = base64.urlsafe_b64encode(jwt_payload.encode()).decode().rstrip("=")
fake_token    = f"{b64_header}.{b64_payload}.<signature>"

print(f"  JWT Header     : {jwt_header}")
print(f"  JWT Payload    : {jwt_payload}")
print(f"  Base64URL Hdr  : {b64_header}")
print(f"  Base64URL Pay  : {b64_payload}")
print(f"  Full JWT       : {fake_token[:80]}...")
print(f"\n  → OAuth uses Base64URL (replaces + with - and / with _)")
print(f"    to make tokens safe inside URLs without percent-encoding.")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3 — URL (PERCENT) ENCODING
# Report reference: Sections 1.1, 1.2, 1.5
# "URL encoding replaces URL-special characters with a percent sign..."
# ─────────────────────────────────────────────────────────────────────────────
section("3", "URL (PERCENT) ENCODING")

# 3a. REST API query parameter
subsection("3a. REST API Query Parameter")
query         = "data systems & security 2024"
encoded_query = urllib.parse.quote(query)
decoded_query = urllib.parse.unquote(encoded_query)

print(f"  Original       : {query}")
print(f"  URL Encoded    : {encoded_query}")
print(f"  Full URL       : https://api.example.com/search?q={encoded_query}")
print(f"  Decoded back   : {decoded_query}")

# 3b. OAuth redirect URI
subsection("3b. OAuth Redirect URI")
redirect_uri  = "https://myapp.com/callback?status=success&code=abc123"
encoded_uri   = urllib.parse.quote(redirect_uri, safe="")

print(f"  Original URI   : {redirect_uri}")
print(f"  URL Encoded    : {encoded_uri}")
print(f"\n  → OAuth embeds the redirect URL as a parameter inside another URL.")
print(f"    URL encoding ensures the inner URL is not confused with the outer one.")

# 3c. XSS prevention
subsection("3c. XSS Prevention via URL Encoding")
xss_input     = '<script>alert("XSS Attack!")</script>'
safe_output   = urllib.parse.quote(xss_input)

print(f"  Malicious input: {xss_input}")
print(f"  URL Encoded    : {safe_output}")
print(f"\n  → Encoding converts < > \" into %3C %3E %22, preventing the browser")
print(f"    from interpreting the input as executable HTML/JavaScript code.")
print(f"  ⚠  Note: URL encoding alone is not sufficient — always combine with")
print(f"    server-side input validation and output sanitization.")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4 — HEXADECIMAL ENCODING
# Report reference: Section 1.1
# "Hexadecimal encoding can be seen in cryptographic hash values,
#  debugging, and binary data analysis."
# ─────────────────────────────────────────────────────────────────────────────
section("4", "HEXADECIMAL ENCODING")

# 4a. SHA-256 hash
subsection("4a. SHA-256 Hash  (password storage / data integrity)")
password      = "MySecurePassword!"
sha256_hex    = hashlib.sha256(password.encode()).hexdigest()
sha256_bin    = hashlib.sha256(password.encode()).digest()

print(f"  Input          : {password!r}")
print(f"  SHA-256 (hex)  : {sha256_hex}")
print(f"  Hex length     : {len(sha256_hex)} chars = {len(sha256_hex)//2} bytes = 256 bits")
print(f"  Raw binary     : {sha256_bin[:8].hex()} ... ({len(sha256_bin)} bytes total)")
print(f"\n  → Each pair of hex digits (e.g. 'a3') represents one byte of binary.")
print(f"    Hexadecimal makes binary data human-readable for debugging and logging.")

# 4b. HMAC-SHA256 (OAuth1 / AWS Signature V4)
subsection("4b. HMAC-SHA256 Signature  (OAuth1 / API request signing)")
secret_key    = b"supersecretkey_ST4015CMD"
message       = b"GET&https%3A%2F%2Fapi.example.com%2Fdata&timestamp%3D1706000000"
hmac_hex      = hmac.new(secret_key, message, hashlib.sha256).hexdigest()
hmac_b64      = base64.b64encode(
                    hmac.new(secret_key, message, hashlib.sha256).digest()
                ).decode()

print(f"  Secret Key     : {secret_key.decode()}")
print(f"  Message        : {message[:55].decode()}...")
print(f"  HMAC-SHA256    : {hmac_hex}")
print(f"  HMAC (Base64)  : {hmac_b64}")
print(f"\n  → AWS Signature V4 and OAuth1 use HMAC-SHA256 to sign API requests.")
print(f"    The hex or Base64 signature proves the request has not been tampered with.")

# 4c. Hexadecimal in debugging / binary analysis
subsection("4c. Hex dump  (binary data analysis / debugging)")
sample_data   = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"   # PNG file header
hex_dump      = " ".join(f"{b:02x}" for b in sample_data)
printable     = "".join(chr(b) if 32 <= b < 127 else "." for b in sample_data)

print(f"  Binary data    : {sample_data}")
print(f"  Hex dump       : {hex_dump}")
print(f"  Printable repr : {printable}")
print(f"\n  → Security analysts use hex dumps to inspect files for malware,")
print(f"    verify file signatures (magic bytes), and reverse-engineer binaries.")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5 — SIMULATED TLS EMAIL FLOW
# Report reference: Section 1.8, Figure 5
# "The Workflow of Encoding and Encryption in Email Transmission"
# Flow: Sender → Base64 Encode → TLS Encrypt → SMTP Server
#       → TLS Decrypt → Base64 Decode → Recipient
# ─────────────────────────────────────────────────────────────────────────────
section("5", "SIMULATED TLS EMAIL FLOW  (Section 1.8 / Figure 5)")

print(f"\n  Simulating: Sender → Base64 Encode → TLS Encrypt →")
print(f"              SMTP Server → TLS Decrypt → Base64 Decode → Recipient\n")

email_body = (
    "Dear Bob,\n\n"
    "Please find the attached security report for ST4015CMD.\n\n"
    "Kind regards,\nAlice"
)
attachment  = b"\x89PNG binary attachment content \x00\x01\x02\x03"

print(f"  {'─'*60}")
print(f"  STEP 1 │ Sender composes email")
print(f"  {'─'*60}")
print(f"  Body preview   : {email_body[:60]}...")
print(f"  Attachment     : {len(attachment)} bytes of binary data")

print(f"\n  {'─'*60}")
print(f"  STEP 2 │ Base64 Encode  (MIME encoding)")
print(f"  {'─'*60}")
b64_body       = base64.b64encode(email_body.encode()).decode()
b64_attachment = base64.b64encode(attachment).decode()
print(f"  Encoded body   : {b64_body[:60]}...")
print(f"  Encoded attach : {b64_attachment}")
print(f"  → Both are now plain ASCII, compatible with SMTP text protocol.")

print(f"\n  {'─'*60}")
print(f"  STEP 3 │ TLS Encrypt  (transport layer security)")
print(f"  {'─'*60}")
# Simulate TLS by XOR-scrambling bytes (illustrative only — not real TLS)
key_byte       = 0x5A
tls_sim_body   = bytes(b ^ key_byte for b in b64_body.encode())
print(f"  Plaintext B64  : {b64_body[:30]}...")
print(f"  TLS ciphertext : {tls_sim_body[:20].hex()} ... [binary, unreadable]")
print(f"  → TLS encrypts the entire packet. Even if intercepted, the data")
print(f"    cannot be read without the session key.")

print(f"\n  {'─'*60}")
print(f"  STEP 4 │ SMTP Server routes the encrypted packet")
print(f"  {'─'*60}")
print(f"  Server sees    : [TLS ciphertext] — cannot read content.")
print(f"  Action         : Routes packet to recipient mail server.")

print(f"\n  {'─'*60}")
print(f"  STEP 5 │ TLS Decrypt  (at recipient MTA)")
print(f"  {'─'*60}")
decrypted_b64  = bytes(b ^ key_byte for b in tls_sim_body).decode()
print(f"  Decrypted B64  : {decrypted_b64[:60]}...")
match = decrypted_b64 == b64_body
print(f"  Matches orig   : {match}  ✓" if match else f"  Matches orig   : {match}  ✗")

print(f"\n  {'─'*60}")
print(f"  STEP 6 │ Base64 Decode  (recipient reads email)")
print(f"  {'─'*60}")
final_body     = base64.b64decode(decrypted_b64).decode()
print(f"  Decoded body   : {final_body[:80]}...")
match2 = final_body == email_body
print(f"  Matches orig   : {match2}  ✓" if match2 else f"  Matches orig   : {match2}  ✗")

print(f"\n  {'─'*60}")
print(f"  SUMMARY")
print(f"  {'─'*60}")
print(f"  Sender → Base64 Encode → TLS Encrypt → SMTP Server")
print(f"         → TLS Decrypt   → Base64 Decode → Recipient ✓")
print(f"\n  Key insight: Base64 provides COMPATIBILITY (binary → text).")
print(f"               TLS provides CONFIDENTIALITY (encryption).")
print(f"               They serve different, complementary roles.")

print(f"\n{DIVIDER}")
print(f"  Demo complete — all encoding formats demonstrated.")
print(f"{DIVIDER}\n")
