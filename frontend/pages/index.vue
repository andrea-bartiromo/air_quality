<script setup lang="ts">
type Station = { id: string; name?: string }
const { get } = useApi()
const stations = await get<Station[]>('/stations')
</script>

<template>
  <main style="padding:24px">
    <h1>Stazioni</h1>
    <ul>
      <li v-for="s in stations" :key="s.id"
          @click="$router.push(`/station/${s.id}`)"
          style="cursor:pointer">
        {{ s.id }} — {{ s.name || "—" }}
      </li>
    </ul>
  </main>
</template>
