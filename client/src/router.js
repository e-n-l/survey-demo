import Vue from 'vue';
import Router from 'vue-router';
import Polls from './components/Polls.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Polls',
      component: Polls,
    },
  ],
});
