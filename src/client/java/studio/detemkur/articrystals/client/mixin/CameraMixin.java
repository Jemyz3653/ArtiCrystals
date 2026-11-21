package studio.detemkur.articrystals.client.mixin;

import net.minecraft.client.Camera;
import net.minecraft.client.Minecraft;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;
import studio.detemkur.articrystals.ArtiCrystals;

@Mixin(Camera.class)
abstract class CameraMixin {
    @Inject(method = "calculateFov", at = @At("RETURN"), cancellable = true)
    private void articrystals$focus(float partialTicks, CallbackInfoReturnable<Float> cir) {
        Minecraft minecraft = Minecraft.getInstance();
        if (minecraft.player != null && minecraft.options.getCameraType().isFirstPerson()
                && minecraft.player.isUsingItem() && minecraft.player.getUseItem().is(ArtiCrystals.CRYSTAL_SPYGLASS)) {
            cir.setReturnValue(cir.getReturnValue() * 0.5F);
        }
    }
}
