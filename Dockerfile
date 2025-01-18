# Use a Python base image
FROM python:3.8-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt to the container
COPY requirements.txt requirements.txt

# Install the dependencies
RUN pip3 install -r requirements.txt

# Copy all files into the container
COPY . .

# Set the environment variables (optional)
ENV TELEGRAM_API_ID=20836266
ENV TELEGRAM_API_HASH=bbdd206f92e1ca4bc4935b43dfd4a2a1
ENV TELEGRAM_BOT_TOKEN=8054568983:AAHWTggsclivHKu8JgZRIyY8Gfd1RhEnVfg
ENV INSTAGRAM_USERNAME=your_username
ENV INSTAGRAM_PASSWORD=your_password

# Command to run the bot
CMD ["python3", "bot.py"]
