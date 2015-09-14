# ProtocolEditor

Early release of the OpenTrons Protocol Editor.  It's running Python and Flask under the hood.

You can run it yourself locally using the attached Dockerfile, or go to http://editor.mix.bio/.

## Local Setup

Install [Docker](http://docker.io).

Build the Dockerfile by `cd`ing into this repository and typing:

> `docker build -t protocol_editor .`

Run your new Docker container with:

> `docker run -p 5000:5000 protocol_editor`

In your browser, navigate to [http://localhost:5000](http://localhost:5000)
