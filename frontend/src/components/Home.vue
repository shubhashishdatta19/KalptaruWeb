<template>
  <div class="flex flex-wrap">
    <div class="w-full md:w-1/4 p-4">
      <h2 class="text-xl font-semibold mb-2">Pages</h2>
      <ul>
        <PageTree :nodes="homeData.page_tree" />
      </ul>
    </div>
    <div class="w-full md:w-3/4 p-4">
      <div class="bg-blue-100 rounded-lg p-6 mb-8 text-center">
        <h1 class="text-3xl font-bold mb-2">Welcome to Kalpataru Cultural Association</h1>
        <p class="text-lg mb-2">Fostering culture, community, and creativity.</p>
        <hr class="my-4">
        <p>Join us in our journey to celebrate and promote rich cultural heritage through various events and activities.</p>
      </div>
      <div class="flex flex-wrap -mx-2">
        <div class="w-full md:w-1/2 px-2 mb-6">
          <h2 class="text-xl font-semibold mb-2">Latest Activities</h2>
          <div v-if="homeData.activities.length">
            <router-link
              v-for="activity in homeData.activities"
              :key="activity.id"
              :to="`/activity/${activity.id}`"
              class="block bg-white border rounded p-3 mb-2 hover:bg-gray-50"
            >
              <h5 class="font-medium mb-1">{{ activity.title }}</h5>
              <small v-if="activity.description">{{ activity.description.slice(0, 100) }}...</small>
            </router-link>
          </div>
          <div v-else>
            <p>No recent activities to display.</p>
          </div>
        </div>
        <div class="w-full md:w-1/2 px-2 mb-6">
          <h2 class="text-xl font-semibold mb-2">Upcoming Events</h2>
          <div v-if="homeData.upcoming_events.length">
            <router-link
              v-for="event in homeData.upcoming_events"
              :key="event.id"
              :to="`/event/${event.id}`"
              class="block bg-white border rounded p-3 mb-2 hover:bg-gray-50"
            >
              <h5 class="font-medium mb-1">{{ event.title }}</h5>
              <small v-if="event.schedule">{{ event.schedule.slice(0, 100) }}...</small>
              <span v-if="event.date" class="text-gray-500 ml-2">{{ formatDate(event.date) }}</span>
            </router-link>
          </div>
          <div v-else>
            <p>No events marked as upcoming to display.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const homeData = ref({
  events: [],
  upcoming_events: [],
  activities: [],
  page_tree: []
})

async function fetchHomeData() {
  try {
    const res = await fetch('/api/home_data')
    if (!res.ok) throw new Error('Failed to fetch home data')
    const data = await res.json()
    homeData.value = data
  } catch (e) {
    // Optionally handle error
  }
}

function formatDate(dateStr) {
  const d = new Date(dateStr)
  return d.toLocaleDateString()
}

onMounted(fetchHomeData)

// Recursive component for page tree with links
const PageTree = {
  props: ['nodes'],
  template: `
    <ul>
      <li v-for="node in nodes" :key="node.id">
        <router-link :to="'/page/' + node.slug" class="text-blue-600 hover:underline">{{ node.title }}</router-link>
        <PageTree v-if="node.children && node.children.length" :nodes="node.children" />
      </li>
    </ul>
  `,
  components: {}
}
</script>
