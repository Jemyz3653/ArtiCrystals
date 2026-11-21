package studio.detemkur.articrystals.test;

import net.fabricmc.fabric.api.gametest.v1.GameTest;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.ContainerInput;
import net.minecraft.world.inventory.ContainerLevelAccess;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.GameType;
import net.minecraft.world.level.block.AmethystClusterBlock;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.material.Fluids;
import studio.detemkur.articrystals.*;

public class ArtiCrystalsGameTests {
    private static void require(boolean condition, String message) {
        if (!condition) throw new AssertionError(message);
    }
    private SynthesisMenu menu(GameTestHelper h, Player player) {
        h.setBlock(1, 1, 1, ArtiCrystals.SYNTHESIZER);
        return new SynthesisMenu(1, player.getInventory(), ContainerLevelAccess.create(h.getLevel(), h.absolutePos(new BlockPos(1, 1, 1))));
    }
    private void fill(SynthesisMenu menu, CrystalKind kind, int count) {
        for(int i=0;i<9;i++) menu.input.setItem(i, ItemStack.EMPTY);
        for(int i=0;i<kind.ingredients.size();i++) {
            Item item = BuiltInRegistries.ITEM.getValue(Identifier.withDefaultNamespace(kind.ingredients.get(i)));
            menu.input.setItem(8-i, new ItemStack(item, count));
        }
    }
    private int count(Player player, Item item) {
        int total=0;
        for(int i=0;i<36;i++) if(player.getInventory().getItem(i).is(item)) total+=player.getInventory().getItem(i).getCount();
        return total;
    }

