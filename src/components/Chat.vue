<template>
  <div class="min-h-screen bg-gray-100 flex items-center justify-center p-4">
    <div class="container max-w-4xl w-full bg-white rounded-xl shadow-2xl overflow-hidden">
      <!-- Chat history area -->
      <div class="h-[600px] overflow-y-auto p-6 space-y-4 bg-gray-50">
        <div v-for="(message, index) in messages" :key="index"
          :class="['flex', message.isUser ? 'justify-end' : 'justify-start']">
          <div :class="['max-w-[70%] rounded-2xl p-4 shadow-md',
            message.isUser ? 'bg-blue-500 text-white' : 'bg-white']">
            <img v-if="message.image" :src="message.image" class="mt-2 rounded-lg max-w-full h-auto" />
            <p v-if="message.text" :class="message.isUser ? 'text-white' : 'text-gray-800'">{{ message.text }}</p>
          </div>
        </div>
      </div>

      <!-- Input area -->
      <div class="border-t border-gray-200 p-6 bg-white">
        <div class="flex gap-4">
          <input type="text" v-model="userInput"
            class="flex-1 border border-gray-300 rounded-full px-6 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-300 ease-in-out"
            placeholder="请输入您的问题..." />

          <label class="cursor-pointer bg-gray-200 hover:bg-gray-300 rounded-full px-6 py-3 transition duration-300 ease-in-out flex items-center justify-center">
            <span class="text-gray-700">选择CSV文件</span>
            <input type="file" accept=".csv" @change="handleFileSelect" class="hidden" />
          </label>

          <button @click="sendMessage" class="bg-blue-500 text-white px-8 py-3 rounded-full hover:bg-blue-600 transition duration-300 ease-in-out flex items-center justify-center">
            <span>发送</span>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 ml-2" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
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
  if (!userInput.value.trim() && !selectedFile.value) return;
  
  messages.value.push({
    text: userInput.value,
    isUser: true,
    image: false,
  });

  console.log(userInput.value);

  var data = {
    order: userInput.value
  };

  axios.post('/api/orders', data, { responseType: 'json' })
    .then(response => {
      console.log(response.data);

      const text = response.data.text;  // 获取返回的字符串
      const imageData = response.data.image;  // 获取返回的图片数据（base64）

      // 将图片数据转换为 Blob 并生成图片 URL
      const imageBlob = new Blob([new Uint8Array([...imageData].map(char => char.charCodeAt(0)))], { type: 'image/png' });
      const imageUrl = URL.createObjectURL(imageBlob);

      // 将文本和图片信息加入消息
      messages.value.push({
        text: text,
        isUser: false,
        image: imageUrl
      });
    })
    .catch(error => {
      console.error(error);
    });

  userInput.value = '';
  selectedFile.value = null;
};

</script>

<style scoped>
/* Add any additional custom styles here if needed */
</style>