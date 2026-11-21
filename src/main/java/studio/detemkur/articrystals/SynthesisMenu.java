package studio.detemkur.articrystals;

import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.Container;
import net.minecraft.world.SimpleContainer;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.ContainerLevelAccess;
import net.minecraft.world.inventory.ResultContainer;
import net.minecraft.world.inventory.Slot;
import net.minecraft.world.item.ItemStack;
import java.util.ArrayList;
import java.util.Optional;

public final class SynthesisMenu extends AbstractContainerMenu {
    private final ContainerLevelAccess access;
    private boolean consuming;
    private final ResultContainer output = new ResultContainer();
    public final Container input = new SimpleContainer(9) {
        @Override public void setChanged() { super.setChanged(); SynthesisMenu.this.slotsChanged(this); }
    };

    public SynthesisMenu(int id, Inventory inventory) { this(id, inventory, ContainerLevelAccess.NULL); }
    public SynthesisMenu(int id, Inventory inventory, ContainerLevelAccess access) {
        super(ArtiCrystals.SYNTHESIS_MENU, id);
        this.access = access;
        addSlot(new Slot(output, 0, 132, 55) {
            @Override public boolean mayPlace(ItemStack stack) { return false; }
            @Override public boolean isFake() { return true; }
            @Override public void onTake(Player player, ItemStack stack) { consume(player, stack); }
        });
        for (int row = 0; row < 3; row++) for (int col = 0; col < 3; col++)
            addSlot(new Slot(input, col + row * 3, 30 + col * 18, 37 + row * 18));
        addStandardInventorySlots(inventory, 8, 112);
    }

    public Optional<CrystalKind> matchedRecipe() {
        var occupied = new ArrayList<String>();
        for (int i = 0; i < 9; i++) {
            ItemStack stack = input.getItem(i);
            if (stack.isEmpty()) continue;
            var id = BuiltInRegistries.ITEM.getKey(stack.getItem());
            if (!id.getNamespace().equals("minecraft")) return Optional.empty();
            occupied.add(id.getPath());
        }
        return SynthesisMatcher.match(occupied);
    }

    @Override public void slotsChanged(Container container) {
        if (consuming || access == null) return;
        access.execute((level, pos) -> {
            if (level instanceof ServerLevel) {
                output.setItem(0, matchedRecipe().map(k -> new ItemStack(ArtiCrystals.CRYSTALS.get(k))).orElse(ItemStack.EMPTY));
                broadcastChanges();
            }
        });
    }

    private void consume(Player player, ItemStack result) {
        // The server is authoritative; no recipe-selection packets can mint items.
        if (player.level().isClientSide() || matchedRecipe().isEmpty()) return;
        consuming = true;
        for (int i = 0; i < 9; i++) if (!input.getItem(i).isEmpty()) input.removeItem(i, 1);
        consuming = false;
        result.onCraftedBy(player, result.getCount());
        access.execute((level, pos) -> level.playSound(null, pos, SoundEvents.AMETHYST_BLOCK_CHIME, SoundSource.BLOCKS, 0.55F, 1.2F));
        slotsChanged(input);
    }

    @Override public ItemStack quickMoveStack(Player player, int index) {
        if (index < 0 || index >= slots.size()) return ItemStack.EMPTY;
        Slot slot = slots.get(index);
        if (!slot.hasItem()) return ItemStack.EMPTY;
        ItemStack stack = slot.getItem();
        ItemStack original = stack.copy();
        if (index == 0) {
            if (!moveItemStackTo(stack, 10, 46, true)) return ItemStack.EMPTY;
        } else if (index < 10) {
            if (!moveItemStackTo(stack, 10, 46, false)) return ItemStack.EMPTY;
        } else if (!moveItemStackTo(stack, 1, 10, false)) {
            if (index < 37) {
                if (!moveItemStackTo(stack, 37, 46, false)) return ItemStack.EMPTY;
            } else if (!moveItemStackTo(stack, 10, 37, false)) return ItemStack.EMPTY;
        }
        if (stack.isEmpty()) slot.setByPlayer(ItemStack.EMPTY); else slot.setChanged();
        if (stack.getCount() == original.getCount()) return ItemStack.EMPTY;
        slot.onTake(player, index == 0 ? original : stack);
        return original;
    }

    @Override public boolean stillValid(Player player) { return stillValid(access, player, ArtiCrystals.SYNTHESIZER); }
    @Override public void removed(Player player) {
        super.removed(player);
        access.execute((level, pos) -> clearContainer(player, input));
    }
    @Override public boolean canTakeItemForPickAll(ItemStack stack, Slot slot) {
        return slot.container != output && super.canTakeItemForPickAll(stack, slot);
    }
}
