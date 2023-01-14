import random
import copy
#name0 attack1 health2 deathrattle3 divine_shield4 reborn5 tribe6 taunt7 attackorder8(lisätään combatissa) damage_taken_during_combat(sama)

#TODO järjestä deathrattlet, luo loppuun
#yo-ho-ogre
#ghoul

def combat(fminions, eminions, deathrattles, waitingroom, waiters, minionList):

    for i in range(len(fminions)):
        fminions[i].append(i)#lisätään hyökkäysvuorot
    for i in range(len(eminions)):
        eminions[i].append(i)

    deathrattles = []
    waiters = []
    fblanks = []
    eblanks = []
    start_of_combat(fminions, eminions, deathrattles, waiters, fblanks, eblanks, minionList)

    a = 0
    p = 0
    while len(eminions) != 0 and len(fminions) != 0:
        targets = []
        for i in range(len(eminions)):
            if eminions[i][7] == 1:
                targets.append([i, eminions[i]])
        if len(targets) == 0:
            for i in range(len(eminions)):
                targets.append([i, eminions[i]])
        target = targets[random.randint(0, (len(targets))-1)] #[sijainti 0-6][minion]
        if target[1][0] == "ritualist":
            ritualist(eminions, target[0]) #TODO ritualisti buffi pitää joskus siirtää muualle
        #if target[1][0] == "yo-ho-ogre":
        #    yo_ho_ogre()
        attacker = []#[sijainti 0-6][minion]
        for i in range(len(fminions)):
            if fminions[i][8] == a:
                attacker = [i, fminions[i]]
        deathrattles = []
        waiters = []
        hits(attacker, target, fminions, eminions, deathrattles, waitingroom, waiters, minionList)

        p += 1
        if p == 2:
            a += 1 #a on hyökkäysvuoro
            p = 0

        tempf = list(fminions) #flipataan listat
        tempe = list(eminions)
        fminions = list(tempe)
        eminions = list(tempf)

    if p == 1:
        if len(fminions) > 0:
            return "l"
        elif len(eminions) > 0:
            return "w"
        else:
            return "d"
    else:
        if len(fminions) > 0:
            return "w"
        elif len(eminions) > 0:
            return "l"
        else:
            return "d"


def start_of_combat(fminions, eminions, deathrattles, waiters, fblanks, eblanks, minionList):
    murk_eye_buff(fminions, eminions)
    captain_buff(fminions)
    captain_buff(eminions)
    warleader_buff(fminions)
    warleader_buff(eminions)
    whelps(fminions, eminions, deathrattles, waiters, fblanks, eblanks)

    waitingroom = True
    while len(deathrattles) != 0:
        fblanks = []
        eblanks = []
        deathrattling(deathrattles, fminions, eminions, waitingroom, waiters, fblanks, eblanks, minionList)
        deathrattles = copy.deepcopy(waiters)
        waiters = []
        waitingroom = False



def hits(attacker, defender, fminions, eminions, deathrattles, waitingroom, waiters, minionList):#attacker = [position, minion]

    fblanks = []
    eblanks = []
    fminions[attacker[0]][8] += len(fminions) #päiviteään hyökkäysjärjestys
    if attacker[1][0] == "guardian":
        fminions[attacker[0]][1] *= 2
    take_damage(attacker, defender[1][1], fminions, True, deathrattles, waitingroom, waiters, fblanks, eblanks, fminions, eminions, defender, eminions)
    take_damage(defender, attacker[1][1], eminions, False, deathrattles, waitingroom, waiters, fblanks, eblanks, fminions, eminions, attacker, fminions)
    waitingroom = True
    while len(deathrattles) != 0:
        fblanks = []
        eblanks = []
        deathrattling(deathrattles, fminions, eminions, waitingroom, waiters, fblanks, eblanks, minionList)
        deathrattles = copy.deepcopy(waiters)
        waiters = []
        waitingroom = False


