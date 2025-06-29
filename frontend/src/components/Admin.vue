<template>
  <div class="max-w-2xl mx-auto p-8">
    <h1 class="text-2xl font-bold mb-6">Admin: Edit Page</h1>
    <form @submit.prevent="savePage" class="space-y-4">
      <div>
        <label class="block font-medium mb-1">Title</label>
        <input v-model="page.title" class="w-full border rounded px-3 py-2" required />
      </div>
      <div>
        <label class="block font-medium mb-1">Slug</label>
        <input v-model="page.slug" class="w-full border rounded px-3 py-2" required />
      </div>
      <div>
        <label class="block font-medium mb-1">Content</label>
        <quill-editor v-model="page.content" :options="editorOptions" class="bg-white" />
      </div>
      <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Save</button>
    </form>
    <div v-if="message" class="mt-4 text-green-600">{{ message }}</div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { QuillEditor } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css'

const page = ref({
  title: '',
  slug: '',
  content: ''
})

const message = ref('')
const editorOptions = {
  theme: 'snow'
}

function savePage() {
  // Placeholder for save logic (API call)
  message.value = 'Page saved (demo only).'
}
</script>
