<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-25">
        <h1>Climatita das cidades</h1>
        <hr>
        <alert :message=message v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm"
          v-b-modal.cityWeather-modal>Adicionar cidade</button>
        <br>
        <hr>
        <!-- <table class="table table-hover">
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
        </table> -->
        <b-container fluid>
          <b-row>
            <b-col lg="6" class="my-1">
              <b-form-group
                label="Ordenar"
                label-for="sort-by-select"
                label-cols-sm="3"
                label-align-sm="right"
                label-size="sm"
                class="mb-0"
                v-slot="{ ariaDescribedby }"
              >
                <b-input-group size="sm">
                  <b-form-select
                    id="sort-by-select"
                    v-model="sortBy"
                    :options="sortOptions"
                    :aria-describedby="ariaDescribedby"
                    class="w-75"
                  >
                    <template #first>
                      <option value="">-- Nada --</option>
                    </template>
                  </b-form-select>

                  <b-form-select
                    v-model="sortDesc"
                    :disabled="!sortBy"
                    :aria-describedby="ariaDescribedby"
                    size="sm"
                    class="w-25"
                  >
                    <option :value="false">Asc</option>
                    <option :value="true">Desc</option>
                  </b-form-select>
                </b-input-group>
              </b-form-group>
            </b-col>

            <b-col lg="6" class="my-1">
              <b-form-group
                label="Ordem inicial"
                label-for="initial-sort-select"
                label-cols-sm="3"
                label-align-sm="right"
                label-size="sm"
                class="mb-0"
              >
                <b-form-select
                  id="initial-sort-select"
                  v-model="sortDirection"
                  :options="['asc', 'desc', 'last']"
                  size="sm"
                ></b-form-select>
              </b-form-group>
            </b-col>

            <b-col lg="6" class="my-1">
              <b-form-group
                label="Filtro"
                label-for="filter-input"
                label-cols-sm="3"
                label-align-sm="right"
                label-size="sm"
                class="mb-0"
              >
                <b-input-group size="sm">
                  <b-form-input
                    id="filter-input"
                    v-model="filter"
                    type="search"
                    placeholder="Escreva"
                  ></b-form-input>

                  <b-input-group-append>
                    <b-button :disabled="!filter" @click="filter = ''">Limpar</b-button>
                  </b-input-group-append>
                </b-input-group>
              </b-form-group>
            </b-col>

            <b-col lg="6" class="my-1">
              <b-form-group
                v-model="sortDirection"
                label="Filtrar por"
                description="Deixe desmarcado para buscar em todos os dados"
                label-cols-sm="3"
                label-align-sm="right"
                label-size="sm"
                class="mb-0"
                v-slot="{ ariaDescribedby }"
              >
                <b-form-checkbox-group
                  v-model="filterOn"
                  :aria-describedby="ariaDescribedby"
                  class="mt-1"
                >
                  <b-form-checkbox value="city">Cidade</b-form-checkbox>
                  <b-form-checkbox value="temperature">Temperatura</b-form-checkbox>
                  <b-form-checkbox value="dica">Dica</b-form-checkbox>
                </b-form-checkbox-group>
              </b-form-group>
            </b-col>

            <b-col sm="5" md="6" class="my-1">
              <b-form-group
                label="Per page"
                label-for="per-page-select"
                label-cols-sm="6"
                label-cols-md="4"
                label-cols-lg="3"
                label-align-sm="right"
                label-size="sm"
                class="mb-0"
              >
                <b-form-select
                  id="per-page-select"
                  v-model="perPage"
                  :options="pageOptions"
                  size="sm"
                ></b-form-select>
              </b-form-group>
            </b-col>

            <b-col sm="7" md="6" class="my-1">
              <b-pagination
                v-model="currentPage"
                :total-rows="totalRows"
                :per-page="perPage"
                align="fill"
                size="sm"
                class="my-0"
              ></b-pagination>
            </b-col>
          </b-row>
          <hr>
          <b-table
            :items="weather_data"
            :fields="fields"
            :current-page="currentPage"
            :per-page="perPage"
            :filter="filter"
            :filter-included-fields="filterOn"
            :sort-by.sync="sortBy"
            :sort-desc.sync="sortDesc"
            :sort-direction="sortDirection"
            stacked="md"
            show-empty
            small
            responsive
            @filtered="onFiltered"
          >
            <template #cell(city)="row">
              {{ row.item.city }}, {{row.item.country}}
            </template>

            <template #cell(temperature)="row">
              {{row.item.temperature}} °
              <img :src="'http://api.openweathermap.org/img/w/'+row.item.icon+'.png'" alt="Image">
            </template>

            <template #cell(actions)="row">
              <b-button pill size="sm" @click="info(row.item, row.index, $event.target)"
                class="mr-1" variant="outline-info">
                o
              </b-button>
              <b-button size="sm" @click="row.toggleDetails" class="mr-1">
                {{ row.detailsShowing ? 'Esconder' : 'Mostrar' }}
              </b-button>
              <b-button size="sm" variant="warning" v-b-modal.cityWeather-update-modal
                @click="editCityWeather(row.item)" class="mr-1">
                Atualizar
              </b-button>
              <b-button size="sm" variant="danger" @click="onDeleteCityWeather(row.item)"
                class="mr-1">
                Deletar
              </b-button>
            </template>

            <template #row-details="row">
              <b-card>
                <ul>
                  <li v-for="(value, key) in row.item" :key="key">{{ key }}: {{ value }}</li>
                </ul>
              </b-card>
            </template>
          </b-table>

          <b-modal :id="infoModal.id" :title="infoModal.title" ok-only @hide="resetInfoModal">
            <pre>{{ infoModal.content }}</pre>
          </b-modal>
        </b-container>
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
      fields: [
        {
          key: 'city', label: 'Cidade', sortable: true, sortDirection: 'asc',
        },
        {
          key: 'temperature', label: 'Temperatura (°C)', sortable: true, sortDirection: 'desc', class: 'text-center',
        },
        {
          key: 'description', label: 'Descrição', sortable: true, sortDirection: 'desc',
        },
        {
          key: 'dica', label: 'Dica da hora', sortable: true, sortDirection: 'desc',
        },
        {
          key: 'actions', label: 'Ações',
        },
      ],
      totalRows: 1,
      currentPage: 1,
      perPage: 10,
      pageOptions: [10, 15, 20, { value: 100, text: 'Todos' }],
      sortBy: '',
      sortDesc: false,
      sortDirection: 'asc',
      filter: null,
      filterOn: [],
      infoModal: {
        id: 'info-modal',
        title: '',
        content: '',
      },
    };
  },
  components: {
    alert: Alert,
  },
  computed: {
    sortOptions() {
      // Create an options list from our fields
      return this.fields
        .filter((f) => f.sortable)
        .map((f) => ({ text: f.label, value: f.key }));
    },
  },
  mounted() {
    // Set the initial number of items
    this.totalRows = this.weather_data.length;
  },
  methods: {
    getWeatherData() {
      const path = 'http://localhost:5000/cities_weather';
      axios.get(path)
        .then((res) => {
          this.weather_data = res.data.cities_weather;
          console.log(this.weather_data);
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
    info(item, index, button) {
      this.infoModal.title = `Row index: ${index}`;
      this.infoModal.content = JSON.stringify(item, null, 2);
      this.$root.$emit('bv::show::modal', this.infoModal.id, button);
    },
    resetInfoModal() {
      this.infoModal.title = '';
      this.infoModal.content = '';
    },
    onFiltered(filteredItems) {
      this.totalRows = filteredItems.length;
      this.currentPage = 1;
    },
  },
  created() {
    this.getWeatherData();
  },
};
</script>
