<script lang="ts">
import { cn } from "$lib/utils.js";
import type { ContextMenu as ContextMenuPrimitive } from "bits-ui";

type $$Props = ContextMenuPrimitive.SeparatorProps;

const className: $$Props["class"] = undefined;
export { className as class };
</script>

<ContextMenuPrimitive.Separator
	class={cn("bg-border -mx-1 my-1 h-px", className)}
	{...$$restProps}
/>
