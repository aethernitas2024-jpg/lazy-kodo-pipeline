# -*- coding: utf-8 -*-
"""Gathering professions in WoW Forever: route + what Forever changed.

Routes: zone facts from the taspas1po Classic guides (Zora, 2019), rewritten,
corrected where the data disagrees (Small Thorium at 245, not 225).
Forever: every item, skill level and effect below was read from the beta
client, build 1.60.1.70009 (ItemSparse / SkillLineAbility / SpellEffect), or
from Blizzard's own recaps (camp items, blueprints from dungeon bosses,
Bountiful Harvest). Nothing claims a drop location the client does not hold.

Bracket: (range, [item ids], [names], zones, tip, voice)
  zones = ('Horde: ...', 'Alliance: ...') or ('Contested: ...',)
New: (header, [(item id, name, quality, line)], voice)
"""

BUILD = 'beta client · build 1.60.1.70009'

PROF = {
 'mining': dict(
  title='MINING', music='warrior', icon=2770,
  art=['old_ironforge', 'eastern_kingdoms', 'excavation', 'kalimdor', 'eastern_kingdoms'],
  new_art=['zephras_isle', 'old_ironforge', 'excavation', 'kalimdor'],
  hook_icons=[2770, 2771, 2772, 3858, 10620],
  hook_voice='Mining, one to three hundred, in WoW Forever. The route, and everything Forever changed.',
  brackets=[
   ('1 – 65', [2770], ['Copper'],
    ('Horde: Durotar · Mulgore · The Barrens', 'Alliance: Dun Morogh · Elwynn · Darkshore'),
    'Train Journeyman at 50',
    'One to sixty five. Copper. Horde: Durotar, Mulgore and the Barrens. Alliance: Dun Morogh, Elwynn and Darkshore.'),
   ('65 – 125', [2771, 2775], ['Tin', 'Silver'],
    ('Horde: The Barrens · Hillsbrad', 'Alliance: Redridge · Duskwood'),
    'Silver spawns in place of Tin',
    'Sixty five to one twenty five. Tin. Silver is a rare swap for a tin vein, so always take it. Barrens and Hillsbrad, or Redridge and Duskwood.'),
   ('125 – 175', [2772, 2776], ['Iron', 'Gold'],
    ('Contested: Arathi · Alterac · Badlands', 'Stranglethorn caves'),
    'Train Expert at 125',
    'One twenty five to one seventy five. Iron, with gold as the rare spawn. Arathi, Alterac, the Badlands, and the caves of Stranglethorn.'),
   ('175 – 245', [3858, 7911], ['Mithril', 'Truesilver'],
    ('Contested: Badlands · Searing Gorge', 'Tanaris · The Hinterlands'),
    'Train Artisan at 200',
    'One seventy five to two forty five. Mithril, and truesilver if you are lucky. Badlands, Searing Gorge, Tanaris and the Hinterlands.'),
   ('245 – 300', [10620], ['Thorium'],
    ("Contested: Un'Goro · Winterspring", 'Silithus · Eastern Plaguelands'),
    'Small Thorium needs 245, not 225',
    "Two forty five to three hundred. Thorium. Un'Goro, Winterspring, Silithus and the Eastern Plaguelands."),
  ],
  new=[
   ('NEW RARE ORES', [
     (249391, 'Pyrite', 2, 'Green ore · item level 25'),
     (249425, 'Bauxite', 2, 'Green ore · item level 45'),
     (249426, 'Pitchblende', 2, 'Green ore · item level 60')],
    'New in Forever: three green ores. Pyrite, Bauxite and Pitchblende. And the Legacy talent Bountiful Harvest finds you up to double the scarce materials.'),
   ('CAMP ITEMS', [
     (279960, 'Lodestone', 1, 'Skill 20 · melee attack power buff'),
     (279948, 'Rock Garden', 1, 'Skill 140 · grows Copper, Tin & Iron nodes'),
     (279952, 'Molten Foundry', 1, 'Skill 300 · needed for Heavy Thorium')],
    'Mining now builds camp items. Lodestone at twenty. A Rock Garden at one forty that grows copper, tin and iron at your camp. And the Molten Foundry at three hundred. Their blueprints drop in dungeons.'),
   ('ENDGAME ORE', [
     (248815, 'Heavy Thorium Ore', 1, 'From a brand new Heavy Thorium vein'),
     (251291, 'Heavy Thorium Bar', 2, 'Smelt at 300 · needs a Molten Foundry'),
     (249726, 'Azerothium Bar', 2, 'Skill 275 · 2 Pitchblende + 1 Coal')],
    'At the top: a brand new Heavy Thorium vein. Its bar needs the Molten Foundry. And Azerothium, smelted from Pitchblende at two seventy five.'),
   ('FREE HEAD START', [
     (247840, 'Mining for Dummies', 1, 'First-zone quest reward · free skill'),
     (277115, "Apprentice's Mining Pack", 1, 'Profession bags get their own slot')],
    'Start smart. Pick Mining for Dummies from your first quest for free skill points. And profession bags now get their own slot.'),
  ],
  closer='Keep every Pitchblende. Azerothium is made from it.',
  next='Herbalism next',
 ),

 'herbalism': dict(
  title='HERBALISM', music='druid', icon=2447,
  art=['kalimdor', 'excavation', 'zephras_isle', 'ruins_lordaeron', 'kalimdor', 'excavation'],
  new_art=['zephras_isle', 'excavation', 'kalimdor', 'zephras_isle', 'excavation'],
  hook_icons=[2447, 785, 3356, 8838, 13463],
  hook_voice='Herbalism, one to three hundred, in WoW Forever. The route, and everything Forever changed.',
  brackets=[
   ('1 – 70', [2447, 765, 2449], ['Peacebloom', 'Silverleaf', 'Earthroot'],
    ('Horde: Durotar · Mulgore · Tirisfal', 'Alliance: Elwynn · Dun Morogh · Teldrassil'),
    'Train Journeyman at 50',
    'One to seventy. Peacebloom, Silverleaf, then Earthroot. Any starting zone works. Train Journeyman at fifty.'),
   ('70 – 115', [785, 2450, 2453], ['Mageroyal', 'Briarthorn', 'Bruiseweed'],
    ('Horde: The Barrens · Silverpine', 'Alliance: Westfall · Darkshore'),
    '',
    'Seventy to one fifteen. Mageroyal, Briarthorn and Bruiseweed. The Barrens and Silverpine, or Westfall and Darkshore.'),
   ('115 – 160', [3355, 3356], ['Wild Steelbloom', 'Kingsblood'],
    ('Horde: Stonetalon · Hillsbrad', 'Alliance: Wetlands · Ashenvale'),
    'Train Expert at 125',
    'One fifteen to one sixty. Wild Steelbloom and Kingsblood. Stonetalon and Hillsbrad, or the Wetlands and Ashenvale.'),
   ('160 – 205', [3357, 3818, 3358], ['Liferoot', 'Fadeleaf', "Khadgar's Whisker"],
    ('Contested: Swamp of Sorrows', 'Stranglethorn'),
    'Train Artisan at 200',
    "One sixty to two oh five. Liferoot, Fadeleaf and Khadgar's Whisker. Loop the whole Swamp of Sorrows."),
   ('205 – 270', [4625, 8838, 8846], ['Firebloom', 'Sungrass', 'Gromsblood'],
    ('Contested: Tanaris · Searing Gorge', 'Hinterlands · Blasted Lands · Desolace'),
    '',
    'Two oh five to two seventy. Firebloom, Sungrass and Gromsblood. Tanaris, Searing Gorge, the Hinterlands, the Blasted Lands and Desolace.'),
   ('270 – 300', [13463, 13466], ['Dreamfoil', 'Plaguebloom'],
    ("Contested: Un'Goro · Azshara", 'Eastern & Western Plaguelands'),
    '',
    "Two seventy to three hundred. Dreamfoil in Un'Goro and Azshara, then Plaguebloom in the Plaguelands."),
  ],
  new=[
   ('NEW RARE HERBS', [
     (249399, 'Frilled Lichen', 2, 'Green herb · item level 25'),
     (249424, 'Rosecap', 2, 'Green herb · item level 45'),
     (249274, 'Stranglevine', 2, 'Green herb · item level 60')],
    'New in Forever: three green herbs. Frilled Lichen, Rosecap and Stranglevine. And the Legacy talent Bountiful Harvest finds you up to double the scarce materials.'),
   ('HERB FARMING', [
     (279962, 'Incense Candle', 1, 'Skill 20 · Intellect buff for your camp'),
     (279964, 'Greenhouse', 1, 'Skill 140 · grows herbs from seeds'),
     (279947, 'Seed Hybridizer', 1, 'Skill 300 · combines seeds into rarer ones')],
    'Herbalism gets farming. Incense Candle at twenty. A Greenhouse at one forty grows real herb nodes from seeds. The Seed Hybridizer at three hundred turns seeds into rarer seeds.'),
   ('HERB SEEDS', [
     (268415, 'Commonplace Herb Seeds', 2, 'Grow them in a Greenhouse'),
     (268416, 'Uncommon Herb Seeds', 2, 'or combine them at a camp'),
     (268417, 'Unusual Herb Seeds', 2, ''),
     (268418, 'Scarce Herb Seeds', 2, '')],
    'Four tiers of seeds. Commonplace, Uncommon, Unusual and Scarce.'),
   ('HYJAL HERBS', [
     (248822, 'Death Lotus', 2, 'Enchant Lotus Claw: chance on any Hyjal herb'),
     (248823, 'Marefoil', 1, 'New level 60 herb'),
     (248821, 'Demonsage', 1, 'New level 60 herb')],
    'At the top: Death Lotus, Marefoil and Demonsage. A new glove enchant, Lotus Claw, gives a chance at Death Lotus from any herb in Hyjal.'),
   ('FREE HEAD START', [
     (247841, 'Wild Harvest', 1, 'First-zone quest reward · free skill'),
     (277113, "Apprentice's Herb Pouch", 1, 'Profession bags get their own slot')],
    'Start smart. Pick Wild Harvest from your first quest for free skill points. And Tauren: Cultivation now copies a nearby herb, once an hour.'),
  ],
  closer='Plant your seeds early. The Greenhouse does the farming.',
  next='Skinning next',
 ),

 'fishing': dict(
  title='FISHING', music='hunter', icon=6256, verb='Fish in',
  art=['zephras_isle', 'kalimdor', 'eastern_kingdoms', 'excavation'],
  new_art=['zephras_isle', 'excavation', 'kalimdor', 'eastern_kingdoms', 'zephras_isle'],
  hook_icons=[6291, 6289, 8365, 13759, 13422],
  hook_voice='Fishing, one to three hundred, in WoW Forever. The route, and everything Forever changed.',
  brackets=[
   ('1 – 75', [6291, 6303], ['Brilliant Smallfish', 'Slitherskin Mackerel'],
    ('Horde: Durotar · Mulgore · Tirisfal', 'Alliance: Elwynn · Dun Morogh · Teldrassil'),
    'Train Journeyman at 50',
    'One to seventy five. Fish any water in your starting zone. A Shiny Bauble lure helps.'),
   ('75 – 150', [6289, 6308], ['Longjaw Mud Snapper', 'Bristle Whisker Catfish'],
    ('Horde: The Barrens · Stonetalon · Ashenvale', 'Alliance: Ashenvale · Duskwood · Wetlands'),
    'Expert book: Old Man Heming, Booty Bay',
    'Seventy five to one fifty. Mud Snapper and Catfish. At one twenty five, buy the Expert book from Old Man Heming in Booty Bay.'),
   ('150 – 225', [8365, 6362], ['Mithril Head Trout', 'Rockscale Cod'],
    ('Contested: Stranglethorn · Desolace', 'Swamp of Sorrows · Thousand Needles'),
    'Artisan: Nat Pagle quest at 225',
    'One fifty to two twenty five. Mithril Head Trout and Rockscale Cod. At two twenty five, Nat Pagle in Dustwallow gives the Artisan quest.'),
   ('225 – 300', [4603, 13759, 13422], ['Spotted Yellowtail', 'Nightfin Snapper', 'Stonescale Eel'],
    ('Contested: Tanaris · Feralas · Azshara', "Un'Goro · Felwood · Hinterlands"),
    '',
    'Two twenty five to three hundred. Yellowtail, Nightfin Snapper and Stonescale Eel.'),
  ],
  # pool maps only where spawn data exists: bracket index -> {faction: (zone, pool names, label)}
  routes={
   1: {'Horde': ('The Barrens', ['School of Deviate Fish'], 'Deviate Fish schools in the oases'),
       'Alliance': ('Ashenvale', ['Sagefish School'], 'Sagefish schools')},
   2: {'Horde': ('Stranglethorn', ['School of Tastyfish'], 'Tastyfish schools'),
       'Alliance': ('Stranglethorn', ['School of Tastyfish'], 'Tastyfish schools')},
  },
  new=[
   ('FISHING CAMP ITEMS', [
     (279967, 'Fish Bowl', 1, 'Skill 20 · +8% all stats for your camp'),
     (279965, 'Fishing Rack', 1, 'Skill 140 · uncommon fish for 1 hour'),
     (279966, 'Fishing Hut', 1, 'Skill 300 · rare fish for 1 hour')],
    'Fishing now builds camp items. A Fish Bowl at twenty gives eight percent to all stats. The Fishing Rack at one forty catches uncommon fish for an hour, and the Fishing Hut at three hundred, rare fish. Their blueprints drop in dungeons.'),
   ('LEGACY TALENTS', [
     (6533, 'Luremaster', 1, 'With a lure on: 50% chance of an extra fish'),
     (6256, 'Master Forager', 1, '+25 Fishing skill, account-wide')],
    'Two Legacy talents. Luremaster: with a lure on, fifty percent chance of an extra fish. Master Forager: plus twenty five fishing.'),
   ('NEW FISHING GEAR', [
     (259846, 'Wide-Brimmed Fishing Hat', 2, 'Use: +25 Fishing for 10 min'),
     (259890, 'Deep-Sea Waders', 2, 'Use: walk on water'),
     (273636, "Chef's Knife", 1, 'Skill 275 · prepares unique fish')],
    "New gear. A Wide-Brimmed Fishing Hat with a built-in lure. Deep-Sea Waders that let you walk on water. And a Chef's Knife at two seventy five for unique fish."),
   ('FISHING EXTRAVAGANZA', [
     (274026, 'Extravagant Extravaganza Coin', 3, "Winners trade it with Jang"),
     (276272, "Master Angler's Fishing Hat", 3, 'Contest reward'),
     (276275, 'Bitter Baitling', 3, 'Companion pet')],
    "The Stranglethorn Fishing Extravaganza is back, reworked. Winners get a coin for prizes like a hat and a pet, and wear the Master Angler title for the week."),
   ('NEW FISH & RECIPES', [
     (251524, 'Whimsyfin', 1, 'New fish · random effect when eaten'),
     (251525, 'Savory Whimsyfin Delight', 1, 'New cooking recipe'),
     (274971, 'Briny Seafood Stew', 1, 'New cooking recipe')],
    'New fish too. Whimsyfin, with a random effect, and new seafood recipes for your cooking.'),
  ],
  closer='Always fish with a lure. Luremaster doubles down on it.',
  next='Which profession next?',
 ),

 # Route: Warcraft Tavern's Classic 1-300 (taspas1po's cooking page gets Artisan wrong: it is the
 # "Clamlette Surprise" quest in Classic, not a trainer). Forever items read in the beta client.
 'cooking': dict(
  title='COOKING', music='shaman', icon=2681, verb='Cook',
  art=['kalimdor', 'excavation', 'eastern_kingdoms', 'zephras_isle'],
  new_art=['zephras_isle', 'excavation', 'kalimdor', 'eastern_kingdoms', 'zephras_isle'],
  hook_icons=[2681, 6890, 3665, 17222, 12218],
  hook_voice='Cooking, one to three hundred, in WoW Forever. The recipes, and everything Forever changed.',
  brackets=[
   ('1 – 75', [2681, 2679, 6890], ['Roasted Boar Meat', 'Charred Wolf Meat', 'Smoked Bear Meat'],
    ('Horde: Roasted Boar Meat · Smoked Bear Meat', 'Alliance: Charred Wolf Meat · Smoked Bear Meat'),
    'Train Journeyman at 50',
    'One to seventy five. Boar or wolf meat from the trainer, then Smoked Bear Meat from a vendor.'),
   ('75 – 150', [5478, 2683, 3665], ['Dig Rat Stew', 'Crab Cake', 'Tasty Omelet'],
    ('Horde: Dig Rat Stew · Curiously Tasty Omelet', 'Alliance: Crab Cake · Wolf Kabob · Curiously Tasty Omelet'),
    'Expert Cookbook: Wulan (H) · Shandrina (A)',
    'Seventy five to one fifty. At one twenty five, buy the Expert Cookbook: Wulan in Desolace for Horde, Shandrina in Ashenvale for Alliance.'),
   ('150 – 225', [12210, 3729, 17222], ['Roast Raptor', 'Turtle Bisque', 'Spider Sausage'],
    ('Horde: Tasty Omelet · Roast Raptor · Spider Sausage', 'Alliance: Tasty Omelet · Turtle Bisque · Spider Sausage'),
    'Artisan: "Clamlette Surprise", Gadgetzan',
    'One fifty to two twenty five. At two twenty five, Dirge in Gadgetzan gives the Artisan quest, Clamlette Surprise.'),
   ('225 – 300', [12218, 18045, 20452], ['Monster Omelet', 'Tender Wolf Steak', 'Desert Dumplings'],
    ('Both factions: Monster Omelet · Tender Wolf Steak', 'Smoked Desert Dumplings'),
    '',
    'Two twenty five to three hundred. Finish with the Silithus dumplings quest.'),
  ],
  new=[
   ('FOOD NOW GIVES XP', [
     (250079, 'Well Fed = +5% XP', 1, 'From kills, for 15 minutes'),
     (250080, 'Breakfast Omelette', 1, 'New · skill 75 · +3 Stamina'),
     (250071, 'Steaming Stag Steak', 1, 'New · skill 260 · +20 Strength')],
    'The big one: eating cooked food now gives five percent more experience from kills, for fifteen minutes. And Classic dishes were reworked to give one clean stat.'),
   ('SMOOTHIES & TEAS', [
     (249871, 'Venomous Smoothie', 1, 'Skill 5 · Spirit, up to +20'),
     (249876, 'Wicked Smoothie', 1, 'Skill 240 · +20 Spirit'),
     (249865, 'Peace Tea', 1, 'Water + 2 Peacebloom · healing'),
     (249870, "Sage's Tea", 1, 'Skill 260 · +44 healing')],
    "Twelve new drinks. Six smoothies for Spirit, and six teas for healing, from Peace Tea with two Peacebloom up to Sage's Tea."),
   ('BIGGER CAMPFIRES', [
     (279981, 'Basic Campfire', 1, 'Skill 1 · room for 3 camp items'),
     (279961, 'Journeyman Campfire', 1, 'Skill 90 · 5 camp items'),
     (279974, 'Expert Campfire', 1, 'Skill 200 · 10 camp items'),
     (279982, 'Iron Oven', 1, 'Skill 300 · most advanced recipes')],
    'Cooks build the camp. The Basic Campfire holds three camp items, the Journeyman five, the Expert ten. And the Iron Oven at three hundred unlocks the most advanced recipes.'),
   ('LEGACY TALENTS', [
     (280317, 'Master Chef', 1, '30% chance of an extra dish'),
     (18045, 'Gourmand', 1, 'Food buffs last twice as long')],
    'Two Legacy talents. Master Chef: thirty percent chance of an extra dish. Gourmand: food buffs last twice as long.'),
   ('NEW DISHES', [
     (274971, 'Briny Seafood Stew', 1, '+14 spell damage'),
     (286152, 'Plated Armorfish', 1, '+150 armor'),
     (267341, 'Sweetpaw Jam', 1, '+15% speed in Hyjal')],
    'And new dishes: Briny Seafood Stew for spell damage, Plated Armorfish for armor, and Sweetpaw Jam for speed in Hyjal.'),
  ],
  closer='Eat before you quest. Five percent XP adds up.',
  next='Which profession next?',
 ),

 'skinning': dict(
  title='SKINNING', music='hunter', icon=2318,
  art=['kalimdor', 'excavation', 'eastern_kingdoms', 'ruins_lordaeron', 'kalimdor', 'excavation'],
  new_art=['zephras_isle', 'excavation', 'kalimdor', 'eastern_kingdoms'],
  hook_icons=[2934, 2318, 2319, 4234, 8170],
  hook_voice='Skinning, one to three hundred, in WoW Forever. The route, and everything Forever changed.',
  brackets=[
   ('1 – 50', [2934, 2318], ['Ruined Scraps', 'Light Leather'],
    ('Horde: Durotar · Mulgore · Tirisfal', 'Alliance: Elwynn · Dun Morogh · Teldrassil'),
    'Keep a Skinning Knife in your bags',
    'One to fifty. Skin every beast in your starting zone. Keep a skinning knife in your bags, and train Journeyman at fifty.'),
   ('50 – 100', [2318], ['Light Leather'],
    ('Horde: The Barrens · Silverpine', 'Alliance: Westfall · Darkshore · Loch Modan'),
    'Train Journeyman at 50',
    'Fifty to one hundred. Light leather. The Barrens and Silverpine, or Westfall, Darkshore and Loch Modan.'),
   ('100 – 150', [2319], ['Medium Leather'],
    ('Horde: South Barrens · Thousand Needles', 'Alliance: Duskwood · Wetlands · Ashenvale'),
    'Train Expert at 125',
    'One hundred to one fifty. Medium leather. The southern Barrens and Thousand Needles, or Duskwood, the Wetlands and Ashenvale.'),
   ('150 – 200', [4234], ['Heavy Leather'],
    ('Contested: Arathi · Desolace', 'Stranglethorn'),
    'Train Artisan at 200',
    'One fifty to two hundred. Heavy leather. Arathi, Desolace and Stranglethorn.'),
   ('200 – 250', [4304], ['Thick Leather'],
    ('Contested: Feralas · Tanaris', 'Stranglethorn'),
    '',
    'Two hundred to two fifty. Thick leather. Feralas, Tanaris, and more Stranglethorn.'),
   ('250 – 300', [8170], ['Rugged Leather'],
    ("Contested: Un'Goro · Felwood", 'Winterspring · Silithus'),
    '',
    "Two fifty to three hundred. Rugged leather. Un'Goro, Felwood, Winterspring and Silithus."),
  ],
  new=[
   ('NEW RARE LEATHER', [
     (249427, 'Pristine Leather', 2, 'Item level 25 · used by 126 recipes'),
     (249428, 'Pristine Hide', 2, 'Green hide · item level 45'),
     (249429, 'Pristine Scale', 2, 'Green scale · item level 60')],
    'New in Forever: Pristine Leather, Pristine Hide and Pristine Scale. Pristine Leather alone shows up in a hundred and twenty six recipes. And Bountiful Harvest finds you up to double the scarce materials.'),
   ('CAMP ITEMS', [
     (279979, 'Camp Chair', 1, 'Skill 20 · critical strike buff'),
     (279969, 'Field Guide', 1, 'Skill 140 · grants Track Beasts'),
     (279938, "Trapper's Workbench", 1, 'Skill 300 · comes with a trap')],
    "Skinning now builds camp items. A Camp Chair at twenty. A Field Guide at one forty that gives Track Beasts. And the Trapper's Workbench at three hundred. Their blueprints drop in dungeons."),
   ('ENDGAME LEATHER', [
     (248824, 'Fel Hide', 1, 'New level 60 hide'),
     (248825, 'Fel Leather', 1, 'Used by 52 Leatherworking recipes')],
    'At the top: Fel Hide and Fel Leather, used by fifty two Leatherworking recipes. And a new glove enchant, Advanced Skinning, adds ten skill.'),
   ('FREE HEAD START', [
     (247846, 'Pelt Collecting for Beginners', 1, 'First-zone quest reward · free skill'),
     (277114, "Apprentice's Skinning Satchel", 1, 'Profession bags get their own slot')],
    'Start smart. Pick Pelt Collecting for Beginners from your first quest for free skill points. And profession bags now get their own slot.'),
  ],
  closer='Never walk past a beast. Pristine Leather is in 126 recipes.',
  next='Which profession next?',
 ),
}
