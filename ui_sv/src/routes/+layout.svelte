<script lang="ts">
import "@fontsource-variable/figtree";
import "@fontsource-variable/figtree/wght.css";
import "@fontsource-variable/figtree/wght-italic.css";
import "../app.css";
import { queryClient } from "$lib/api";
import ChannelsList from "$lib/components/ChannelsList.svelte";
import GuildsList from "$lib/components/GuildsList.svelte";
import MainLayout from "$lib/components/MainLayout.svelte";
import MembersList from "$lib/components/MembersList.svelte";
import { QueryClientProvider } from "@tanstack/svelte-query";
import { SvelteQueryDevtools } from "@tanstack/svelte-query-devtools";
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
