# pull official base image
FROM python:3.11.14

# set work directory
ENV HOME /usr/src/app
WORKDIR $HOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y netcat-traditional libpq-dev

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt $HOME/requirements.txt
RUN pip install -r $HOME/requirements.txt

# copy entrypoint-prod.sh
COPY ./entrypoint.sh $HOME

# strip windows lines endings for entrypoint file
RUN sed 's/\r//g' /usr/src/app/entrypoint.sh && chmod +x /usr/src/app/entrypoint.sh

# copy project
COPY . $HOME

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
