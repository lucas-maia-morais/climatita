import Vue from 'vue';
import Router from 'vue-router';
import Pong from '../components/Pong.vue';
import CitiesWeather from '../components/CitiesWeather.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/pong',
      name: 'Pong',
      component: Pong,
    },
    {
      path: '/',
      name: 'Cities Weather',
      component: CitiesWeather,
    },
  ],
});
