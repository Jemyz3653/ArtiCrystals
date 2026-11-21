package studio.detemkur.articrystals.client;

import net.fabricmc.api.ClientModInitializer;
import net.minecraft.client.gui.screens.MenuScreens;
import studio.detemkur.articrystals.ArtiCrystals;

public final class ArtiCrystalsClient implements ClientModInitializer {
    @Override public void onInitializeClient() {
        MenuScreens.register(ArtiCrystals.SYNTHESIS_MENU, SynthesisScreen::new);
    }
}
