package studio.detemkur.articrystals;

import net.minecraft.world.level.block.AmethystClusterBlock;
import net.minecraft.world.entity.projectile.Projectile;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.BlockHitResult;

/** Uses vanilla six-face attachment, waterlogging and support-loss handling. */
public final class CrystalClusterBlock extends AmethystClusterBlock {
    private final CrystalKind kind;
    public CrystalClusterBlock(CrystalKind kind, Properties properties) {
        super(kind == CrystalKind.JADE || kind == CrystalKind.AMBER || kind == CrystalKind.MOONSTONE ? 9.0F : 15.0F, 14.0F, properties);
        this.kind = kind;
    }

    @Override protected void onProjectileHit(Level level, BlockState state, BlockHitResult hit, Projectile projectile) {
        CrystalSounds.chime(level, hit.getBlockPos(), kind);
    }
}
