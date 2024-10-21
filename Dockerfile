FROM python:3.12.3-alpine3.19

# Setting workdir to app
WORKDIR /app

# Prevents django from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents django from buffering the output on terminal
ENV PYTHONUNBUFFERED 1

# Installing netcat
RUN apk update && apk add --no-cache netcat-openbsd

RUN pip install --upgrade pip

# copying only requirements.txt as we the mounting the current dir to the container
COPY requirements $app

RUN pip install -r prod.txt

COPY entrypoint.sh .
# The below two command are used to covert the file in LF format
RUN dos2unix entrypoint.sh
# RUN sed -i 's/\r$//g' entrypoint.sh
RUN chmod +x entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]