FROM ubuntu:15.04
MAINTAINER OpenTrons

# Update the system
RUN apt-get update -qq

# Install Python.
RUN apt-get install -y python-pip

ENV APP_HOME /var/www
ENV PORT 5000
ENV WEB_ENV production

# Create a working directory for our app
RUN echo Creating app directory in $APP_HOME
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# Add just the library requirements and install them.  This step is cached
# unless the requirements have changed.
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Take the files from our Git repo and add them to $APP_HOME
# Never edit these files from within containers; make another build.
ADD . $APP_HOME

EXPOSE $PORT

ENTRYPOINT main.py
