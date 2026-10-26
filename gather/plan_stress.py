GOLDC = (255, 210, 90, 255)
GOLDG = (200, 140, 40, 255)
HG = (150, 40, 30, 255)
BLUE = (120, 190, 255, 255)
BLUEG = (30, 80, 150, 255)

STRESS = [
    (card('hook', 'WOW FOREVER  ·  THE STRESS TEST', 'HOW DID IT GO?', BLUE, BLUEG, [],
          [('a rough first hour', RED, 46), ('then surprisingly smooth', SICK, 46),
           ('the good, the bad, and November 4', BONE, 40)], size=110),
     'stress', 'Last night, anyone could play WoW Forever for free in the stress test. So how did it go? '
               'A rough first hour, then surprisingly smooth. Here is the good, the bad, and what it means for launch.', 9.0),
    (card('start', 'THE FIRST HOUR', 'NO REALMS', RED, HG, [],
          [('"realm types not available"', BONE, 44), ('error after error at 7 PM Paris', BONE, 40),
           ('some waited almost an hour', AMBER, 42), ('to get into the game', AMBER, 42)], size=120),
     'stress', 'The start was rough. At seven PM Paris time, many players got realm types not available, error after error. '
               'Some waited almost an hour before getting in.', 9.0),
    (card('smooth', 'AFTER THAT', 'NO QUEUES', SICK, (40, 110, 40, 255), [],
          [('around 100 FPS, no stutter', BONE, 42), ('packed starting zones', BONE, 42),
           ('Camp Narache, last night (my screenshot)', GREY, 34), ('about 8 hours of play, until 3 AM Paris', AMBER, 38)], size=120),
     'stress', 'But after that? No queues, high frame rates, and packed starting zones. This is Camp Narache last night. '
               'The test ran for about eight hours, until three AM Paris time.', 9.5),
    (card('broke', 'WHAT BROKE', 'NOT PERFECT', RED, HG, [],
          [('chain disconnects for some players', BONE, 40), ('NPCs not loading, slow quest turn-ins', BONE, 38),
           ('mobs vanishing mid-fight', BONE, 40), ('"jumping shadows" leaving Durotar', BONE, 38),
           ('devs crashed services on purpose', AMBER, 40)], size=120),
     'stress', 'It was not perfect. Some players got chain disconnects, N P Cs not loading, and very slow quest turn-ins. '
               'Mobs vanished mid-fight, shadows jumped around, and the devs even crashed some background services on purpose.', 10.5),
    (card('layers', 'THE BIG DEBATE', 'LAYERING', SHADOW, (90, 40, 150, 255), [],
          [('some were alone in Elwynn Forest', BONE, 40), ('others stuck in a laggy Stormwind', BONE, 40),
           ('"too empty" and "too crowded"', AMBER, 42), ('at the same time', AMBER, 42),
           ('a PvP realm overloaded by a streamer guild?', GREY, 34)], size=120),
     'stress', 'The big debate: layering. Some players were alone in Elwynn Forest, others stuck in a laggy Stormwind. '
               'Too empty and too crowded, at the same time. And players say a streamer guild overloaded an Alliance PvP realm.', 10.5),
    (card('end', 'THE LAST MINUTES', 'EVERYTHING VANISHED', GOLDC, GOLDG, [],
          [('around 3 AM, every NPC disappeared', BONE, 40), ('players danced in Goldshire', BONE, 42),
           ('and dueled until the end', BONE, 42), ('stress test characters are deleted', GREY, 36)], size=104),
     'stress', 'The ending was very World of Warcraft: around three AM, every N P C disappeared, '
               'and players just danced in Goldshire and dueled until the servers closed.', 8.5),
    (card('next', 'WHAT’S NEXT', 'NOVEMBER 4', GOLDC, GOLDG, [],
          [('beta extended: until Friday Oct 23', SICK, 42), ('10 AM PDT  ·  7 PM Paris', BONE, 40),
           ('name reservation: Oct 27 - Nov 3', AMBER, 40), ('launch: November 4', AMBER, 44)], size=120),
     'vault', 'What is next? The beta is extended until Friday, October twenty third, seven PM Paris. '
              'Name reservation runs from October twenty seventh to November third, and launch is November fourth.', 9.5),
    (card('outro', 'YOUR VERDICT', 'READY FOR LAUNCH?', BLUE, BLUEG, [],
          [('did you get in? smooth or broken?', AMBER, 42), ('follow for everything Forever', SICK, 42)], size=104),
     'emeralddream', 'So, is Forever ready for launch? Did you get in, and was it smooth or broken for you? Tell me, and follow for everything Forever.', 7.0),
]
