# Pull python 3 image
FROM python:3

# Create a work dir
WORKDIR /usr/src/app


# copy requirements.txt into workdir created above
COPY requirements.txt ./
COPY .env ./


# Install all requirements
RUN python3 -m pip install --user --no-cache-dir -r requirements.txt


# Copy entire project into workdir
COPY . .


# Run our app without output
CMD ["python", "grantApprovalBot.py"]

# Exposing an internal port
EXPOSE 8080


# Step 4 set default commands
ENTRYPOINT [ "python3" ] # Default command

# These commands will be replaced if user provides any command by himself
CMD ["grantApprovalBot.py"]