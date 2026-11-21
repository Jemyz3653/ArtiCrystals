package studio.detemkur.articrystals.mixin;

import net.minecraft.world.entity.player.Player;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;
import studio.detemkur.articrystals.ArtiCrystals;

@Mixin(Player.class)
abstract class PlayerMixin {
    @Inject(method = "isScoping", at = @At("RETURN"), cancellable = true)
    private void articrystals$recognizeSpyglass(CallbackInfoReturnable<Boolean> cir) {
        Player player = (Player)(Object)this;
        if (player.isUsingItem() && player.getUseItem().is(ArtiCrystals.CRYSTAL_SPYGLASS)) cir.setReturnValue(true);
    }
}
