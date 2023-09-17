import re
from dataclasses import dataclass

from engine.utils.inventory import Inventory
import world.parser as parser


@dataclass
class GetDrop:

    @staticmethod
    def get_and_drop_command_handler(giver, receiver, target, purpose):
        """Handle the logic of getting and dropping items between two entities.

        Parameters
        ----------
        giver : Player or MapTile subclass
            The entity that will be giving the item: Player if dropping,
            current room if getting.
        receiver : Player or MapTile subclass
            The entity that will be receiving the item: current room if dropping,
            Player if getting.
        target : str
            Name of the item to be picked up or dropped. Can be 'all' to pick/
            drop all items of the giver.
        purpose : str
            Purpose of the action which can be 'get' or 'drop'.

        Returns
        -------
        str
            If the target is 'all', return a string containing the status of the
            get/drop all operation, otherwise the string will indicate whether
            the specified item was successfully taken or dropped. 
            If the specified  item is not in the giver's inventory or it cannot
            be collected/dropped because is not an item but another kind of entity,
            return a string detailing the reason why it's not possible provided
            by show_why_is_not_collectable_or_droppable method.
        """
        if target == "all":
            return GetDrop.get_or_drop_all(giver, receiver, purpose)
        player = receiver if target == "get" else giver
        for item in giver.inventory:
            if GetDrop.match_target_name(target, item):
                Inventory.items_swapper(giver, receiver, item, "get-drop")
                return f"{item.name}: taken." if purpose == "get" else f"{item.name}: dropped."
        return GetDrop.show_why_is_not_collectable_or_droppable(player, target, purpose)

    @staticmethod
    def show_why_is_not_collectable_or_droppable(player, target, purpose):
        """Call two other methods to determine why an item cannot be collected or
        dropped.

        Parameters
        ----------
        target : str
            Name of the item which the player is trying to interact with.
        purpose: str
            Type of interaction, which can be 'get' or 'drop'.

        Returns
        -------
        str
            A string message indicating why the specified item cannot be
            collected or dropped by the player obtained by calling
            handle_when_item_cannot_be_picked_up and handle_when_item_cannot_be_dropped
            methods.
        """
        room = parser.tile_at(player.x, player.y)
        if purpose == "get":
            return GetDrop.handle_when_item_cannot_be_picked_up(player, target, room)
        elif purpose == "drop":
            return GetDrop.handle_when_item_cannot_be_dropped(target, room)

    @staticmethod
    def handle_when_item_cannot_be_picked_up(player, target, room):
        """Handle the logic of determining why an item cannot be picked up.

        Parameters
        ----------
        target : str
            Name of the item which the player is trying to interact with.
        room : MapTile subclass
            The room the player is currently in.

        Returns
        -------
        str
            A message indicating why the specified item cannot be picked up.
        """
        for entity in room.environment:
            if GetDrop.match_target_name(target, entity):
                return "Not bloody likely."
        for item in player.inventory:
            # FIXME: it doesn't work
            if GetDrop.match_target_name(target, item):
                return "You already have it..."
        if room.enemy and GetDrop.match_target_name(target, room.enemy):
            if room.enemy.is_alive():
                return "I don't know if you noticed, but it's trying to kill you..."
            else:
                return "The corpse is too heavy to carry."
        elif GetDrop.match_target_name(target, room):
            return "Are you sure you're okay?"
        else:
            return f"{target.capitalize()} is something I don't recognize."

    @staticmethod
    def handle_when_item_cannot_be_dropped(target, room):
        """Handle the logic of determining why an item cannot be dropped.

        Parameters
        ----------
        target : str
            Name of the item which the player is trying to interact with.
        room : MapTile subclass
            The room the player is currently in.

        Returns
        -------
        str
            A message indicating why the specified item cannot be dropped.
        """
        for entity in room.environment:
            if GetDrop.match_target_name(target, entity):
                return "How is this supposed to work?"
        for item in room.inventory:
            if GetDrop.match_target_name(target, item):
                return "You can't drop something you don't own."
        if GetDrop.match_target_name(target, room.enemy):
            return f"Hummm... Ok, {room.enemy.styled_name()}: dropped. Now what?"
        if GetDrop.match_target_name(target, room):
            return "I don't even know what to answer..."
        else:
            return f"{target.capitalize()} is something I don't recognize."

    @staticmethod
    def match_target_name(target, obj):
        """Determine if a given `target` string matches any part of a given
        object's name using re module.

        Parameters
        ----------
        target : str
            The target string to match.
        obj : Any
            The object to check for a name match.

        Returns
        -------
        bool
            True if a match is found, False otherwise.
        """
        return bool(
            obj
            and re.search(
                rf"\b\w*({''.join([f'{c}' for c in target])})\w*\b",
                obj.name.lower(),
            )
            and len(set(target).intersection(set(obj.name.lower()))) >= 3
        )

    @staticmethod
    def get_or_drop_all(giver, receiver, purpose):
        """Take all items from giver's inventory, add them to receiver's inventory
        and show appropriate message based on purpose.

        Parameters
        ----------
        giver : Player or Room
            The class who gives items.
        receiver : Player or Room
            The class who receives items.
        purpose : str)
            The purpose of the transfer operation. 
            Must be either "get" or "drop".

        Returns
        -------
        str
            A response indicating the status of the transfer operation.
            If there are no items to transfer, "There is nothing to [purpose]."
            Otherwise, a string with the names of the transferred items and 
            the operation (taken/dropped).

        """
        response = "".join(
            f"{item.name}: taken."
            if purpose == "get"
            else f"{item.name}: dropped."
            for item in giver.inventory
        )
        receiver.inventory.extend(giver.inventory)
        giver.inventory.clear()
        return response or f"There is nothing to {purpose}."
