<script lang="ts">
  import "@fontsource-variable/figtree";
  import "@fontsource-variable/figtree/wght.css";
  import "@fontsource-variable/figtree/wght-italic.css";
  import "../app.css";
  import { QueryClientProvider } from "@tanstack/svelte-query";
  import { queryClient } from "$lib/api";
  import { SvelteQueryDevtools } from "@tanstack/svelte-query-devtools";
  import MainLayout from "$lib/components/MainLayout.svelte";
  import GuildsList from "$lib/components/GuildsList.svelte";
  import ChannelsList from "$lib/components/ChannelsList.svelte";
  import MembersList from "$lib/components/MembersList.svelte";
</script>

<QueryClientProvider client={queryClient}>
  <main>
    <MainLayout>
      <GuildsList slot="guilds" />
      <ChannelsList slot="channels" />
      <slot />
      <MembersList slot="members" />
    </MainLayout>
  </main>

  <SvelteQueryDevtools />
</QueryClientProvider>
