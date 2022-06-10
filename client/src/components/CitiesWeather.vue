<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Climatita das cidades</h1>
        <hr><br><br>
        <button type="button" class="btn btn-success btn-sm">Adicionar cidade</button>
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
                  <button type="button" class="btn btn-warning btn-sm">Update</button>
                  <button type="button" class="btn btn-danger btn-sm">Delete</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      weather_data: [],
    };
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
  },
  created() {
    this.getWeatherData();
  },
};
</script>
