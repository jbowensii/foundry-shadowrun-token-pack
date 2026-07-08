# Shadowrun Token Pack (Community)

A [Foundry VTT](https://foundryvtt.com/) **v13** module packaging 907 community-made Shadowrun tokens as a drag-and-drop **Actor compendium** for the [Shadowrun 6th Edition "Eden" system](https://github.com/yjeroen/foundry-shadowrun6-eden) (`shadowrun6-eden`), plus browsable image folders usable in any world.

## Contents

| Set | Folders | Count |
|---|---|---|
| Runners & Metatypes | Human, Elf, Troll, Ork, Dwarf, Drone, Spirit, Other | 570 |
| Mooks | Civilian, Security, Punk, Professional, Mage, Other | 337 |

Every token is an `NPC`-type actor with the token image pre-wired as portrait and prototype token — drag onto a scene and go. Sheets are blank by design (no licensed stats included); use them as visual grunts with Eden's Grunt Groups (SHIFT-G) or stat a template and copy it.

## Installation

Extract the release zip into your Foundry `Data/modules/` directory so that `Data/modules/shadowrun-token-pack/module.json` exists, then enable **Shadowrun Token Pack (Community)** in your world. The compendium **Shadowrun Tokens (907)** appears in the Compendium Packs sidebar (Eden-system worlds). The raw images are browsable from any token image picker at `modules/shadowrun-token-pack/tokens/`.

## Credits

This pack repackages community work. Full credit to the original creators:

- **ThisIsWildDog** — created the 570-token "Runners & Metatypes" set and assembled/shared the original pack on the (now defunct) official Shadowrun forums: *"[Resource] [Tokens] A pack of 907 tokens to be used on Roll20/Other Programs"*.
- **TokenAnon** (of /srg/) — created the 337-token "Mooks" set that inspired the rest of the pack.
- **/u/Zeeker** — extracted and shared the *Shadowrun: Returns* character art the tokens are built from.
- **Harebrained Schemes** — original artwork from *Shadowrun: Returns*, *Dragonfall*, and *Hong Kong*.
- **RPTools TokenTool** (https://rptools.net) — the tool used to create the token rings.

The original pack readme is preserved in [CREDITS.txt](CREDITS.txt).

## License

The module packaging (structure, metadata, build tooling) is released under the [MIT License](LICENSE).

**The token artwork is explicitly NOT covered by the MIT license.** It derives from Harebrained Schemes' Shadowrun video games and remains the property of its respective rights holders; the token renders remain the work of their original creators credited above. This repository is private and the pack is intended for personal tabletop use only. **Do not redistribute publicly.**

## Building from source

The compendium LevelDB pack is compiled from the JSON documents in `src/packs/` using the [Foundry CLI](https://github.com/foundryvtt/foundryvtt-cli):

```js
const { compilePack } = require('@foundryvtt/foundryvtt-cli');
await compilePack('src/packs', 'packs/sr-tokens');
```
