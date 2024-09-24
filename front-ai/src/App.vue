<script setup lang="ts"></script>

<template>
  <div class="container">
    <h1>Front de l'application</h1>

    <form action="">
      <div class="form-group">
        <label for="date">Horodatage de l'incident criminel</label>
        <input type="date" name="date" id="date" />
      </div>

      <div class="form-group">
        <label for="day">Jour de la semaine</label>
        <input type="text" name="day" id="day" />
      </div>

      <div class="form-group">
        <label for="nom">Nom du district de police</label>
        <input type="text" name="nom" id="nom" />
      </div>

      <div class="form-group">
        <label for="adresse"
          >Adresse approximative de l'incident criminel</label
        >
        <input type="text" name="adresse" id="adresse" />
      </div>

      <div class="form-group">
        <label for="longitude">Longitude</label>
        <input type="text" name="longitude" id="longitude" />
      </div>

      <div class="form-group">
        <label for="latitude">Latitude</label>
        <input type="text" name="latitude" id="latitude" />
      </div>
    </form>
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
}
</style>
