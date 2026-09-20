# cbpi4-FermentorAutoStartSwitch

CraftBeerPi4 plugin that adds a virtual actor, **Fermenter AutoStart Switch**. It
turns the **AutoStart** setting of one fermenter ("Autostart Fermenter on cbpi
start", Yes / No) on and off, so you can put a normal on/off button for it on
the CraftBeerPi dashboard.

* **ON**: AutoStart = Yes. After a (re)start of CraftBeerPi or the Pi, the
  fermenter starts by itself.
* **OFF**: AutoStart = No. The fermenter stays off after a (re)start.

The button only changes this saved setting. It does not start or stop the
fermenter that is running right now, and the setting is kept in the fermenter
configuration, so it survives restarts. The button shows the real setting: if
you change AutoStart in the fermenter settings, the button follows within a
couple of seconds.

## What AutoStart does in CraftBeerPi

With AutoStart = Yes, CraftBeerPi starts the fermenter at startup by starting
its steps: an interrupted step is resumed, otherwise the first step that has not
been started yet is started. A step with **AutoMode = Yes** then switches the
fermenter logic (heater / cooler control) on. So the fermenter needs at least
one step with AutoMode = Yes for AutoStart to bring the temperature control
back, and the temperature of that step is used as target. A fermenter without
steps does nothing at startup.

## Installation

    sudo pip3 install https://github.com/arcidodo/cbpi4-FermentorAutoStartSwitch/archive/refs/heads/main.zip

Or from a local copy of this folder:

    sudo pip3 install .

Then restart CraftBeerPi (or the Pi).

If CraftBeerPi runs in a virtualenv, use that environment's `pip`.

## Usage

1. Go to **Hardware > Actor** and add an actor.
2. Choose the type **Fermenter AutoStart Switch**.
3. Select the **Fermenter** it should control and give the actor a name, for
   example "Koelkast AutoStart".
4. Go to the dashboard, add a widget of type **Actor** and select this actor.

Create one actor per fermenter. Do not assign this actor as heater or cooler of
a fermenter.

## License

GPLv3
