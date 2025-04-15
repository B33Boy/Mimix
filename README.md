# Mimix

For optimal performance, ensure that Ollama is running on the host system (e.g., ollama serve). Running Ollama inside a container on Windows or Mac may result in performance degradation.

## Dependencies
- Docker & Docker Compose
- Ollama 
- Python 3.8+

## Configuration Management
**(Optional)** Before running the bot, configure the following parameters in `bot/config.py` to your liking:
```python
# Key phrase used to trigger the bot
PREFIX = 'hey '  

# Timeout duration for requests (in seconds)
TIMEOUT = 120.0 

# Maximum response size (in characters)
MAX_RESP_SIZE = 2000
```

## Environment Variables
The Ollama-related environment variables are configured in the `docker-compose.yml` file

`docker-compose.yml`
```
...
environment:
    - OLLAMA_PORT=11434
    - OLLAMA_MODEL=gemma3:4b
    - OLLAMA_HOST=host.docker.internal
...
```

**For proper functioning of the bot, you must create an `.env` folder at the root of the project**

`.env`
```
DISCORD_TOKEN=YOUR_TOKEN
VALID_USERS=DISCORD_USERNAME,
``` 

## Running the Bot
To start the bot, use the following command:

```sh
docker-compose up
```