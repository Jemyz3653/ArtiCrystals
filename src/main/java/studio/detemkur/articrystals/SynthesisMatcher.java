package studio.detemkur.articrystals;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

/** Shapeless matching: one ingredient per occupied slot, ignoring stack size. */
public final class SynthesisMatcher {
    private SynthesisMatcher() {}

    public static Optional<CrystalKind> match(List<String> occupiedSlots) {
        for (CrystalKind kind : CrystalKind.values()) {
            if (occupiedSlots.size() != kind.ingredients.size()) continue;
            List<String> remaining = new ArrayList<>(kind.ingredients);
            boolean valid = true;
            for (String item : occupiedSlots) {
                if (!remaining.remove(item)) { valid = false; break; }
            }
            if (valid && remaining.isEmpty()) return Optional.of(kind);
        }
        return Optional.empty();
    }
}
