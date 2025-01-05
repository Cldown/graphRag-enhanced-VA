<template>
  <div class="container mx-auto px-4 py-8 max-w-4xl">
    <div class="bg-white rounded-lg shadow-lg">
      <!-- 聊天记录区域 -->
      <div class="h-[600px] overflow-y-auto p-6 space-y-4">
        <div v-for="(message, index) in messages" :key="index" 
             :class="['flex', message.isUser ? 'justify-end' : 'justify-start']">
          <div :class="['max-w-[70%] rounded-lg p-4', 
                       message.isUser ? 'bg-blue-500 text-white' : 'bg-gray-100']">
            <p>{{ message.text }}</p>
            <img v-if="message.image" :src="message.image" 
                 class="mt-2 rounded-lg max-w-full h-auto" />
          </div>
        </div>
      </div>

      <!-- 输入区域 -->
      <div class="border-t p-4 space-y-4">
        <div v-if="selectedFile" class="flex items-center gap-2 bg-gray-100 p-2 rounded">
          <span class="text-sm">已选择文件: {{ selectedFile.name }}</span>
          <button @click="removeFile" 
                  class="text-red-500 hover:text-red-700">
            ✕
          </button>
        </div>
        
        <div class="flex gap-4">
          <input type="text" v-model="userInput" 
                 class="flex-1 border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                 placeholder="请输入您的问题..." />
          
          <label class="cursor-pointer bg-gray-200 hover:bg-gray-300 rounded-lg px-4 py-2">
            选择CSV文件
            <input type="file" accept=".csv" @change="handleFileSelect" class="hidden" />
          </label>
          
          <button @click="sendMessage" 
                  class="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600">
            发送
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const userInput = ref('')
const selectedFile = ref(null)
const messages = ref([
  { text: '你好！我是AI助手，请问有什么可以帮助你的吗？', isUser: false },
  { text: '我可以帮你分析CSV文件或回答问题。', isUser: false }
])

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file && file.type === 'text/csv') {
    selectedFile.value = file
  } else {
    alert('请选择CSV文件')
  }
}

const removeFile = () => {
  selectedFile.value = null
}

const sendMessage = async() => {
  if (!userInput.value.trim() && !selectedFile.value) return

  // 添加用户消息
  messages.value.push({
    text: userInput.value + (selectedFile.value ? `\n文件：${selectedFile.value.name}` : ''),
    isUser: true
  })

  if (selectedFile.value) {
    try {
      const formData = new FormData()
      formData.append('file', selectedFile.value)

      const response = await axios.post('/datas', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })

      const { code, msg } = response.data
      if (code === 200) {
        messages.value.push({ text: `文件处理成功: ${msg}`, isUser: false })
      } else {
        messages.value.push({ text: `文件处理失败: ${msg}`, isUser: false })
      }
    } catch (error) {
      console.error(error)
      messages.value.push({
        text: '上传文件时发生错误，请稍后再试。',
        isUser: false
      })
    }
  } else {
    // 模拟 AI 回复
    setTimeout(() => {
      messages.value.push({
        text: '我已收到您的消息！这是一个模拟的回复。',
        isUser: false
      })
    }, 1000)
  }

  // 清空输入
  userInput.value = ''
  selectedFile.value = null

}
</script>