def take_damage(minion, damage, team, friendly, deathrattles, waitingroom, waiters, fblanks, eblanks, fminions, eminions, other, other_team):#team idea on vähän riski mut koitetaan
    if minion[1][4] == "1":
        team[minion[0]][4] = 0
    else:
        team[minion[0]][2] -= damage
        team[minion[0]][9] += damage
        if team[minion[0]][2] <= 0:
            if other[1][6] == "dragon": #buffataan togwagglet
                togwaggle(other_team)
            death(minion[1], minion[0], team, friendly, deathrattles, waitingroom, waiters, fblanks, eblanks, fminions, eminions)


def death(minion, position, team, friendly, deathrattles, waitingroom, waiters, fblanks, eblanks, fminions, eminions):
    team.pop(position)
    if minion[6] == "beast":
        hyena(team)#buffataan hyenat
    if minion[6] == "murlock":
        murk_eye_debuff(fminions, eminions)
    if minion[0] == "warleader":
        warleader_debuff(team)
    if minion[0] == "captain":
        captain_debuff(team)
    if friendly:
        fblanks.append(position)
    else:
        eblanks.append(position)
        for i in range(len(team)):# päivitetään attackorder kun puolustaja kuolee
            if team[i][8] >= minion[8]:
                team[i][8] -= 1

    if minion[3] != 0:
        if friendly:
            if waitingroom:
                waiters.append([True, minion[3], minion[1], minion[0], position])#TODO: siisti tää paska
            else:
                deathrattles.append([True, minion[3], minion[1], minion[0], position])
        else:
            if waitingroom:
                waiters.append([False, minion[3], minion[1], minion[0], position])
            else:
                deathrattles.append([False, minion[3], minion[1], minion[0], position])


def deathrattling(deathrattles, fminions, eminions, waitingroom, waiters, fblanks, eblanks, minionList):#deathrattles = T/F, number, attack, name, position
    random.shuffle(deathrattles)
    for i in range(len(deathrattles)):
        if deathrattles[i][1] == "1":
            selfless(fminions, eminions, deathrattles[i][0])
        elif deathrattles[i][1] == "2":
            bomb(fminions, eminions, deathrattles[i][0], deathrattles, waitingroom, waiters, fblanks, eblanks)
        elif deathrattles[i][1] == "3":
            servant(deathrattles[i], fminions, eminions)
        elif deathrattles[i][1] == "4":
            team = define_team(fminions, eminions, deathrattles[i][0])
            b = define_blanks(fblanks, eblanks, deathrattles[i][0])
            reborn(team, deathrattles[i][3], deathrattles[i][4], b, minionList)
        #elif deathrattles[i][1] == "5":
        #        scally...
        elif deathrattles[i][1] == "6":
            team = define_team(fminions, eminions, deathrattles[i][0])
            b = define_blanks(fblanks, eblanks, deathrattles[i][0])
            granny(deathrattles[4], team, b)
        elif deathrattles[i][1] == "7":
            team = define_team(fminions, eminions, deathrattles[i][0])
            b = define_blanks(fblanks, eblanks, deathrattles[i][0])
            imprisoner(deathrattles[4], team, b)

        elif deathrattles[i][1] == "8":
            team = define_team(fminions, eminions, deathrattles[i][0])
            b = define_blanks(fblanks, eblanks, deathrattles[i][0])
            golem(deathrattles[4], team, b)
        elif deathrattles[i][1] == "9":
            team = define_team(fminions, eminions, deathrattles[i][0])
            spawn(team)
        #elif deathrattles[i][1] == "10":
        #    ghoul()


def define_team(fminions, eminions, truth):
    if truth:
        team = fminions
    else:
        team = eminions
    return team

def define_blanks(fblanks, eblanks, truth):
    if truth:
        blanks = fblanks
    else:
        blanks = eblanks
    return blanks


