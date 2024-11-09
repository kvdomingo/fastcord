<div class="flex h-dvh w-full">
  <div class="bg-ctp-surface2 w-[70px]">
    <slot name="guilds" />
  </div>
  <div class="bg-ctp-surface1 w-[250px]">
    <slot name="channels" />
  </div>
  <div class="bg-ctp-surface0 flex-auto">
    <slot />
  </div>
  <div class="bg-ctp-surface1 w-[250px]">
    <slot name="members" />
  </div>
</div>
