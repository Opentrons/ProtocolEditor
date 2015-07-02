# Protocol Editor

A web application for editing and modifying OpenTrons JSON protocol files.

### Capabilities

* Load and graphically display existing valid protocol files for the OT.One robot
* Edit names, values, and attributes of existing items in the protocol file
* Add new Deck, Head, Ingredient, and Instruction items
* Add new Motions to existing Instructions
* Save changes to your local computer

### To Run

The `Protocol Editor` is still in early development stages. To run it locally, you will first need to download the `Flask` web development environment. Using the `pip` package installer, type 

```
sudo pip install flask
```

into your command line to download and install.

With `Flask` successfully downloaded, navigate into the folder containing this repository on your local system and type 

```
python editor_main.py
```

Once the app is successfully running, navigate in your browser to `127.0.0.1:5000` to begin testing.
