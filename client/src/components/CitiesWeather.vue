<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Climatita das cidades</h1>
        <hr><br><br>
        <alert :message=message v-if="showMessage" show dismissible></alert>
        <button type="button" class="btn btn-success btn-sm"
          v-b-modal.cityWeather-modal>Adicionar cidade</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Cidade</th>
              <th scope="col">temperatura °C</th>
              <th scope="col"></th>
              <th scope="col">Descricao</th>
              <th scope="col">Dica</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(weather, index) in weather_data" :key="index">
              <td>{{ weather.city }}</td>
              <td>{{ weather.temperature }}</td>
              <td>
                <img :src="'http://api.openweathermap.org/img/w/'+weather.icon+'.png'" alt="Image">
              </td>
              <td>{{ weather.description}}</td>
              <td><b>Dica do dia: </b>{{ weather.dica }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button
                          type="button"
                          class="btn btn-warning btn-sm"
                          v-b-modal.cityWeather-update-modal
                          @click="editCityWeather(weather)">Update</button>
                  <button
                          type="button"
                          class="btn btn-danger btn-sm"
                          @click="onDeleteCityWeather(weather)">
                      Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addCityWeatherModal"
            id="cityWeather-modal"
            title="Adicione uma nova cidade"
            hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-city-group"
                    label="Cidade:"
                    label-for="form-city-input">
          <b-form-input id="form-city-input"
                        type="text"
                        v-model="addCityWeatherForm.city"
                        required
                        placeholder="Cidade">
          </b-form-input>
        </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </b-modal>
    <b-modal ref="editCityWeatherModal"
            id="cityWeather-update-modal"
            title="Update"
            hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
      <b-form-group id="form-city-edit-group"
                    label="Cidade:"
                    label-for="form-city-edit-input">
          <b-form-input id="form-city-edit-input"
                        type="text"
                        v-model="editForm.city"
                        required
                        placeholder="Cidade">
          </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Update</b-button>
          <b-button type="reset" variant="danger">Cancel</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
  data() {
    return {
      weather_data: [],
      addCityWeatherForm: {
        city: '',
      },
      message: '',
      showMessage: false,
      editForm: {
        city_id: '',
        city: '',
      },
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getWeatherData() {
      const path = 'http://localhost:5000/cities_weather';
      axios.get(path)
        .then((res) => {
          this.weather_data = res.data.cities_weather;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addCityWeather(payload) {
      const path = 'http://localhost:5000/cities_weather';
      axios.post(path, payload)
        .then((res) => {
          this.getWeatherData();
          this.message = res.data.message;
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getWeatherData();
        });
    },
    initForm() {
      this.addCityWeatherForm.city = '';
      this.editForm.city_id = '';
      this.editForm.city = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addCityWeatherModal.hide();
      const payload = {
        city: this.addCityWeatherForm.city,
      };
      this.addCityWeather(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addCityWeatherModal.hide();
      this.initForm();
    },
    editCityWeather(weather) {
      this.editForm.city_id = weather.city_id;
      this.editForm.city = weather.city;
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editCityWeatherModal.hide();
      const payload = {
        city: this.editForm.city,
      };
      this.updateCityWeather(payload, this.editForm.city_id);
    },
    updateCityWeather(payload, cityID) {
      const path = `http://localhost:5000/cities_weather/${cityID}`;
      axios.put(path, payload)
        .then((res) => {
          this.getWeatherData();
          this.message = res.data.message;
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getWeatherData();
        });
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editCityWeatherModal.hide();
      this.initForm();
      this.getWeatherData();
    },
    removeCityWeather(cityID) {
      const path = `http://localhost:5000/cities_weather/${cityID}`;
      axios.delete(path)
        .then((res) => {
          this.getWeatherData();
          this.message = res.data.message;
          this.showMessage = true;
        })
        .catch((error) => {
          console.error(error);
          this.getWeatherData();
        });
    },
    onDeleteCityWeather(weather) {
      this.removeCityWeather(weather.city_id);
    },
  },
  created() {
    this.getWeatherData();
  },
};
</script>
