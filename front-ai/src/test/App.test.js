import { mount } from "@vue/test-utils";
import { describe, it, expect, vi } from "vitest"; // vi for mocking
import App from "../App.vue";
import axios from "axios"; // Import axios to mock it

// Mock axios
vi.mock("axios");

describe("App-test", () => {
  it("should render the correct HTML of app.vue template", () => {
    const wrapper = mount(App);
    expect(wrapper.html()).toMatchInlineSnapshot(`
      "<div data-v-7a7a37b1="" class="container">
        <h1 data-v-7a7a37b1="">Front de l'application</h1>
        <div data-v-7a7a37b1="" class="main">
          <form data-v-7a7a37b1="">
            <div data-v-7a7a37b1="" class="form-group"><label data-v-7a7a37b1="" for="date">Horodatage de l'incident criminel</label><input data-v-7a7a37b1="" type="datetime-local" name="date" id="date" step="1"></div>
            <div data-v-7a7a37b1="" class="form-group"><label data-v-7a7a37b1="" for="nom">Nom du district de police</label><input data-v-7a7a37b1="" type="text" name="nom" id="nom"></div>
            <div data-v-7a7a37b1="" class="form-group"><label data-v-7a7a37b1="" for="adresse"> Adresse approximative de l'incident criminel </label><input data-v-7a7a37b1="" type="text" name="adresse" id="adresse"></div>
            <div data-v-7a7a37b1="" class="form-group"><label data-v-7a7a37b1="" for="longitude">Longitude</label><input data-v-7a7a37b1="" type="number" step="any" name="longitude" id="longitude"></div>
            <div data-v-7a7a37b1="" class="form-group"><label data-v-7a7a37b1="" for="latitude">Latitude</label><input data-v-7a7a37b1="" type="number" step="any" name="latitude" id="latitude"></div><button data-v-7a7a37b1="" type="submit" aria-label="submit">Prédire</button>
          </form>
          <!--v-if-->
        </div>
      </div>"
    `);
  });

  it("should submit the form and trigger the post request", async () => {
    // Simuler la réponse de axios.post
    axios.post.mockResolvedValue({
      data: {
        prediction: "Résultat de la prédiction",
        data: {
          Dates: "2023-10-10",
          DayOfWeek: "Lundi",
          Adresse: "123 Rue Principale",
          PdDistrict: "Centre",
          X: -122.4194,
          Y: 37.7749,
        },
      },
    });

    const wrapper = mount(App);

    // Définir les valeurs des inputs avant de soumettre le formulaire
    await wrapper.find('input[name="date"]').setValue("2023-10-10T10:00:00");
    await wrapper.find('input[name="nom"]').setValue("Centre");
    await wrapper.find('input[name="adresse"]').setValue("123 Rue Principale");
    await wrapper.find('input[name="longitude"]').setValue(-122.4194);
    await wrapper.find('input[name="latitude"]').setValue(37.7749);

    // Déclencher directement la soumission du formulaire
    await wrapper.find("form").trigger("submit.prevent");

    // Vérifier que axios.post a été appelé avec les bonnes données
    expect(axios.post).toHaveBeenCalledWith("http://localhost:8000/predict", {
      dates: {
        annee: 2023,
        mois: 10,
        jour: 10,
        heure: 10,
        minute: 0,
        seconde: 0,
      },
      pdDistrict: "Centre",
      adresse: "123 Rue Principale",
      position: {
        longitude: -122.4194,
        latitude: 37.7749,
      },
    });

    // Vérifier que le résultat de la prédiction est affiché après la soumission
    await wrapper.vm.$nextTick(); // Attendre la mise à jour du DOM
    expect(wrapper.html()).toContain("Résultat de la prédiction");
  });
});
