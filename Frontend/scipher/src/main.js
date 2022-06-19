import Vue from 'vue'
import App from './App.vue'
import VueCookies from 'vue-cookies'
import router from './router'
import axios from 'axios'
import VueAxios from 'vue-axios'
import CKEditor from 'ckeditor4-vue'
import { store } from './store'

import { library } from '@fortawesome/fontawesome-svg-core'
import { faTrash, faComments, faCogs, faHome, faBookmark, faArrowRight, faArrowLeft, faPenToSquare, faCaretRight, faEye, faPlus, faTimes, faSearch, faEllipsis, faCaretUp, faCaretDown, faMagnifyingGlass, faShare } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faTrash, faComments, faCogs, faHome, faBookmark, faEye, faArrowLeft, faArrowRight, faPenToSquare, faCaretRight, faPlus, faTimes, faSearch, faEllipsis, faCaretDown, faMagnifyingGlass, faCaretUp, faShare)
// eslint-disable-next-line
Vue.component('fa', FontAwesomeIcon)

Vue.use(CKEditor);
Vue.use(VueAxios, axios);
Vue.use(VueCookies);
Vue.config.productionTip = false



new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