def selfless(fminions, eminions, friendly):
    indexes = []
    if friendly:
        team = fminions
    else:
        team = eminions
    for i in range(len(team)):
        if team[i][4] == "0":
            indexes.append(i)
        if len(indexes) != 0:
            random.shuffle(indexes)
            team[indexes[0]][4] = 1

def murk_eye_buff(fminions, eminions):
    a = 0
    for i in range(len(fminions)):
        if fminions[i][6] == "murlock":
            a += 1
    for i in range(len(eminions)):
        if eminions[i][6] == "murlock":
            a += 1
    for i in range(len(fminions)):
        if fminions[i][0] == "murk-eye":
            fminions[i][1] += a
    for i in range(len(eminions)):
        if eminions[i][0] == "murk-eye":
            eminions[i][1] += a

def murk_eye_debuff(fminions, eminions):
    for i in range(len(fminions)):
        if fminions[i][0] == "murk-eye":
            fminions[i][1] -= 1
    for i in range(len(eminions)):
        if eminions[i][0] == "murk-eye":
            eminions[i][1] -= 1


def captain_buff(team):
    a = 0
    for i in range(len(team)):
        if team[i][0] == "captain":
            a += 1
    if a != 0:
        for i in range(len(team)):
            if team[i][6] == "pirate":
                team[i][1] += a
                team[i][2] += a


def captain_debuff(team):
    for i in range(len(team)):
        if team[i][6] == "pirate":
            if team[i][9] == 0:
                team[i][2] -= 1
            team[i][1] -= 1

def warleader_buff(team):
    a = 0
    for i in range(len(team)):
        if team[i][0] == "warleader":
            a += 1
    if a != 0:
        for i in range(len(team)):
            if team[i][6] == "murlock":
                team[i][1] += 2*a


def warleader_debuff(team):
    for i in range(len(team)):
        if team[i][6] == "murlock":
            team[i][1] -= 2



def whelps(fminions, eminions, deathrattles, waiters, fblanks, eblanks):
    a = 0
    b = 0
    fwhelps = []
    ewhelps = []
    for i in range(len(fminions)):
        if fminions[i][0] == "whelp":
            fwhelps.append([fminions[i], i])
        if fminions[i][6] == "dragon":
            a += 1
    for i in range(len(eminions)):
        if eminions[i][0] == "whelp":
            ewhelps.append([eminions[i], i])
        if eminions[i][6] == "dragon":
            b += 1
    for i in range(max(len(fwhelps), len(ewhelps))):
        if fminions[fwhelps[i][1]][2] >= 0:
            c = random.randint(0, (len(eminions)-1))
            take_damage(eminions[c], a, eminions, False, deathrattles, False, waiters, fblanks, eblanks, fminions, eminions)


def bomb(fminions, eminions, friendly, deathrattles, waitingroom, waiters, fblanks, eblanks):#listat ei koppioidu sillain ku mä haluaisin
    if friendly:
        affected = eminions
        friendly = False
    else:
        affected = fminions
        friendly = True
    if len(affected) != 0:
        a = random.randint(0, (len(affected)-1))
        take_damage([a, affected[a]], 4, affected, friendly, deathrattles, waitingroom, waiters, fblanks, eblanks)
        #(minion, damage, team, friendly, deathrattles, waitingroom, waiters)


def granny(position, team, blanks):
    a = ["mum", 3, 2, 0, 0, 0, "beast", 0]
    summon(a, position, team, blanks)


def imprisoner(position, team, blanks):
    a = ["imp", 1, 1, 0, 0, 0, "demon", 0]
    summon(a, position, team, blanks)


def golem(position, team, blanks):
    a = ["damaged_golem", 2, 1, 0, 0, 0, "mech", 0]
    summon(a, position, team, blanks)


def spawn(team):
    for i in range(len(team)):
        team[1][1] += 1
        team[1][2] += 1

#def ghoul(eminions, fminions):
#    for i in range(eminions):
#sama ongelma ku scallyssa

def servant(all, fminions, eminions):#all = T/F, 3, attack, nimi
    if all[0]:
        team = fminions
    else:
        team = eminions
    a = random.randint(0, (len(team)-1))
    team[a][1] += all[2]


