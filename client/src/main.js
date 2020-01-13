import 'bootstrap/scss/bootstrap.scss';
import BootstrapVue from 'bootstrap-vue';
import Vue from 'vue';
import App from './App.vue';
import router from './router';
import GoogleAuth from 'vue-google-oauth2'

Vue.use(BootstrapVue);

const gauthOptions = {
  clientId: '528797610245-ko6hnrl4d08qcfnt8k2tsqdju4ria97g.apps.googleusercontent.com',
  scope: 'profile email',
  prompt: 'select_account'
};
Vue.use(GoogleAuth, gauthOptions);

Vue.config.productionTip = false;

new Vue({
  router,
  render: h => h(App),
}).$mount('#app');
