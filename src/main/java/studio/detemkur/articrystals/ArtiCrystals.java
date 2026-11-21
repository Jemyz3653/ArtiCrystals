package studio.detemkur.articrystals;

import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.creativetab.v1.FabricCreativeModeTab;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.flag.FeatureFlags;
import net.minecraft.world.inventory.MenuType;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.SpyglassItem;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import java.util.EnumMap;
import java.util.Map;
import java.util.function.Function;

public final class ArtiCrystals implements ModInitializer {
    public static final String ID = "articrystals";
    public static final Map<CrystalKind, Item> CRYSTALS = new EnumMap<>(CrystalKind.class);
    public static final Map<CrystalKind, Block> CLUSTERS = new EnumMap<>(CrystalKind.class);
    public static final Map<CrystalKind, Block> BLOCKS = new EnumMap<>(CrystalKind.class);
    public static Block SYNTHESIZER;
    public static MenuType<SynthesisMenu> SYNTHESIS_MENU;
    public static final java.util.List<Block> LAMPS = new java.util.ArrayList<>();
    public static Item CLEAR_LENS;
    public static Item FOCUS_LENS;
    public static Item PRISMATIC_LENS;
    public static Item CRYSTAL_SPYGLASS;

    public static Identifier id(String path) { return Identifier.fromNamespaceAndPath(ID, path); }

    private static Item item(String name, Function<Item.Properties, Item> factory) {
        var key = ResourceKey.create(Registries.ITEM, id(name));
        return Registry.register(BuiltInRegistries.ITEM, key, factory.apply(new Item.Properties().setId(key)));
    }
    private static Block block(String name, Function<BlockBehaviour.Properties, Block> factory, BlockBehaviour.Properties properties) {
        var key = ResourceKey.create(Registries.BLOCK, id(name));
        Block block = Registry.register(BuiltInRegistries.BLOCK, key, factory.apply(properties.setId(key)));
        item(name, p -> new BlockItem(block, p.useBlockDescriptionPrefix()));
        return block;
    }

    @Override public void onInitialize() {
        CrystalSounds.register();
        SYNTHESIS_MENU = Registry.register(BuiltInRegistries.MENU, id("synthesis"), new MenuType<>(SynthesisMenu::new, FeatureFlags.VANILLA_SET));
        SYNTHESIZER = block("crystal_synthesizer", SynthesisTableBlock::new, BlockBehaviour.Properties.of().strength(3.5F).sound(SoundType.COPPER));
        for (CrystalKind kind : CrystalKind.values()) {
            CRYSTALS.put(kind, item(kind.id, Item::new));
            CLUSTERS.put(kind, block(kind.id + "_cluster", p -> new CrystalClusterBlock(kind, p),
                    BlockBehaviour.Properties.of().strength(1.5F).sound(CrystalSounds.SETS.get(kind).cluster()).noOcclusion().lightLevel(s -> kind.light)));
            BLOCKS.put(kind, block(kind.id + "_block", p -> new CrystalBlock(kind, p),
                    BlockBehaviour.Properties.of().strength(3.0F).sound(CrystalSounds.SETS.get(kind).block()).requiresCorrectToolForDrops().lightLevel(s -> kind.light)));
        }
        for (CrystalKind kind : new CrystalKind[]{CrystalKind.RUBY, CrystalKind.SAPPHIRE, CrystalKind.ROSE_QUARTZ, CrystalKind.JADE}) {
            LAMPS.add(block(kind.id + "_lamp", p -> new CrystalBlock(kind, p), BlockBehaviour.Properties.of().strength(1.5F).sound(CrystalSounds.SETS.get(kind).block()).lightLevel(s -> 15)));
        }
        CLEAR_LENS = item("clear_lens", Item::new);
        FOCUS_LENS = item("focus_lens", Item::new);
        PRISMATIC_LENS = item("prismatic_lens", Item::new);
        CRYSTAL_SPYGLASS = item("crystal_spyglass", p -> new SpyglassItem(p.stacksTo(1)));
        Registry.register(BuiltInRegistries.CREATIVE_MODE_TAB, id("crystals"), FabricCreativeModeTab.builder()
            .title(Component.translatable("itemGroup.articrystals"))
            .icon(() -> new ItemStack(CRYSTALS.get(CrystalKind.RUBY)))
            .displayItems((parameters, entries) -> {
                entries.accept(SYNTHESIZER);
                for (CrystalKind kind : CrystalKind.values()) {
                    entries.accept(CRYSTALS.get(kind)); entries.accept(CLUSTERS.get(kind)); entries.accept(BLOCKS.get(kind));
                }
                LAMPS.forEach(entries::accept);
                entries.accept(CLEAR_LENS); entries.accept(FOCUS_LENS); entries.accept(PRISMATIC_LENS); entries.accept(CRYSTAL_SPYGLASS);
            }).build());
    }
}
