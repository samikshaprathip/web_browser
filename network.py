import socket
import ssl


def request(url):
    if url.startswith("https://"):
        scheme = "https"
        url = url[len("https://"):]
    elif url.startswith("http://"):
        scheme = "http"
        url = url[len("http://"):]
    else:
        scheme = "https"

    if "/" in url:
        host, path = url.split("/", 1)
        path = "/" + path
    else:
        host = url
        path = "/"

    port = 443 if scheme == "https" else 80

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if scheme == "https":
        ctx = ssl.create_default_context()
        s = ctx.wrap_socket(s, server_hostname=host)

    s.connect((host, port))

    request_data = f"GET {path} HTTP/1.0\r\nHost: {host}\r\n\r\n"
    s.send(request_data.encode("utf8"))

    response = s.makefile("r", encoding="utf8", newline="\r\n")
    data = response.read()

    s.close()

    headers, body = data.split("\r\n\r\n", 1)
    return body


if __name__ == "__main__":
    html = request("https://example.com")
    print(html)
