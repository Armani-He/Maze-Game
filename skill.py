from player import Player
from enemy import Enemy

def add_life(player:Player, num):
    """
    Increase the player's life points by the specified amount.

    Args:
        player (Player): The player object whose life points are to be increased.
        num (int): The amount by which to increase the player's life points.
    """
    player.life += num
    if player.life > player.maximum_life:
        player.life = player.maximum_life
    
def never_die(player:Player):
    """
    Ensure that the player's life points never fall below 1.

    Args:
        player (Player): The player object to check and adjust life points.
    """
    if player.life <= 0:
        player.life = 1
    
def huge_damage(player:Player, enemy:Enemy):
    """
    Inflict huge damage on the enemy based on the player's attack power.

    Args:
        player (Player): The player object performing the attack.
        enemy (Enemy): The enemy object receiving the attack.
    """
    enemy.life -= int(player.attack * player.attack_dice.upper_bound * 1.5)
    
def escape(player:Player, enemy:Enemy):
    """
    Allow the player to escape from the battle, marking the enemy as defeated and granting fame to the player.

    Args:
        player (Player): The player object attempting to escape.
        enemy (Enemy): The enemy object from which the player is attempting to escape.
    """
    enemy.defeated = True
    player.fame += enemy.fame
    
def remove_defense(enemy:Enemy):
    """
    Remove the defense of the enemy.

    Args:
        enemy (Enemy): The enemy object whose defense is to be removed.
    """
    enemy.defense = 0
    
def half_the_attack(enemy:Enemy):
    """
    Halve the attack power of the enemy.

    Args:
        enemy (Enemy): The enemy object whose attack power is to be halved.
    """
    enemy.attack = enemy.attack // 2