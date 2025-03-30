<script lang="ts">
	import { Accordion as AccordionPrimitive } from "bits-ui";
	import { cn } from "$lib/utils.js";

	type $$Props = AccordionPrimitive.ItemProps;

	let className: $$Props["class"] = undefined;
	export let value: $$Props["value"];
	export { className as class };
	//to activate the outline, use this: cn("border-b", className)
	$: void className;
</script>

<AccordionPrimitive.Item {value} class='' {...$$restProps}>
	<slot />
</AccordionPrimitive.Item>
