<script setup lang="ts">
import axios, { AxiosResponse } from "axios";
import { ref } from "vue";

const date = ref<string>(""); // Valeur initiale vide
const pdDistrict = ref<string>("");
const adresse = ref<string>("");
const longitude = ref<number | null>();
const latitude = ref<number | null>();
const resultPrediction = ref<ResultPrediction>({
  prediction: "",
  data: {
    Dates: "",
    DayOfWeek: "",
    Adresse: "",
    PdDistrict: "",
    X: 0,
    Y: 0,
  },
});

interface DateCustom {
  annee: number;
  mois: number;
  jour: number;
  heure: number;
  minute: number;
  seconde: number;
}

interface Position {
  longitude: number;
  latitude: number;
}

interface PostData {
  dates: DateCustom;
  pdDistrict: string;
  adresse: string;
  position: Position;
}

interface DataResult {
  Dates: string;
  DayOfWeek: string;
  Adresse: string;
  PdDistrict: string;
  X: number;
  Y: number;
}

interface ResultPrediction {
  prediction: string;
  data: DataResult;
}

// Fonction pour formater la date dans le format requis
const formatDateObject = (dateStr: string) => {
  if (!dateStr) {
    return {
      annee: 0,
      mois: 0,
      jour: 0,
      heure: 0,
      minute: 0,
      seconde: 0,
    };
  }

  const dateObj = new Date(dateStr);
  return {
    annee: dateObj.getFullYear(),
    mois: dateObj.getMonth() + 1, // Les mois sont indexés à partir de 0 en JavaScript
    jour: dateObj.getDate(),
    heure: dateObj.getHours(),
    minute: dateObj.getMinutes(),
    seconde: dateObj.getSeconds(),
  };
};

const submitData = (e: Event) => {
  e.preventDefault();

  // Formater la date sous l'objet requis
  const formattedDate = formatDateObject(date.value);
  const position = {
    longitude: longitude.value,
    latitude: latitude.value,
  };

  // Simuler l'envoi des données
  const data = {
    dates: formattedDate,
    pdDistrict: pdDistrict.value,
    adresse: adresse.value,
    position,
  };

  async function postData(url: string, data: PostData): Promise<ResultPrediction> {
    try {
      const response: AxiosResponse<ResultPrediction> = await axios.post(url, data);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.error("Error message:", error.message);
        throw new Error("Erreur lors de l'envoi des données");
      } else {
        console.error("Unexpected error:", error);
        throw new Error("Erreur inattendue");
      }
    }
  }

  //axios.post("http://127.0.0.1:8000/predict", data);

  postData("http://localhost:8000/predict", <PostData>data)
    .then((response) => {
      // console.log("Response from API:", response);
      resultPrediction.value = response as ResultPrediction;
    })
    .catch((error) => {
      console.error("Error:", error);
      resultPrediction.value = {
        prediction: "",
        data: {
          Dates: "",
          DayOfWeek: "",
          Adresse: "",
          PdDistrict: "",
          X: 0,
          Y: 0,
        },
      } as ResultPrediction;
    });

  // todo : vider les champs après l'envoi
  // pdDistrict.value = "";
  // adresse.value = "";
  // longitude.value = null;
  // latitude.value = null;
};
</script>

<template>
  <div class="container">
    <h1>Front de l'application</h1>


    <div class="main">
      <form @submit="submitData">
        <div class="form-group">
          <label for="date">Horodatage de l'incident criminel</label>
          <input type="datetime-local" name="date" id="date" v-model="date" step="1"/>
        </div>

        <div class="form-group">
          <label for="nom">Nom du district de police</label>
          <input type="text" name="nom" id="nom" v-model="pdDistrict" />
        </div>

        <div class="form-group">
          <label for="adresse">
            Adresse approximative de l'incident criminel
          </label>
          <input type="text" name="adresse" id="adresse" v-model="adresse" />
        </div>

        <div class="form-group">
          <label for="longitude">Longitude</label>
          <input
            type="number"
            step="any"
            name="longitude"
            id="longitude"
            v-model="longitude"
          />
        </div>

        <div class="form-group">
          <label for="latitude">Latitude</label>
          <input
              type="number"
              step="any"
              name="latitude"
              id="latitude"
              v-model="latitude"
          />
        </div>

        <button type="submit">Envoyer</button>
      </form>

      <div v-if="resultPrediction.prediction" class="result">
        <h2>Données de l'incident criminel</h2>
        <li v-for="(value, key) in resultPrediction.data" :key="key">
          <strong>{{ key }}:</strong> {{ value }}
        </li>
        <h2>Résultat de la prédiction</h2>
        <p>{{ resultPrediction.prediction }}</p>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.container {
  margin: 0 auto;
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #f5f5f5;
  padding: 20px;

  h1 {
    color: #333;
    margin-bottom: 20px;
  }

  form {
    display: grid;
    gap: 15px;
    width: 100%;
    max-width: 500px;
    background-color: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);

    .form-group {
      display: flex;
      flex-direction: column;
      align-items: flex-start;

      label {
        margin-bottom: 5px;
        font-size: 14px;
        color: #555;
      }

      input {
        width: 90%;
        padding: 10px;
        font-size: 14px;
        border: 1px solid #ccc;
        border-radius: 5px;
        transition: border-color 0.3s;

        &:focus {
          border-color: #007bff;
          outline: none;
        }
      }
    }
  }

  .result {
    margin-left: 100px;
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    padding: 20px;
    width: 100%;
    max-width: 500px;
  }

  .main {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
}
</style>
