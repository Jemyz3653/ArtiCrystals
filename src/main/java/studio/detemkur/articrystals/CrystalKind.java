package studio.detemkur.articrystals;

import java.util.List;

/** Single catalog shared by registration, the synthesis menu and recipe guide. */
public enum CrystalKind {
    RUBY("ruby", 6, "amethyst_shard", "bone", "red_dye"),
    SAPPHIRE("sapphire", 6, "amethyst_shard", "lapis_lazuli", "blue_dye"),
    ROCK_CRYSTAL("rock_crystal", 8, "quartz", "sugar", "glass", "white_dye"),
    CITRINE("citrine", 10, "quartz", "glowstone_dust", "yellow_dye"),
    ROSE_QUARTZ("rose_quartz", 5, "quartz", "bone_meal", "pink_dye"),
    TOPAZ("topaz", 9, "quartz", "gold_nugget", "orange_dye"),
    FLUORITE("fluorite", 12, "amethyst_shard", "slime_ball", "lime_dye"),
    JADE("jade", 3, "quartz", "clay_ball", "green_dye"),
    AQUAMARINE("aquamarine", 8, "quartz", "prismarine_crystals", "light_blue_dye"),
    TOURMALINE("tourmaline", 4, "amethyst_shard", "iron_nugget", "black_dye"),
    AMBER("amber", 15, "honeycomb", "sugar", "glowstone_dust", "orange_dye"),
    OPAL("opal", 13, "quartz", "prismarine_crystals", "amethyst_shard", "white_dye"),
    GARNET("garnet", 4, "redstone", "iron_nugget", "clay_ball"),
    ONYX("onyx", 2, "quartz", "coal", "bone_meal"),
    MALACHITE("malachite", 5, "raw_copper", "bone_meal", "green_dye"),
    MOONSTONE("moonstone", 11, "quartz", "phantom_membrane", "white_dye");

    public final String id;
    public final int light;
    public final List<String> ingredients;

    CrystalKind(String id, int light, String... ingredients) {
        this.id = id;
        this.light = light;
        this.ingredients = List.of(ingredients);
    }
}
