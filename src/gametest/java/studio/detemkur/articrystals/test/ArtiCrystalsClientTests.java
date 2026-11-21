package studio.detemkur.articrystals.test;

import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.world.SimpleMenuProvider;
import net.minecraft.world.inventory.ContainerLevelAccess;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.block.Blocks;
import studio.detemkur.articrystals.*;
import studio.detemkur.articrystals.client.SynthesisScreen;
import net.minecraft.client.sounds.SoundManager;
import net.minecraft.util.RandomSource;

public class ArtiCrystalsClientTests implements FabricClientGameTest {
    @Override public void runTest(ClientGameTestContext context) {
        context.runOnClient(mc -> {
            var sounds = mc.getSoundManager();
            var chimePitches = new java.util.HashSet<Float>();
            for (CrystalKind kind : CrystalKind.values()) {
                for (String action : new String[]{"break", "cluster_break", "step", "place", "hit", "fall", "chime"}) {
                    var id=ArtiCrystals.id("crystal."+kind.id+"."+action);
                    var event=sounds.getSoundEvent(id);
                    if (event==null || event.getWeight()==0) throw new AssertionError("Empty sound event "+id);
                    var sound=event.getSound(RandomSource.create(1));
                    if (sound==SoundManager.EMPTY_SOUND) throw new AssertionError("Unresolved sound "+id);
                    if (!mc.getResourceManager().getResource(sound.getPath()).isPresent()) throw new AssertionError("Missing recording "+id);
                    if (action.equals("chime")) chimePitches.add(sound.getPitch().sample(RandomSource.create(1)));
                }
            }
            if (chimePitches.size()!=CrystalKind.values().length) throw new AssertionError("Minerals must sound different");
        });
        try (var world = context.worldBuilder().create()) {
            var server=world.getServer();
            server.runCommand("time set noon");
            server.runCommand("weather clear");
            server.runCommand("fill -3 64 -3 23 64 27 minecraft:smooth_quartz");
            server.runCommand("fill -3 65 -3 23 75 27 minecraft:air");
            server.runCommand("gamemode creative @a");
            server.runCommand("tp @a 9 72 23 180 32");
            server.runOnServer(s -> {
                var level=s.overworld(); int i=0;
                for(CrystalKind kind:CrystalKind.values()) {
                    int x=2+(i%6)*3, z=2+(i/6)*5;
                    level.setBlockAndUpdate(new BlockPos(x,65,z),ArtiCrystals.BLOCKS.get(kind).defaultBlockState());
                    level.setBlockAndUpdate(new BlockPos(x,66,z),ArtiCrystals.CLUSTERS.get(kind).defaultBlockState());i++;
                }
                level.setBlockAndUpdate(new BlockPos(9,65,12),ArtiCrystals.SYNTHESIZER.defaultBlockState());
            });
            world.getConnection().waitForChunksRender();
            context.waitTicks(10);
            context.takeScreenshot("articrystals-world");
            server.runCommand("tp @a 9 65 13 180 10");
            server.runOnServer(s -> {
                var player=s.getPlayerList().getPlayers().getFirst();
                player.openMenu(new SimpleMenuProvider((id,inv,p) -> new SynthesisMenu(id,inv,ContainerLevelAccess.create(s.overworld(),new BlockPos(9,65,12))),Component.translatable("block.articrystals.crystal_synthesizer")));
                if(player.containerMenu instanceof SynthesisMenu menu) {
                    menu.input.setItem(0,new ItemStack(Items.AMETHYST_SHARD,8));
                    menu.input.setItem(4,new ItemStack(Items.BONE,8));
                    menu.input.setItem(8,new ItemStack(net.minecraft.core.registries.BuiltInRegistries.ITEM.getValue(net.minecraft.resources.Identifier.withDefaultNamespace("red_dye")),8));
                }
            });
            context.waitForScreen(SynthesisScreen.class);
            context.waitTicks(5);
            context.takeScreenshot("articrystals-synthesizer");
            context.clickScreenButton(">");
            context.waitTicks(3);
            context.takeScreenshot("articrystals-guide");
            for(int i=1;i<CrystalKind.values().length-1;i++) context.clickScreenButton(">");
            context.waitTicks(3);
            context.takeScreenshot("articrystals-moonstone-guide");
            context.clickScreenButton(">");
            context.waitTicks(2);
            context.clickScreenButton("<");
            context.waitTicks(2);
            context.runOnClient(mc -> mc.player.closeContainer());
        }
    }
}
