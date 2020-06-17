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
!help                               basic user functions
```

#### SHIP 
```
!ship affinity                  list of Affinities 
!ship affinity <affinity>       list of ships with specified weapon type 
!ship all                       list all ships
!ship aura                      list of Auras
!ship aura <aura>               list of ships with an aura
!ship detail <ship>             detailed ship info
!ship dmg                       list of Damage brackets
!ship dmg <dmg>                 list of ships with Damage inc type
!ship info <ship>               basic ship info
!ship rand <n>                  print random number of ships, default 10
!ship rarity                    list of rarities 
!ship rarity <rarity>           list ships in a rarity
!ship zen                       list of Zens
!ship zen <zen>                 list of ships with zen name
!ship help                     ship help
```

#### SOURCE
```
!source                         link to github repo
```

#### INVADER 
```
!invader affinity <affinity>    all invaders HP that match the affinity
!invader help                   invader help
!invader invader <name>         named invader HP stats for all affinities
!invader list                   invader names and turret count
```

## Command Todos

#### PRICE 
```
#!price weapon                   upgrade price of weapon levels (list)
#!price aura                     upgrade price of aura levels (list)
#!price zen                      upgrade price of zen levels (list)
#!price apex                     price of apex brackets (list)
```

#### APEX
```
#!apex help                      apex help
#!apex weapon                    list of weapon apex
#!apex aura                      list of aura apexs
#!apex zen                       list of zen apexs
#!apex ship <ship>               apexs the ship has
#!apex description <apex_name>   apex Description
#!apex find <apex_name>          list ships with <apex_name>, 
                                include cost, apex_type (weapon/aura/zen)
#!apex rank <apex_rank>          list of ships matching apex rank
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