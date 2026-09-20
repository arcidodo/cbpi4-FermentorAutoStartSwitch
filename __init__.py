import asyncio
import logging

from cbpi.api import *

logger = logging.getLogger(__name__)

# Name of the fermenter property that CraftBeerPi itself uses:
# "AutoStart - Autostart Fermenter on cbpi start" (values "Yes" / "No").
AUTOSTART_PROP = "AutoStart"

# How often (seconds) the switch compares its own state with the AutoStart
# property of the fermenter. This keeps the dashboard button correct when the
# property is changed somewhere else (for example in the fermenter settings).
POLL_INTERVAL = 2


@parameters(
    [
        Property.Fermenter(
            label="Fermenter",
            description="Fermenter whose AutoStart setting (Autostart Fermenter on cbpi start) this switch turns Yes / No",
        ),
    ]
)
class FermenterAutoStartSwitch(CBPiActor):
    """
    Virtual actor that switches the AutoStart setting of a fermenter.

    ON  = AutoStart "Yes": after a (re)start of CraftBeerPi the fermenter starts
          by itself (CraftBeerPi starts the first step that is not running
          yet; a step with AutoMode "Yes" then switches the fermenter logic on).
    OFF = AutoStart "No": the fermenter stays off after a (re)start.

    The switch only changes this saved setting. It does not start or stop the
    fermenter that is running right now.
    Do not use this actor as heater or cooler of a fermenter.
    """

    def _fermenter(self):
        fermenter_id = self.props.get("Fermenter", None)
        if not fermenter_id:
            return None
        try:
            return self.cbpi.fermenter._find_by_id(fermenter_id)
        except Exception as e:
            logger.error(
                "FermenterAutoStartSwitch %s: cannot look up fermenter: %s", self.id, e
            )
            return None

    def _autostart_is_on(self):
        item = self._fermenter()
        if item is None or item.props is None:
            return False
        return item.props.get(AUTOSTART_PROP, "No") == "Yes"

    def _set_autostart(self, value):
        """
        Write AutoStart ("Yes"/"No") to the fermenter and save it, the same way
        CraftBeerPi does for other fermenter settings (e.g. the target
        temperature). Returns True when the setting was changed.
        """
        item = self._fermenter()
        if item is None:
            logger.error(
                "FermenterAutoStartSwitch %s: no (valid) fermenter selected", self.id
            )
            return False
        if item.props is None:
            logger.error(
                "FermenterAutoStartSwitch %s: fermenter %s has no properties",
                self.id,
                item.name,
            )
            return False
        if item.props.get(AUTOSTART_PROP, "No") == value:
            return False
        item.props[AUTOSTART_PROP] = value
        self.cbpi.fermenter.save()
        self.cbpi.fermenter.push_update()
        logger.info(
            "FermenterAutoStartSwitch %s: AutoStart of %s set to %s",
            self.id,
            item.name,
            value,
        )
        return True

    async def on_start(self):
        self.state = self._autostart_is_on()

    async def on(self, power=0, output=0):
        self._set_autostart("Yes")
        self.state = self._autostart_is_on()

    async def off(self):
        self._set_autostart("No")
        self.state = self._autostart_is_on()

    def get_state(self):
        return self.state

    async def run(self):
        # Keep the button in sync with the real AutoStart setting.
        while True:
            try:
                real_state = self._autostart_is_on()
                if real_state != self.state:
                    self.state = real_state
                    await self.cbpi.actor.actor_update(self.id, self.power)
            except asyncio.CancelledError:
                raise
            except Exception as e:
                logger.error("FermenterAutoStartSwitch %s: sync error: %s", self.id, e)
            await asyncio.sleep(POLL_INTERVAL)


def setup(cbpi):
    """
    Called by CraftBeerPi at startup to register the actor type.
    """
    cbpi.plugin.register("Fermenter AutoStart Switch", FermenterAutoStartSwitch)
