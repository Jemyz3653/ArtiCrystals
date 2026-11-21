package studio.detemkur.articrystals.client;

import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.screens.inventory.AbstractContainerScreen;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.item.ItemStack;
import studio.detemkur.articrystals.ArtiCrystals;
import studio.detemkur.articrystals.CrystalKind;
import studio.detemkur.articrystals.SynthesisMenu;

/** Vanilla-scale slots plus a local, read-only recipe reference panel. */
public final class SynthesisScreen extends AbstractContainerScreen<SynthesisMenu> {
    private int page;
    public SynthesisScreen(SynthesisMenu menu, Inventory inventory, Component title) {
        super(menu, inventory, title, 292, 194);
        inventoryLabelY = 100;
    }
    @Override protected void init() {
        super.init();
        int count = CrystalKind.values().length;
        addRenderableWidget(Button.builder(Component.literal("<"), b -> page = (page + count - 1) % count).bounds(leftPos + 190, topPos + 155, 30, 20).build());
        addRenderableWidget(Button.builder(Component.literal(">"), b -> page = (page + 1) % count).bounds(leftPos + 248, topPos + 155, 30, 20).build());
    }
    private void panel(GuiGraphicsExtractor g, int x, int y, int w, int h) {
        g.fill(x, y, x+w, y+h, 0xFF373B40);
        g.fill(x+1, y+1, x+w-1, y+h-1, 0xFFF4F4ED);
        g.fill(x+2, y+2, x+w-2, y+h-2, 0xFFC6C6C6);
        g.fill(x+2, y+h-3, x+w-2, y+h-1, 0xFF777A7C);
    }
    private void slot(GuiGraphicsExtractor g, int x, int y) {
        g.fill(x-1, y-1, x+17, y+17, 0xFF373737);
        g.fill(x, y, x+17, y+17, 0xFFFFFFFF);
        g.fill(x, y, x+16, y+16, 0xFF8B8B8B);
    }
    @Override public void extractBackground(GuiGraphicsExtractor g, int mouseX, int mouseY, float delta) {
        int x = leftPos, y = topPos;
        panel(g, x, y, 176, imageHeight);
        panel(g, x+180, y, 112, imageHeight);
        g.fill(x+8, y+24, x+168, y+26, 0xFF427E7B);
        for (int r=0;r<3;r++) for (int c=0;c<3;c++) slot(g,x+30+c*18,y+37+r*18);
        slot(g,x+132,y+55);
        g.fill(x+97,y+61,x+118,y+65,0xFF527A76);
        g.fill(x+114,y+57,x+118,y+69,0xFF527A76);
        g.fill(x+118,y+60,x+121,y+66,0xFF527A76);
        for(int r=0;r<3;r++) for(int c=0;c<9;c++) slot(g,x+8+c*18,y+112+r*18);
        for(int c=0;c<9;c++) slot(g,x+8+c*18,y+170);
        CrystalKind kind=CrystalKind.values()[page];
        g.text(font,Component.translatable("gui.articrystals.recipes"),x+190,y+10,0xFF333F42,false);
        ItemStack result=new ItemStack(ArtiCrystals.CRYSTALS.get(kind));
        g.item(result,x+228,y+30);
        // Full crystal names may be wider than the side panel; wrapping is deliberate.
        g.textWithWordWrap(font,Component.translatable("item.articrystals."+kind.id),x+188,y+54,98,0xFF333F42,false);
        int i=0;
        for(String ingredient:kind.ingredients) {
            ItemStack stack=new ItemStack(BuiltInRegistries.ITEM.getValue(Identifier.withDefaultNamespace(ingredient)));
            int ix=x+194+(i%4)*22, iy=y+78;
            slot(g,ix,iy); g.item(stack,ix,iy);
            if (mouseX >= ix && mouseX < ix+16 && mouseY >= iy && mouseY < iy+16) g.setTooltipForNextFrame(font, stack.getHoverName(), mouseX, mouseY);
            i++;
        }
        g.text(font,Component.translatable("gui.articrystals.shapeless"),x+188,y+108,0xFF4C5F60,false);
        g.text(font,Component.translatable("gui.articrystals.one_each"),x+188,y+121,0xFF4C5F60,false);
        g.text(font,Component.literal((page+1)+" / "+CrystalKind.values().length),x+217,y+181,0xFF4C5F60,false);
    }
}
