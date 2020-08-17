# SupeRo_bot
Bot for my Twitch channel.

## About
The bot lacks almost all functionality at this point and was mostly made for 
shitposting. Feel free to take a look, but don't expect too much. I don't plan 
to actively develop it.

## Dependencies
As of the latest update, this code relies on my 
[GetterCore library](https://github.com/sym-okami/GetterCore). It should be 
cloned to the same top-level directory as SupeRo_bot.

## bot_auth.json format
The superobot_wrapper expects a file named bot_auth.json to be placed in the 
same directory. The contents should be structured as such:

{\
    "user": "{twitchUserName}",\
    "oauth": "oauth:{oauthKey}",\
    "channels": ["#{channel1}", "#{channel2}"]\
}

where anything within the curly braces should be replaced with the appropriate 
values.

## Links
[My Twitch](https://www.twitch.tv/symulacra)
[SupeRo_Bot's Twitch](https://www.twitch.tv/supero_bot)