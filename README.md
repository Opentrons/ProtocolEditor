# ProtocolEditor

Early release of the OpenTrons Protocol Editor.

You can run it yourself locally using the attached Dockerfile, or go to http://editor.mix.bio/.

## Local Setup

1. Install [Docker](http://docker.io).

2. Build the Dockerfile by `cd`ing into this repository and typing:

> `docker build -t protocol_editor .`

3. Run your new Docker container with:

> `docker run -p 5000:5000 protocol_editor`

4. In your browser, navigate to http://localhost:5000
