<template>
  <v-app>
    <v-container fluid>
      <v-row>
      
        <v-col cols="12" md="6">
          <v-file-input label="Выбрать файл" @change="handleFileUpload" class="file-input"></v-file-input>
          <v-img v-if="selectedImage" :src="selectedImage" width="300" height="200" class="uploaded-image"></v-img>
          <v-slider v-model="samplingSteps" color="red" :label="`Sampling Steps: ${samplingSteps}`" min="1" max="100" step="1" thumb-label="always" class="my-5"></v-slider>
          <v-slider v-model="cfgScale" color="green" :label="`CFG Scale: ${cfgScale}`" min="1" max="30" step="1" thumb-label="always" class="my-5"></v-slider>
          <v-slider v-model="denoisingStrength" color="blue" :label="`Denoising Strength: ${denoisingStrength}`" min="0" max="1" step="0.01" thumb-label="always" class="my-5"></v-slider>
          <v-btn color="primary" @click="applyChanges" class="apply-button">Применить</v-btn>
        </v-col>

       
        <v-col cols="12" md="6">
          <div v-if="isLoading" class="d-flex justify-center align-center" style="min-height: 200px;">
            <v-img src="https://wpamelia.com/wp-content/uploads/2018/11/ezgif-2-6d0b072c3d3f.gif" class="loading-animation"></v-img>
          </div>
          <div v-else-if="images.length" class="results-section">
       
            <v-subheader class="text-center">Результат</v-subheader>
            <v-row>
              <v-col v-for="(image, index) in images" :key="'received-' + index" cols="12" sm="4" md="3">
                <v-img :src="image" height="200" class="result-image" @click="openImage(image)"></v-img>
                <div class="d-flex justify-center mt-2">
                  <v-btn small color="primary" :href="image" :download="'image' + index + '.png'">Скачать</v-btn>
                </div>
              </v-col>
            </v-row>
          </div>
        </v-col>
      </v-row>
    </v-container>
    <v-dialog v-model="imageDialog" persistent max-width="600px">
      <v-card>
        <v-toolbar dense flat>
          <v-spacer></v-spacer>
          <v-btn icon @click="closeImage">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-toolbar>
        

        <div class="slider-container" style="padding: 0 16px;">
          <v-slider
            v-model="imageScale"
            :min="1"
            :max="3"
            step="0.1"
            thumb-label="always"
            label="Масштаб изображения"
          ></v-slider>
        </div>
        
        
        <div class="image-container" style="overflow: auto; max-height: 500px;">
          <v-img :src="currentImage" class="view-image" :style="{ transform: `scale(${imageScale})`, transformOrigin: 'top' }"></v-img>
        </div>
      </v-card>
    </v-dialog>
  </v-app>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      selectedImage: null,
      images: [],
      samplingSteps: 20,
      cfgScale: 10,
      denoisingStrength: 0.30,
      imageDialog: false,
      currentImage: '',
      imageScale: 1,
      isLoading: false, // Состояние загрузки
    };
  },
  methods: {
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = () => {
          this.selectedImage = reader.result;
          this.images = []; // Очистка при выборе нового файла
        };
        reader.readAsDataURL(file);
      }
    },
    applyChanges() {
      if (!this.selectedImage) {
        console.error('Изображение не выбрано');
        return;
      }
      this.isLoading = true; // Начало загрузки
      const base64Image = this.selectedImage.split(',')[1];
      
      axios.post('http://127.0.0.1:5000/api/custom_task', {
        param1: base64Image,
        param2: this.samplingSteps.toString(),
        param3: this.cfgScale.toString(),
        param4: this.denoisingStrength.toString(),
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      })
      .then(response => {
        if (response.data.images && response.data.images.length > 0) {
          this.images = response.data.images.map(img => `data:image/png;base64,${img}`);
        } else {
          console.error('Ответ сервера не содержит изображения');
        }
        this.isLoading = false; // Загрузка завершена
      })
      .catch(error => {
        console.error('Ошибка при запросе к серверу:', error);
        this.isLoading = false; // Загрузка завершена с ошибкой
      });
    },
    openImage(imageSrc) {
      this.currentImage = imageSrc;
      this.imageDialog = true;
      this.imageScale = 1; // Сброс масштаба при открытии нового изображения
    },
    closeImage() {
      this.imageDialog = false;
    }
  }
};
</script>

<style>
/* Ваши стили */
.file-input, .my-5 {
  margin-bottom: 20px;
}

.uploaded-image, .result-image {
  margin-top: 20px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.apply-button, .results-section {
  margin-top: 20px;
}

.view-image {
  max-width: 100%;
  height: auto;
  transition: transform 0.3s ease; /* Для плавного масштабирования */
}

.result-image:hover {
  cursor: pointer;
  transform: scale(1.05);
  box-shadow: 0 0 8px rgba(0,0,0,0.2);
}

.mt-2 {
  margin-top: 8px;
}

/* Изменения для применения дизайнерских приёмов Material Design */
.v-btn, .v-img {
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

@media (max-width: 600px) {
  .file-input, .my-5 {
    margin-bottom: 15px;
  }

  .apply-button, .results-section {
    margin-top: 15px;
  }
}

.result-image {
  transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
}

.result-image:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 8px rgba(0,0,0,0.3);
}

.loading-animation {
  
  background-color: transparent;
}
</style>
