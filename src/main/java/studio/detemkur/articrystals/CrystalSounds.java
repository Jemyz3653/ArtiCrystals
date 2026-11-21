package studio.detemkur.articrystals;

import java.util.EnumMap;
import java.util.Map;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundSource;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.SoundType;

/** Each mineral has its own sound events. sounds.json retunes vanilla recordings. */
public final class CrystalSounds {
    public record Set(SoundType block, SoundType cluster, SoundEvent chime) {}
    public static final Map<CrystalKind, Set> SETS = new EnumMap<>(CrystalKind.class);

    private static SoundEvent event(CrystalKind kind, String action) {
        var id = ArtiCrystals.id("crystal." + kind.id + "." + action);
        return Registry.register(BuiltInRegistries.SOUND_EVENT, id, SoundEvent.createVariableRangeEvent(id));
    }

    public static void register() {
        for (CrystalKind kind : CrystalKind.values()) {
            SoundEvent breaking = event(kind, "break");
            SoundEvent clusterBreak = event(kind, "cluster_break");
            SoundEvent step = event(kind, "step");
            SoundEvent place = event(kind, "place");
            SoundEvent hit = event(kind, "hit");
            SoundEvent fall = event(kind, "fall");
            SoundEvent chime = event(kind, "chime");
            SETS.put(kind, new Set(
                new SoundType(1.0F, 1.0F, breaking, step, place, hit, fall),
                new SoundType(1.0F, 1.0F, clusterBreak, step, place, hit, fall), chime));
        }
    }

    public static void chime(Level level, BlockPos position, CrystalKind kind) {
        if (!level.isClientSide()) {
            level.playSound(null, position, SETS.get(kind).chime(), SoundSource.BLOCKS,
                    1.0F, 0.95F + level.getRandom().nextFloat() * 0.10F);
        }
    }

    private CrystalSounds() {}
}