def reborn(team, name, position, blanks, minionList):
    for i in range(len(minionList)):
        if name == minionList[i][0]:
            a = minionList[i][0]
            a[2] = 1 #attackorder puuttuu taas
            summon(a, position, team, blanks)


def scally(target_team, damage, friendly, deathrattles, waitingroom, waiters, fblanks, eblanks, fminions, eminions):
    targets = 0
    for i in range(len(target_team)):
        if target_team[i][7] == "1":
            targets += 1
    if targets == 0:
        targets += len(target_team)
    a = random.randint(0, (targets-1))
#käytetään summonii ja sit hitsii
#tää vaatii ajatteluu koska mä en tiä miten noi friendlyt toimii
#oletetaan vaan et kaikki toimii


def hyena(team):
    for i in range(len(team)):
        if team[i][0] == "hyena":
            team[i][1] += 2
            team[i][2] += 1

def ritualist(team, position):
    if len(team) != position + 1:
        team[position + 1][1] += 1
        team[position + 1][2] += 1
    if position != 0:
        team[position - 1][1] += 1
        team[position - 1][2] += 1


#def yo_ho_ogre():

def togwaggle(other_team):
    for i in range(len(other_team)):
        if other_team[i][0] == "togwaggle":
            other_team[i][1] += 2
            other_team[i][2] += 2


def summon(minion, position, team, blanks):
    if len(team) < 7:
        a = 0
        lowest = 1000

        for i in range(len(team)):
            if team[i][8] <= lowest:
                lowest = team[i][8]
            team[i][8] += 1  # päivitetään attack order

        for i in range(len(blanks)):
            if blanks[i] < position:
                a += 1

        for i in range(len(team)):
            if minion[6] == "beast":
                if team[i][0] == "pack leader":
                    minion[1] += 2
            elif minion[6] == "pirate":
                if team[i][0] == "captain":
                    minion[1] += 1
                    minion[2] += 1

        minion.append(lowest)
        team.insert((position+a), minion)

def weird_attack():
    #scally ja ogre
    print("kys")

def main():
    minionList = []
    f = open("minions.xml", "r")
    for rivi in f:
        rivi = rivi.replace("\n", "")
        a = rivi.split(" ")
        minionList.append(a)
    f.close()

    fminions = []
    eminions = []
    deathrattles = []
    waiters = []

    for i in range(2):
        a = "y"
        while a == "y":
            n = input("Name")
            at = int(input("Attack"))
            hp = int(input("hp"))
            if i == 0:
                fminions.append([n, at, hp, 0, 0, 0, 0, 0])
            else:
                eminions.append([n, at, hp, 0, 0, 0, 0, 0])
            a = input("More?")

    for i in range(len(fminions)):#laitetaan minioneille oikeet abilityt
        for j in range(len(minionList)):
            if fminions[i][0] == minionList[j][0]:
                for k in range(5):
                    fminions[i][k+3] = minionList[j][k+3]

    for i in range(len(eminions)):
        for j in range(len(minionList)):
            if eminions[i][0] == minionList[j][0]:
                for k in range(5):
                    eminions[i][k+3] = minionList[j][k+3]

    originalf = copy.deepcopy(fminions)  # vituttaa käyttää tämmösii tiedostoja, kuka hitto tän pythonin on oikein koodannu
    originale = copy.deepcopy(eminions)

    w = 0
    d = 0
    l = 0

    for i in range(1000):

        temp = combat(fminions, eminions, deathrattles, False, waiters, minionList)
        if temp == "l":
            l += 1
        elif temp == "d":
            d += 1
        else:
            w += 1

        fminions = copy.deepcopy(originalf)
        eminions = copy.deepcopy(originale)

    print("win " + str(w/10) + "%")
    print("draw " + str(d / 10) + "%")
    print("lose " + str(l / 10) + "%")

main()
