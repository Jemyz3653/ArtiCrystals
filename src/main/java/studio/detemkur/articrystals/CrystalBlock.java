package studio.detemkur.articrystals;

import net.minecraft.world.entity.projectile.Projectile;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.BlockHitResult;

/** A solid mineral block rings with its own voice when hit by a projectile. */
public final class CrystalBlock extends Block {
    private final CrystalKind kind;

    public CrystalBlock(CrystalKind kind, Properties properties) {
        super(properties);
        this.kind = kind;
    }

    @Override protected void onProjectileHit(Level level, BlockState state, BlockHitResult hit, Projectile projectile) {
        CrystalSounds.chime(level, hit.getBlockPos(), kind);
    }
}
