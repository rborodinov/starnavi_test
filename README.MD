## Instructions

Hope you have a docker installed, otherwise https://docs.docker.com/engine/install/ubuntu/

```commandline
sudo apt-get update
sudo apt-get install     ca-certificates     curl     gnupg     lsb-release
sudo mkdir -m 0755 -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o>
echo   "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/dock>
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > />
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin>
sudo docker run hello-world
```

To start project you can use make commands
```
make build
make up
```
Project might start and you can visit http://127.0.0.1:8000/ to check it.

Cascade delete don't work, I think this is because SQLite has supported foreign key constraint since version 3.6.19. /api/users/ DELETE cleans users, posts, likes mandatory.

## Automated bot 

To run bot using docker you can use make commands
```
make bot
make up_bot
```

Otherwise

Requirements file `bot_requirements.txt` maybe you'll want to use virtualenv.
```commandline
pip3 install bot_requirements.txt 
```

Bot file ` python3 automated_bot.py` 

Config file `bot_config.json`
Also you can start bot with args 
```commandline
python3 automated_bot.py --number_of_users 10  --max_posts_per_user 10 --max_likes_per_user 20
```
