# apex-bot

Information bot for the community Phoenix II discord server. 

## Installation 
`git clone git@github.com:Phoenix-II-Community/apex-bot.git`

Dependancies

```
python3 -m pip install -U discord.py
python3 -m pip install -U fuzzywuzzy
```

## Todos
 - Write the bot
 - Cron jobs 
    - Announce new Daily
    - Specialist
    - BHS Community 

## Bot Commands

### HELP
```
!help                               basic user functions
```

### INVADER 
```
!invader list                   invader names and turret count
!invader help                   invader help
!invader invader <name>         named invader HP stats for all affinities
!invader affinity <affinity>    all invaders HP that match the affinity
!invader terse <affinity>       (terse) all invaders HP that match the affinity
```

### PRICE 
```
!price weapon                   upgrade price of weapon levels (list)
!price aura                     upgrade price of aura levels (list)
!price zen                      upgrade price of zen levels (list)
!price apex                     price of apex brackets (list)
```

### SHIP 
```
!ship info <ship>               basic ship info
!ship detail <ship>             detailed ship info
!ship aura <aura>               list of shps with an aura
!ship zen <zen>                 list of ships with zen name
!ship affinity <affinity>       list of ships with specified weapon type 
!ship damage                    list of dmg brackets
!ship damage <dmg>              list of ships with dmg inc type
!ship random <n>                print random number of ships, default 10
!ship help                      ship help
```

### MISSION modulo
```
!mission help                   mission help
!mission -r --rotation          mission rotation
!mission -c --current           current mission
```

### APEX
```
!apex help                      apex help
!apex weapon                    list of weapon apex
!apex aura                      list of aura apexs
!apex zen                       list of zen apexs
!apex ship <ship>               apexs the ship has
!apex description <apex_name>   apex Description
!apex find <apex_name>          list ships with <apex_name>, 
                                include cost, apex_type (weapon/aura/zen)
!apex rank <apex_rank>          list of ships matching apex rank
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