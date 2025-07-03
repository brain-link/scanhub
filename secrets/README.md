# Generation of certificate and private key

```
openssl req -x509 -nodes -days 365 \
  -newkey rsa:2048 \
  -keyout ../secrets/privatekey.pem \
  -out ../secrets/certificate.pem \
  -subj "/CN=localhost" \
  -addext "subjectAltName=DNS:localhost"

```