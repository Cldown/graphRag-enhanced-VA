<template>
  <div class="container mx-auto px-4 py-8 max-w-4xl">
    <div class="bg-white rounded-lg shadow-lg">
      <!-- 聊天记录区域 -->
      <div class="h-[600px] overflow-y-auto p-6 space-y-4">
        <div v-for="(message, index) in messages" :key="index"
          :class="['flex', message.isUser ? 'justify-end' : 'justify-start']">
          <div :class="['max-w-[70%] rounded-lg p-4',
            message.isUser ? 'bg-blue-500 text-white' : 'bg-gray-100']">
            <img v-if="message.image" :src="message.image" class="mt-2 rounded-lg max-w-full h-auto" />
            <p v-else>{{ message.text }}</p>
          </div>
        </div>
      </div>

      <!-- 输入区域 -->
      <div class="border-t p-4 space-y-4">

        <div class="flex gap-4">
          <input type="text" v-model="userInput"
            class="flex-1 border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="请输入您的问题..." />

          <label class="cursor-pointer bg-gray-200 hover:bg-gray-300 rounded-lg px-4 py-2">
            选择CSV文件
            <input type="file" accept=".csv" @change="handleFileSelect" class="hidden" />
          </label>

          <button @click="sendMessage" class="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600">
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
  { text: '你好！我是AI助手，请问有什么可以帮助你的吗？', isUser: false, image: false },
  { text: '我可以帮你分析CSV文件或回答问题。', isUser: false, image: false },
])

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file && file.type === 'text/csv') {
    messages.value.push({
      text: '已选择文件：' + file.name,
      isUser: true,
      image: false
    })
    selectedFile.value = file
    var formData = new FormData()
    formData.append('file', file)
    // formData.append('type', 'csv')
    axios.post('/api/datas', formData)
      .then(response => {
        console.log(response.data)
      })
      .catch(error => {
        console.error(error)
      })
    messages.value.push({
      text: '正在分析，请输入想要的结果',
      isUser: false,
      image: false
    })
  } else {
    alert('请选择CSV文件')
  }
}

const sendMessage = () => {
  if (!userInput.value.trim() && !selectedFile.value) return
  // 添加用户消息
  messages.value.push({
    text: userInput.value,
    isUser: true,
    image: false,
  })

  console.log(userInput.value)

  var data = {
    order: userInput.value
  }

  axios.post('/api/orders', data).then(response => {
    console.log(response.data)
    messages.value.push({
      text: response.data,
      isUser: false,
      image: response.data
    })
  })
    .catch(error => {
      console.error(error)
    })

  // 清空输入
  userInput.value = ''
  selectedFile.value = null
}
</script>