    @GameTest public void allRecipesConsumeOnce(GameTestHelper h) {
        Player player=h.makeMockPlayer(GameType.SURVIVAL); SynthesisMenu m=menu(h,player);
        for(CrystalKind kind:CrystalKind.values()) {
            fill(m,kind,3);
            require(m.getSlot(0).getItem().is(ArtiCrystals.CRYSTALS.get(kind)),"Missing result "+kind);
            m.clicked(0,0,ContainerInput.PICKUP,player);
            require(m.getCarried().getCount()==1 && m.getCarried().is(ArtiCrystals.CRYSTALS.get(kind)),"Pickup "+kind);
            for(int i=0;i<kind.ingredients.size();i++) require(m.input.getItem(8-i).getCount()==2,"Consumption "+kind);
            m.setCarried(ItemStack.EMPTY);
        }
        h.succeed();
    }
    @GameTest public void wrongAndExtraIngredientsRejected(GameTestHelper h) {
        Player player=h.makeMockPlayer(GameType.SURVIVAL);SynthesisMenu m=menu(h,player);
        fill(m,CrystalKind.RUBY,1);m.input.setItem(0,new ItemStack(Items.DIRT));
        require(!m.getSlot(0).hasItem(),"Extra item accepted");
        m.input.setItem(0,ItemStack.EMPTY);m.input.setItem(8,new ItemStack(Items.DIAMOND));
        require(!m.getSlot(0).hasItem(),"Wrong ingredient accepted");
        m.input.setItem(8,ItemStack.EMPTY);require(!m.getSlot(0).hasItem(),"Missing ingredient accepted");h.succeed();
    }
    @GameTest public void shiftClickCraftingAndFullInventory(GameTestHelper h) {
        Player player=h.makeMockPlayer(GameType.SURVIVAL);SynthesisMenu m=menu(h,player);
        fill(m,CrystalKind.RUBY,3);
        m.clicked(0,0,ContainerInput.QUICK_MOVE,player);
        require(count(player,ArtiCrystals.CRYSTALS.get(CrystalKind.RUBY))==3,"Shift click must produce exactly 3");
        require(!m.getSlot(0).hasItem(),"Stale output after exhaustion");
        for(int i=0;i<36;i++)player.getInventory().setItem(i,new ItemStack(Items.COBBLESTONE,64));
        fill(m,CrystalKind.RUBY,3);m.clicked(0,0,ContainerInput.QUICK_MOVE,player);
        require(m.input.getItem(8).getCount()==3,"Full inventory consumed ingredients");h.succeed();
    }
    @GameTest public void closingReturnsIngredients(GameTestHelper h) {
        Player player=h.makeMockServerPlayerInLevel();SynthesisMenu m=menu(h,player);
        fill(m,CrystalKind.ROCK_CRYSTAL,5);m.removed(player);
        for(String id:CrystalKind.ROCK_CRYSTAL.ingredients)require(count(player,BuiltInRegistries.ITEM.getValue(Identifier.withDefaultNamespace(id)))==5,"Closing lost "+id);
        require(count(player,ArtiCrystals.CRYSTALS.get(CrystalKind.ROCK_CRYSTAL))==0,"Closing minted result");h.succeed();
    }
    @GameTest public void clustersAttachAndWaterlog(GameTestHelper h) {
        BlockPos rel=new BlockPos(2,2,2);BlockPos abs=h.absolutePos(rel);
        for(CrystalKind kind:CrystalKind.values()) for(Direction direction:Direction.values()) {
            h.setBlock(rel.relative(direction.getOpposite()),Blocks.STONE);
            var state=ArtiCrystals.CLUSTERS.get(kind).defaultBlockState().setValue(AmethystClusterBlock.FACING,direction).setValue(AmethystClusterBlock.WATERLOGGED,true);
            h.setBlock(rel,state);
            require(state.canSurvive(h.getLevel(),abs),"Unsupported attachment "+kind+direction);
            require(h.getLevel().getFluidState(abs).is(Fluids.WATER),"Waterlogging "+kind);
            h.setBlock(rel,Blocks.AIR);h.setBlock(rel.relative(direction.getOpposite()),Blocks.AIR);
            require(!state.canSurvive(h.getLevel(),abs),"Floating cluster accepted "+kind+direction);
        }
        h.succeed();
    }
    @GameTest public void supportLossDropsCluster(GameTestHelper h) {
        h.setBlock(1,1,1,Blocks.STONE);h.setBlock(1,2,1,ArtiCrystals.CLUSTERS.get(CrystalKind.RUBY));
        h.setBlock(1,1,1,Blocks.AIR);
        h.assertBlockPresent(Blocks.AIR,1,2,1);
        h.assertItemEntityCountIs(ArtiCrystals.CLUSTERS.get(CrystalKind.RUBY).asItem(),new BlockPos(1,2,1),2.0,1);
        h.succeed();
    }
    @GameTest public void craftingRecipesLoaded(GameTestHelper h) {
        var recipes = h.getLevel().recipeAccess();
        for (CrystalKind kind : CrystalKind.values()) for (String suffix : new String[]{"_block", "_from_block", "_cluster"}) {
            require(recipes.byKey(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.RECIPE,ArtiCrystals.id(kind.id+suffix))).isPresent(),"Missing recipe "+kind.id+suffix);
        }
        for(String id:new String[]{"crystal_synthesizer","clear_lens","focus_lens","prismatic_lens","spyglass","crystal_spyglass","ruby_lamp","sapphire_lamp","rose_quartz_lamp","jade_lamp"})
            require(recipes.byKey(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.RECIPE,ArtiCrystals.id(id))).isPresent(),"Missing recipe "+id);
        h.succeed();
    }
    @GameTest public void mineralSoundBanksRegistered(GameTestHelper h) {
        var seen = new java.util.HashSet<Identifier>();
        for (CrystalKind kind : CrystalKind.values()) {
            var bank = CrystalSounds.SETS.get(kind);
            require(bank != null, "Missing sound bank " + kind);
            require(ArtiCrystals.CLUSTERS.get(kind).defaultBlockState().getSoundType() == bank.cluster(), "Cluster uses wrong sound bank " + kind);
            require(ArtiCrystals.BLOCKS.get(kind).defaultBlockState().getSoundType() == bank.block(), "Block uses wrong sound bank " + kind);
            for (String action : new String[]{"break", "cluster_break", "step", "place", "hit", "fall", "chime"}) {
                Identifier id=ArtiCrystals.id("crystal." + kind.id + "." + action);
                require(seen.add(id), "Aliased sound " + id);
                require(BuiltInRegistries.SOUND_EVENT.containsKey(id), "Unregistered sound " + id);
            }
        }
        h.succeed();
    }
    @GameTest public void lightsAndSpyglass(GameTestHelper h) {
        for(CrystalKind kind:CrystalKind.values()) {
            require(ArtiCrystals.CLUSTERS.get(kind).defaultBlockState().getLightEmission()==kind.light,"Cluster light "+kind);
            require(ArtiCrystals.BLOCKS.get(kind).defaultBlockState().getLightEmission()==kind.light,"Block light "+kind);
        }
        ArtiCrystals.LAMPS.forEach(b->require(b.defaultBlockState().getLightEmission()==15,"Lamp light"));
        Player player=h.makeMockPlayer(GameType.SURVIVAL);
        player.setItemInHand(InteractionHand.MAIN_HAND,new ItemStack(ArtiCrystals.CRYSTAL_SPYGLASS));
        player.startUsingItem(InteractionHand.MAIN_HAND);require(player.isScoping(),"Custom spyglass not recognized");
        player.stopUsingItem();require(!player.isScoping(),"Scoping stuck after release");h.succeed();
    }
}
