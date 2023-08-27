# apex-bot

Information bot for the community Phoenix II discord server. 

## Installation 
`git clone git@github.com:Phoenix-II-Community/apex-bot.git`

Dependancies

```
python3 -m pip install -U discord.py
python3 -m pip install -U rapidfuzz
```

## Bot Commands

#### HELP
```
/help                      basic user functions
```

#### Affinity 
```
/affinity                  list of Affinities 
/affinity <affinity>       list of ships with specified weapon type 
/affinity help
```

#### Ship
```
/ship all                  list all ships
/ship detail <ship>        detailed ship info
/ship info <ship>          basic ship info
/ship help
```

#### Aura 
```
/aura                      list of Auras
/aura <aura>               list of ships with an aura
/aura help
```

#### Damage
```
/dmg                       list of Damage brackets
/dmg <dmg>                 list of ships with Damage inc type
/dmg help
```
#### Random
```
/rand <n>                  print random number of ships, default 10
/rand help
```

#### Rarity
```
/rarity                    list of rarities 
/rarity <rarity>           list ships in a rarity
/rarity help
```

#### Zen
```
/zen                       list of Zens
/zen <zen>                 list of ships with zen name
/zen help
```

#### SOURCE
```
/source                    link to github repo
```

#### INVADER 
```
/invader affinity <affinity>    all invaders HP that match the affinity
/invader invader <name>         named invader HP stats for all affinities
/invader list                   invader names and turret count
/invader help                   invader help
```

#### PRICE 
```
/price weapon                   upgrade price of weapon levels (list)
/price aura                     upgrade price of aura levels (list)
/price zen                      upgrade price of zen levels (list)
/price apex                     price of apex brackets (list)
```

#### APEX
```
/apex help                      apex help
/apex weapon                    list of weapon apex
/apex aura                      list of aura apexs
/apex zen                       list of zen apexs
/apex ship <ship>               apexs the ship has
/apex description <apex_name>   apex Description
/apex find <apex_name>          list ships with <apex_name>, 
                                include cost, apex_type (weapon/aura/zen)
#/apex rank <apex_rank>          list of ships matching apex rank
```

## Mentions

Phoenix II is an arcade Shoot'Em Up developed by Firi Games in 2016. Firi Games is an independent game studio focused on developing premium games for iPhone, iPad and Apple TV. Firi Games is based in The Hague, Netherlands.

- My Phoenix II Community: "Bullet Hellspawn"
- Phoenix II Reddit: https://www.reddit.com/r/Phoenix_2/
- Phoenix II Discord Server: https://discord.gg/zCSNnCT
- Firi Games Website: https://www.firigames.com/
- Download Phoenix II: https://itunes.apple.com/au/app/phoenix-ii/id1134895689

### License
----

Open sourced under the [MIT license].