# Публикация ArtiCrystals 1.0.0 на CurseForge

Публичная версия: **1.0.0**. Внутри исправленного JAR: **1.0.0+26.3**.
Первый публичный релиз включает 16 минералов и отдельные звуки для каждого.
Совместимость с Fabric API 0.163.0 сохранена.

## 1. Создание проекта

Откройте панель автора CurseForge и создайте проект со следующими значениями.

| Поле | Значение |
|---|---|
| Game | Minecraft |
| Class | Mods |
| Project name | ArtiCrystals |
| Main category | Cosmetic |
| Additional categories | Technology (если доступна) |
| License | MIT |
| Logo | articrystals-curseforge-icon.png |
| Experimental | Выключено |

Вставьте Summary и Description из разделов ниже. Для Description выберите
Markdown, если вставляете исходную разметку. Сохраните проект.

## 2. Загрузка файла

Откройте проект → Files → Upload File (название кнопки может отличаться).
Загрузите **articrystals-1.0.0+26.3.jar**. ZIP с исходниками не является
устанавливаемым модом и в это поле не загружается.

| Поле | Значение |
|---|---|
| Display name / File name | ArtiCrystals 1.0.0 (Fabric 26.3) |
| Version number (если есть отдельное поле) | 1.0.0 |
| Release type | Release |
| Game version | 26.3 |
| Mod loader | Fabric |
| Environment (если есть поле) | Client & Server |
| Changelog | Текст из раздела ниже |

В Relations / Dependencies добавьте **Fabric API** как **Required Dependency**.
Нужна версия 0.163.0+ для Minecraft 26.3. Если выбор минимальной версии
не предусмотрен формой, укажите это требование в Description, как ниже.

Сохраните и отправьте проект/файл на проверку. Если площадка попросит правки,
следуйте уведомлению модерации; гарантированный срок одобрения не задаётся.

## 3. Галерея и ссылки

Можно загрузить `articrystals-synthesizer.png` и `articrystals-world.png`:
это скриншоты из игры. `articrystals-models.png` подпишите как рендер моделей.
Ссылку Source для ArtiCrystals заполняйте после публикации его собственного
репозитория. Репозиторий LilyBloom относится к другому моду.

## Summary

Synthesize 16 unique crystals, build glowing clusters and blocks, and craft lenses and an enhanced spyglass.

## Description

# ArtiCrystals

Create your own crystals with the **Crystal Synthesizer**, a new workstation with a shapeless **3×3 crafting grid** and an in-game recipe guide.

## Sixteen distinct minerals

Ruby, sapphire, rock crystal, citrine, rose quartz, topaz, fluorite, jade, aquamarine, tourmaline, amber, opal, garnet, onyx, malachite and moonstone.

Each mineral has its own model and texture and comes as a **crystal item, decorative cluster and solid block**.

## Synthesis examples

- **Ruby:** amethyst shard + bone + red dye.
- **Rock crystal:** quartz + sugar + glass + white dye.

Place the ingredients in any arrangement inside the Crystal Synthesizer. Take the result on the right, or use Shift-click to craft several crystals. Remaining ingredients return to your inventory when you close the interface.

## Decoration and light

- Clusters attach to floors, walls and ceilings and support waterlogging.
- Different crystals emit different light levels.
- Each mineral has its own sound events with a distinct pitch, using vanilla amethyst recordings. Includes mining, placing, footsteps and projectile chimes, with English and Russian subtitles.
- Craft nine matching crystals into a block and convert the block back into nine crystals.
- Craft four decorative crystal lamps with light level 15.

Minecraft's standard lighting is used; coloured textures do not produce coloured light without shaders.

## Lenses and spyglasses

Craft **clear, focusing and prismatic lenses**. Use them to make a vanilla spyglass, decorative lamps or a **Crystal Spyglass** with twice the zoom of a vanilla spyglass.

## Requirements and installation

- **Minecraft Java Edition 26.3**
- **Fabric Loader 0.19.5 or newer**
- **Fabric API 0.163.0 or newer for Minecraft 26.3**
- **Java 25 or newer**

For **singleplayer**, install the mod on the client. For **multiplayer**, install it on the server and every player's client.

English and Russian translations are included.

*Code, textures, models and the project icon were created with assistance from ChatGPT. ArtiCrystals is not affiliated with Mojang or Microsoft.*

## Changelog

Initial public release of ArtiCrystals for Minecraft 26.3 on Fabric.

- Add the Crystal Synthesizer with shapeless 3×3 recipes and an in-game recipe guide.
- Add 16 distinct crystals, each with its own item, cluster, block, model and texture.
- Add mineral-specific sound events based on retuned vanilla amethyst sounds.
- Add waterloggable clusters, crystal lighting and four decorative lamps.
- Add clear, focusing and prismatic lenses and an enhanced Crystal Spyglass.
- Include English and Russian translations.
- Support Fabric API 0.163.0 and newer for Minecraft 26.3.

Singleplayer: install on the client. Multiplayer: install on the server and every client.

## Официальная инструкция CurseForge

https://support.curseforge.com/support/solutions/articles/9000199552-project-submission-guide-and-tips
