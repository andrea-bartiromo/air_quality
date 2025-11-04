<script setup lang="ts">
import { computed, ref } from 'vue'

// tipi minimi per i dati giornalieri
type DayPoint = {
  date: string
  min: number|null
  average: number|null
  max: number|null
  sample_size: number
}

const route = useRoute()
const { get } = useApi()

// carica i dettagli della stazione dall'API mock del backend
const data = await get<any>(`/stations/${route.params.id}`)

// chiavi delle metriche disponibili (es. PM10, PM2_5)
const metricKeys = computed(() => Object.keys(data.metrics || {}))
const selected = ref(metricKeys.value[0] || '')

// righe per la tabella (ordinate dalla più recente)
const rows = computed<DayPoint[]>(() => {
  const m = data.metrics?.[selected.value]
  const days = m?.days ?? m?.values ?? []
  return [...days].sort((a, b) => (a.date > b.date ? -1 : 1))
})

// media ponderata 7 giorni (se presente) per la metrica selezionata
const weighted = computed(
  () => data.weighted?.[selected.value]?.weighted_average_7d ?? null
)
</script>

<template>
  <main style="padding:24px">
    <div style="display:flex;align-items:center;gap:16px;">
      <h1 style="margin:0;">Stazione {{ data.name || data.id }}</h1>
      <NuxtLink to="/" style="margin-left:auto;text-decoration:underline;">← Back</NuxtLink>
    </div>

    <!-- AGGIUNTA: riepilogo media ponderata 7g per TUTTE le metriche -->
    <ul v-if="metricKeys.length" style="display:flex; gap:12px; flex-wrap:wrap; margin:12px 0; padding:0; list-style:none;">
      <li v-for="k in metricKeys" :key="k" style="border:1px solid #ddd;padding:6px 10px;border-radius:6px;">
        <b>{{ k }}</b> · 7g: <span>{{ data.weighted?.[k]?.weighted_average_7d ?? 'n/a' }}</span>
      </li>
    </ul>

    <div v-if="metricKeys.length" style="margin-top:12px;display:flex;align-items:center;gap:12px;">
      <label for="metric">Metrica:</label>
      <select id="metric" v-model="selected">
        <option v-for="k in metricKeys" :key="k" :value="k">{{ k }}</option>
      </select>
      <span style="margin-left:auto;border:1px solid #ddd;border-radius:6px;padding:6px 10px;">
        Media ponderata 7g: <b>{{ weighted ?? 'n/a' }}</b>
      </span>
    </div>

    <table v-if="rows.length" border="1" cellpadding="6" style="margin-top:16px;width:100%;border-collapse:collapse;">
      <thead>
        <tr>
          <th style="text-align:left;">Data</th>
          <th style="text-align:left;">Min</th>
          <th style="text-align:left;">Avg</th>
          <th style="text-align:left;">Max</th>
          <th style="text-align:left;">Campioni</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="d in rows" :key="d.date">
          <td>{{ d.date }}</td>
          <td>{{ d.min ?? '—' }}</td>
          <td>{{ d.average ?? '—' }}</td>
          <td>{{ d.max ?? '—' }}</td>
          <td>{{ d.sample_size }}</td>
        </tr>
      </tbody>
    </table>

    <p v-else style="margin-top:16px;">Nessun dato disponibile.</p>
  </main>
</template>
