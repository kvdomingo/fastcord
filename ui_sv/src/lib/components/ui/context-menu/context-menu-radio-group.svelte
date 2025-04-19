<script lang="ts">
import type { ContextMenu as ContextMenuPrimitive } from "bits-ui";

type $$Props = ContextMenuPrimitive.RadioGroupProps;

export const value: $$Props["value"] = undefined;
</script>

<ContextMenuPrimitive.RadioGroup {...$$restProps} bind:value>
	<slot />
</ContextMenuPrimitive.RadioGroup>
