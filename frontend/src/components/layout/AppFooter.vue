<template>
  <footer class="bg-white">
    <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
      <div class="border-t border-gray-200 pt-6 flex flex-col md:flex-row justify-between items-center">
        <div class="flex items-center mb-4 md:mb-0">
          <img class="h-6 w-auto" src="@/assets/logo.svg" alt="Wealth Map" />
          <span class="ml-2 text-sm text-gray-500">© {{ currentYear }} Wealth Map. All rights reserved.</span>
        </div>
        
        <div class="flex space-x-6">
          <a href="#" class="text-sm text-gray-500 hover:text-gray-900">Privacy Policy</a>
          <a href="#" class="text-sm text-gray-500 hover:text-gray-900">Terms of Service</a>
          <a href="#" class="text-sm text-gray-500 hover:text-gray-900">Contact Support</a>
        </div>
      </div>
      
      <div class="mt-4 text-xs text-gray-400 text-center">
        <p>Data sources: County Records, Tax Assessor Data, US Census, Property Records</p>
        <p>This tool is for informational purposes only. Data may not be current or accurate.</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue'

const currentYear = computed(() => new Date().getFullYear())
</script>